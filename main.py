# sglobbylink-discord.py
# by Peck (2018-2023)
# project page: https://github.com/ctmatthews/sglobbylink-discord.py

# IMPORTANT: You must enter your Discord bot token and Steam API key in settings_sglobbylink.py or the bot won't work!

import discord
import asyncio
import json
import aiohttp
import threading
import time
from enum import Enum
from settings_sglobbylink import *

# Default settings for old versions of settings_sglobbylink:
if not "allowImagePosting" in locals():
    allowImagePosting = True

if not "imagePostingCooldownSeconds" in locals():
    imagePostingCooldownSeconds = 60 * 10

if discordBotTokenIMPORTANT == "PASTE_DISCORD_BOT_TOKEN_HERE":
    print("ERROR: Discord bot token has not been set. Get one from https://discordapp.com/developers/applications/me and paste it into 'discordBotTokenIMPORTANT' in settings_sglobbylink.py")
    quit()

if steamApiKeyIMPORTANT == "PASTE_STEAM_API_KEY_HERE":
    print("ERROR: Steam Web API key has not been set. Get one from https://steamcommunity.com/dev/apikey and paste it into 'steamApiKeyIMPORTANT' in settings_sglobbylink.py")
    quit()


versionNumber = "1.41"

steamProfileUrlIdentifier = "steamcommunity.com/id"
steamProfileUrlIdentifierLen = len(steamProfileUrlIdentifier)

steamProfileUrlLongIdentifier = "steamcommunity.com/profiles"
steamProfileUrlLongIdentifierLen = len(steamProfileUrlLongIdentifier)

steamIdTable = {}

steamIdInstructionsOnlyFullURL = "enter your full Steam profile URL, e.g. `!steamid http://steamcommunity.com/id/robinwalker/`"
steamIdInstructionsPartialURLAllowed = "enter your full Steam profile URL or just the last part, e.g. `!steamid http://steamcommunity.com/id/robinwalker/` or `!steamid robinwalker`. DON'T just enter your current Steam nickname, e.g. `!steamid Jim`, or it will think you are `http://steamcommunity.com/id/Jim/`"

todaysRequestCounts = {}

todaysTotalRequestCount = 0

requestCountsLock = threading.RLock()

lastPublicProfileImagePostedTimestamp = 0
lastSteamURLImagePostedTimestamp = 0

client = discord.Client()

class RequestLimitResult(Enum):
    LIMIT_NOT_REACHED = 1
    USER_LIMIT_JUST_REACHED = 2
    TOTAL_LIMIT_JUST_REACHED = 3
    ALREADY_OVER_LIMIT = 4

class LobbyBotCommand(Enum):
    NONE = 1
    HELP = 2
    STEAMID = 3
    LOBBY = 4

def get_steam_id_instructions():
    if onlyAllowFullProfileURLs:
        return steamIdInstructionsOnlyFullURL
    else:
        return steamIdInstructionsPartialURLAllowed

async def save_steam_ids():
    try:
        with open(steamIdFileName, 'w+') as f:
            for discordUserId in steamIdTable.keys():
                f.write(str(discordUserId) + " " + steamIdTable[discordUserId] + "\n")
    except:
        pass

async def load_steam_ids():
    global steamIdFileName
    global steamIdTable

    try:
        with open(steamIdFileName, 'r') as f:
            steamIdTable.clear()
            for line in f:
                line = line.rstrip('\n')
                splitLine = line.split(" ")
                if len(splitLine) >= 2:
                    steamIdTable[int(splitLine[0])] = splitLine[1]
    except:
        pass

def increment_request_count(userIdInt): # returns whether or not the user has hit their daily request limit
    global todaysRequestCounts
    global todaysTotalRequestCount
    global maxDailyRequestsPerUser
    global maxTotalDailyRequests

    if maxDailyRequestsPerUser <= 0:
        return RequestLimitResult.ALREADY_OVER_LIMIT

    with requestCountsLock:

        if todaysTotalRequestCount > maxTotalDailyRequests:
            return RequestLimitResult.ALREADY_OVER_LIMIT

        if userIdInt not in todaysRequestCounts.keys():
            todaysRequestCounts[userIdInt] = 0

        if todaysRequestCounts[userIdInt] > maxDailyRequestsPerUser:
            return RequestLimitResult.ALREADY_OVER_LIMIT

        todaysRequestCounts[userIdInt] += 1
        todaysTotalRequestCount += 1

        if todaysTotalRequestCount > maxTotalDailyRequests:
            return RequestLimitResult.TOTAL_LIMIT_JUST_REACHED

        elif todaysRequestCounts[userIdInt] > maxDailyRequestsPerUser:
            return RequestLimitResult.USER_LIMIT_JUST_REACHED

        else:
            return RequestLimitResult.LIMIT_NOT_REACHED

    return RequestLimitResult.ALREADY_OVER_LIMIT


