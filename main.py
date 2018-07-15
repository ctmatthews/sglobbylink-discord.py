# sglobbylink-discord.py
# by Mr Peck (2018)
# project page: https://github.com/itsmrpeck/sglobbylink-discord.py
# 
# NOTE: You must enter your Discord bot token and Steam API key below before this will work!

import discord
import asyncio
import urllib.request
import json

client = discord.Client()

# IMPORTANT: get your Discord bot token from https://discordapp.com/developers/applications/me
discordBotTokenDoNotSteal = "PASTE_DISCORD_BOT_TOKEN_HERE"

# IMPORTANT: get your Steam API key from https://steamcommunity.com/dev/apikey
steamApiKeyDoNotSteal = "PASTE_STEAM_API_KEY_HERE"

# replace this with whatever you want!
steamIdFileName = "steam_ids.txt"

steamIdTable = {}

steamIdInstructions = "enter your full Steam profile URL or just the last part, e.g. `!steamid http://steamcommunity.com/id/robinwalker/` or `!steamid robinwalker`"

def save_steam_ids():
    try:
        with open(steamIdFileName, 'w+') as f:
            for steamId in steamIdTable.keys():
                f.write(steamId + " " + steamIdTable[steamId] + "\n")
    except:
        pass


def load_steam_ids():
    try:
        with open(steamIdFileName, 'r') as f:
            steamIdTable.clear()
            for line in f:
                line = line.rstrip('\n')
                splitLine = line.split(" ")
                if len(splitLine) >= 2:
                    steamIdTable[splitLine[0]] = splitLine[1]
    except:
        pass

@client.event
async def on_ready():
    load_steam_ids()

@client.event
async def on_message(message):
    if message.content.startswith('!help'):
        await client.send_message(message.channel, "Hello it's me, the SG Lobby Link bot.\nCommands:\n- `!lobby`: posts the link to your current Steam lobby.\n- `!steamid`: tells the bot what your Steam ID is. You can " + steamIdInstructions)
    if message.content.startswith('!steamid'):
        words = message.content.split(" ")
        if len(words) < 2:
            await client.send_message(message.channel, "`!steamid` usage: " + steamIdInstructions)
        else:
            idStr = words[1]
            idStr = idStr.rstrip('/')

            if idStr.find("steamcommunity.com") != -1:
                lastSlash = idStr.rfind('/')
                if lastSlash != -1:
                    idStr = idStr[lastSlash + 1:]

            if len(idStr) > 200:
                await client.send_message(message.channel, "Error: Steam ID too long.")
            elif idStr.isdigit():
                steamIdTable[message.author.id] = idStr
                save_steam_ids()
                await client.send_message(message.channel, "Saved " + message.author.name + "'s Steam ID.")
            else:
                steamIdUrl = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" + steamApiKeyDoNotSteal + "&vanityurl=" + idStr
                contents = urllib.request.urlopen(steamIdUrl).read()
                if contents:
                    data = json.loads(contents)
                    if data["response"] is None:
                        await client.send_message(message.channel, "SteamAPI: ResolveVanityURL() failed for " + message.author.name + ". Is Steam down?")
                    else:
                        if "steamid" in data["response"].keys():
                            steamIdTable[message.author.id] = data["response"]["steamid"]
                            save_steam_ids()
                            await client.send_message(message.channel, "Saved " + message.author.name + "'s Steam ID.")
                        else:
                            await client.send_message(message.channel, "Could not find Steam ID: " + idStr + ". Make sure you " + steamIdInstructions)
                else:
                    await client.send_message(message.channel, "Error: failed to find " + message.author.name + "'s Steam ID.")

    if message.content.startswith('!lobby'):
        if message.author.id in steamIdTable.keys():
            steamId = steamIdTable[message.author.id]
            profileUrl = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steamApiKeyDoNotSteal + "&steamids=" + steamId
            contents = urllib.request.urlopen(profileUrl).read()
            if contents:
                data = json.loads(contents)
                if "response" in data.keys():
                    pdata = data["response"]["players"][0]
                    if "lobbysteamid" in pdata.keys():
                        steamLobbyUrl = "steam://joinlobby/" + pdata["gameid"] + "/" + pdata["lobbysteamid"] + "/" + steamId
                        gameName = ""
                        if "gameextrainfo" in pdata.keys():
                            gameName = pdata["gameextrainfo"] + " "
                        await client.send_message(message.channel, message.author.name + "'s " + gameName + "lobby: " + steamLobbyUrl)
                    else:
                        await client.send_message(message.channel, "Lobby not found for " + message.author.name + " . Is your Steam profile public, and are you in a lobby?")
                else:
                    await client.send_message(message.channel, "SteamAPI: GetPlayerSummaries() failed for " + message.author.name + ". Is Steam down?")
                    
                        
            else:
                await client.send_message(message.channel, "SteamAPI: GetPlayerSummaries() failed for " + message.author.name + ". Is Steam down?")
        else:
            await client.send_message(message.channel, "Steam ID not found for " + message.author.name +  ". Type `!steamid` and " + steamIdInstructions)

client.run(discordBotTokenDoNotSteal)