async def clear_request_counts_once_per_day():
    global todaysRequestCounts
    global todaysTotalRequestCount

    await client.wait_until_ready()
    while not client.is_closed():
        with requestCountsLock:
            todaysRequestCounts.clear()
            todaysTotalRequestCount = 0
        await asyncio.sleep(60*60*24) # task runs every 24 hours

def check_if_public_profile_image_can_be_posted_and_update_timestamp_if_true():
    global allowImagePosting
    global imagePostingCooldownSeconds
    global lastPublicProfileImagePostedTimestamp

    if allowImagePosting:
        currentTime = time.time()
        if (currentTime - lastPublicProfileImagePostedTimestamp) >= imagePostingCooldownSeconds:
            lastPublicProfileImagePostedTimestamp = currentTime
            return True

    return False

def check_if_steam_url_image_can_be_posted_and_update_timestamp_if_true():
    global allowImagePosting
    global imagePostingCooldownSeconds
    global lastSteamURLImagePostedTimestamp

    if allowImagePosting:
        currentTime = time.time()
        if (currentTime - lastSteamURLImagePostedTimestamp) >= imagePostingCooldownSeconds:
            lastSteamURLImagePostedTimestamp = currentTime
            return True

    return False

async def async_get_json(url): 
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                return None

@client.event
async def on_ready():
    await load_steam_ids()
    client.loop.create_task(clear_request_counts_once_per_day())
    print("LOADED: sglobbylink-discord.py v" + versionNumber + " by Peck.")

@client.event
async def on_message(message):

    # all commands start with '!', but we try to handle messages that start with <@ too
    if not message.content.startswith('!') and not message.content.startswith('<@'):
        return

    messageContent = message.content[:40] # Grab enough message for an @username and some whitespace before the !command

    # If we start with a <@, skip everything up to the >
    startedWithUsername = messageContent.startswith('<@')
    if startedWithUsername:
        whitespaceStart = messageContent.find('>')
        if whitespaceStart > 0:
            messageContent = messageContent[(whitespaceStart + 1):]
        else:
            return # We didn't find a '>'

    # Skip leading whitespace
    messageContent =  messageContent.lstrip()

    # all commands start with '!'
    if not messageContent.startswith('!'):
        return

    # filter out DMs
    if not allowDirectMessages and not message.channel:
        return

    # filter out messages not on the whitelisted channels
    if channelWhitelistIDs and message.channel:
        channelFound = False
        for channelID in channelWhitelistIDs:
            if message.channel.id == (int(channelID) if isinstance(channelID, str) else channelID):
                channelFound = True
                break
        if not channelFound:
            return

    # check which command we wanted (and ignore any message that isn't a command)
    lowerCaseMessageStart = messageContent[:8].lower()
    if lowerCaseMessageStart.startswith('!help') and not startedWithUsername:
        botCmd = LobbyBotCommand.HELP
    elif lowerCaseMessageStart.startswith('!steamid') and not startedWithUsername:
        botCmd = LobbyBotCommand.STEAMID
    elif lowerCaseMessageStart.startswith('!lobby'):
        botCmd = LobbyBotCommand.LOBBY
    else:
        return

    # rate limit check
    rateLimitResult = increment_request_count(message.author.id)
    if rateLimitResult == RequestLimitResult.ALREADY_OVER_LIMIT:
        return
    elif rateLimitResult == RequestLimitResult.TOTAL_LIMIT_JUST_REACHED:
        await message.channel.send("Error: Total daily bot request limit reached. Try again in 24 hours.")
        return
    elif rateLimitResult == RequestLimitResult.USER_LIMIT_JUST_REACHED:
        await message.channel.send("Error: Daily request limit reached for user " + message.author.name + ". Try again in 24 hours.")
        return

    # actually execute the command
    if botCmd == LobbyBotCommand.HELP:
        await message.channel.send("Hello, I am sglobbylink-discord.py v" + versionNumber + " by Peck.\n\nCommands:\n- `!lobby`: posts the link to your current Steam lobby.\n- `!steamid`: tells the bot what your Steam profile is. You can " + get_steam_id_instructions())
        if check_if_steam_url_image_can_be_posted_and_update_timestamp_if_true():
            await message.channel.send("", file=discord.File("steam_url_instructions.jpg"))
        return

    elif botCmd == LobbyBotCommand.STEAMID:
        words = message.content.split(" ")
        bSavedSteamId = False
        if len(words) < 2:
            await message.channel.send("`!steamid` usage: " + get_steam_id_instructions())
            if check_if_steam_url_image_can_be_posted_and_update_timestamp_if_true():
                await message.channel.send("", file=discord.File("steam_url_instructions.jpg"))
            return
        else:
            maxWordCount = min(len(words), 10)
            idStr = ""
            for i in range(1, maxWordCount):
                if len(words[i]) > 0:
                    idStr = words[i]
                    break

            idStr = idStr.rstrip('/')

            profileUrlStart = idStr.find(steamProfileUrlIdentifier)
            if profileUrlStart != -1:
                # It's a steam profile URL. Erase everything after the last slash
                lastSlash = idStr.rfind('/')
                if lastSlash >= (profileUrlStart + steamProfileUrlIdentifierLen):
                    idStr = idStr[lastSlash + 1:]
                else:
                    # This is a malformed profile URL, with no slash after "steamcommunity.com/id"
                    await message.channel.send("`!steamid` usage: " + get_steam_id_instructions())
                    if check_if_steam_url_image_can_be_posted_and_update_timestamp_if_true():
                        await message.channel.send("", file=discord.File("steam_url_instructions.jpg"))
                    return
            else:
                # Try the other type of steam profile URL. Let's copy and paste.
                profileUrlStart = idStr.find(steamProfileUrlLongIdentifier)

                if profileUrlStart != -1:
                    # It's a steam profile URL. Erase everything after the last slash
                    lastSlash = idStr.rfind('/')
                    if lastSlash >= (profileUrlStart + steamProfileUrlLongIdentifierLen):
                        idStr = idStr[lastSlash + 1:]
                    else:
                        # This is a malformed profile URL, with no slash after "steamcommunity.com/profiles"
                        await message.channel.send("`!steamid` usage: " + get_steam_id_instructions())
                        if check_if_steam_url_image_can_be_posted_and_update_timestamp_if_true():
                            await message.channel.send("", file=discord.File("steam_url_instructions.jpg"))
                        return
                elif onlyAllowFullProfileURLs:
                    # This isn't either type of full profile URL, and we're only allowing full profile URLs
                    await message.channel.send("`!steamid` usage: " + get_steam_id_instructions())
                    if check_if_steam_url_image_can_be_posted_and_update_timestamp_if_true():
                        await message.channel.send("", file=discord.File("steam_url_instructions.jpg"))
                    return

            if len(idStr) > 200:
                await message.channel.send("Error: Steam ID too long.")
                return
            else:
                steamIdUrl = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" + steamApiKeyIMPORTANT + "&vanityurl=" + idStr
                contents = await async_get_json(steamIdUrl)
                if contents:
                    data = json.loads(contents)
                    if data["response"] is None:
                        await message.channel.send("SteamAPI: ResolveVanityURL() failed for " + message.author.name + ". Is the Steam Web API down?")
                        return
                    else:
                        if "steamid" in data["response"].keys():
                            steamIdTable[message.author.id] = data["response"]["steamid"]
                            await save_steam_ids()
                            await message.channel.send("Saved " + message.author.name + "'s Steam ID.")
                            bSavedSteamId = True
                            # Don't return; fall through to the "if bSavedSteamId" code instead
                        elif idStr.isdigit():
                            steamIdTable[message.author.id] = idStr
                            await save_steam_ids()
                            await message.channel.send("Saved " + message.author.name + "'s Steam ID.")
                            bSavedSteamId = True
                            # Don't return; fall through to the "if bSavedSteamId" code instead
                        else:
                            await message.channel.send("Could not find Steam ID: " + idStr + ". Make sure you " + get_steam_id_instructions())
                            if check_if_steam_url_image_can_be_posted_and_update_timestamp_if_true():
                                await message.channel.send("", file=discord.File("steam_url_instructions.jpg"))
                            return
                else:
                    await message.channel.send("Error: failed to find " + message.author.name + "'s Steam ID.")
                    return

        if bSavedSteamId:
            # It's common for players to add themselves to the bot without their Steam Game Details being public. Tell them this right away, to save time
            if message.author.id in steamIdTable.keys():
                steamId = steamIdTable[message.author.id]
                profileUrl = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steamApiKeyIMPORTANT + "&steamids=" + steamId
                contents = await async_get_json(profileUrl)
                if contents:
                    data = json.loads(contents)
                    if "response" in data.keys():
                        pdata = data["response"]["players"][0]
                        if "lobbysteamid" not in pdata.keys():
                            # Steam didn't give us a lobby ID. But why?
                            # Let's test if their profile's Game Details are public by seeing if Steam will tell us how many games they own.
                            ownedGamesUrl = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + steamApiKeyIMPORTANT + "&steamid=" + steamId + "&include_played_free_games=1"
                            ownedGamesContents = await async_get_json(ownedGamesUrl)
                            if ownedGamesContents:
                                ownedGamesData = json.loads(ownedGamesContents)
                                if "response" in ownedGamesData.keys():
                                    if not ("game_count" in ownedGamesData["response"].keys() and ownedGamesData["response"]["game_count"] > 0):
                                        await message.channel.send("(Note for " + message.author.name + ": Your profile's Game Details are not public, so the bot won't be able to see if you're in a lobby.)")
                                        if check_if_public_profile_image_can_be_posted_and_update_timestamp_if_true():
                                            await message.channel.send("", file=discord.File("public_profile_instructions.jpg"))
        return

    elif botCmd == LobbyBotCommand.LOBBY:
        if message.author.id in steamIdTable.keys():
            steamId = steamIdTable[message.author.id]
            profileUrl = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steamApiKeyIMPORTANT + "&steamids=" + steamId
            contents = await async_get_json(profileUrl)
            if contents:
                data = json.loads(contents)
                if "response" in data.keys():
                    pdata = data["response"]["players"][0]
                    if "lobbysteamid" in pdata.keys():
                        steamLobbyUrl = "steam://joinlobby/" + pdata["gameid"] + "/" + pdata["lobbysteamid"] + "/" + steamId
                        gameName = ""
                        if "gameextrainfo" in pdata.keys():
                            gameName = pdata["gameextrainfo"] + " "
                        await message.channel.send(message.author.name + "'s " + gameName + "lobby: " + steamLobbyUrl)
                        return
                    else:
                        # Steam didn't give us a lobby ID. But why?
                        # Let's test if their profile's Game Details are public by seeing if Steam will tell us how many games they own.
                        ownedGamesUrl = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + steamApiKeyIMPORTANT + "&steamid=" + steamId + "&include_played_free_games=1"
                        ownedGamesContents = await async_get_json(ownedGamesUrl)
                        if ownedGamesContents:
                            ownedGamesData = json.loads(ownedGamesContents)
                            if "response" in ownedGamesData.keys():
                                if "game_count" in ownedGamesData["response"].keys() and ownedGamesData["response"]["game_count"] > 0:
                                    # They have public Game Details. Let's make sure we can see their account, and that they're online
                                    if pdata["communityvisibilitystate"] == 3: # If the bot can view whether or not the player's Steam account is online https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_.28v0002.29
                                        if "personastate" in pdata.keys() and pdata["personastate"] > 0:
                                            # They have public Game Details, Steam thinks they're online. Let's see if they're in a game!
                                            if "gameid" in pdata.keys():
                                                gameName = ""
                                                if "gameextrainfo" in pdata.keys():
                                                    gameName = pdata["gameextrainfo"]
                                                else:
                                                    gameName = "a game"
                                                await message.channel.send("Lobby not found for " + message.author.name + ": Steam thinks you're playing " + gameName + " but not in a lobby.")
                                                return
                                            else:
                                                await message.channel.send("Lobby not found for " + message.author.name + ": Steam thinks you're online but not playing a game.")
                                                return
                                        else:
                                            await message.channel.send("Lobby not found for " + message.author.name + ": Steam thinks you're offline. Make sure you're connected to Steam, and not set to Appear Offline on your friends list.")
                                            return
                                    else:
                                        await message.channel.send("Lobby not found for " + message.author.name + ": Your profile is not public, so the bot can't see if you're in a lobby.")
                                        if check_if_public_profile_image_can_be_posted_and_update_timestamp_if_true():
                                            await message.channel.send("", file=discord.File("public_profile_instructions.jpg"))
                                        return
                                else:
                                    await message.channel.send("Lobby not found for " + message.author.name + ": Your profile's Game Details are not public, so the bot can't see if you're in a lobby.")
                                    if check_if_public_profile_image_can_be_posted_and_update_timestamp_if_true():
                                        await message.channel.send("", file=discord.File("public_profile_instructions.jpg"))
                                    return
                            else:
                                await message.channel.send("SteamAPI: GetOwnedGames() failed for " + message.author.name + ". Is the Steam Web API down?")
                                return
                        else:
                            await message.channel.send("SteamAPI: GetOwnedGames() failed for " + message.author.name + ". Is the Steam Web API down?")
                            return
                else:
                    await message.channel.send("SteamAPI: GetPlayerSummaries() failed for " + message.author.name + ". Is the Steam Web API down?")
                    return
                        
            else:
                await message.channel.send("SteamAPI: GetPlayerSummaries() failed for " + message.author.name + ". Is the Steam Web API down?")
                return
        else:
            await message.channel.send("Steam ID not found for " + message.author.name +  ". Type `!steamid` and " + get_steam_id_instructions())
            if check_if_steam_url_image_can_be_posted_and_update_timestamp_if_true():
                await message.channel.send("", file=discord.File("steam_url_instructions.jpg"))
            return

client.run(discordBotTokenIMPORTANT)
