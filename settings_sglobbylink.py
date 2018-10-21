# sglobbylink-discord.py
# by Mr Peck (2018)
# project page: https://github.com/itsmrpeck/sglobbylink-discord.py

######################################
####### API KEYS:

# IMPORTANT: You must enter these or the bot won't work!

# IMPORTANT: get your Discord bot token from https://discordapp.com/developers/applications/me
discordBotTokenIMPORTANT = "PASTE_DISCORD_BOT_TOKEN_HERE"

# IMPORTANT: get your Steam API key from https://steamcommunity.com/dev/apikey
steamApiKeyIMPORTANT = "PASTE_STEAM_API_KEY_HERE"


######################################
####### SETTINGS:

# Everything here can be left at the default values unless you want to change them.

# You can replace this with whatever you want, or leave it as it is. This is where the bot stores its users' Steam IDs.
steamIdFileName = "steam_ids.txt"

# Add channel IDs to the whitelist if you only want the bot to read and reply to messages in certain channels.
# Leaving the whitelist empty means the bot runs in all channels of your server.
# You can get a channel's ID by enabling Settings->Appearance->Developer Mode in Discord then right-clicking a channel.
# wrap your channel IDs in quotation marks, and separate them with commas if there's more than one channel.
# e.g. channelWhitelistIDs =  ["476458350444412951", "112133450844143616"]
channelWhitelistIDs = []

# Set this to False if you want users to be able to just enter the last part of their URL, e.g. "!steamid robinwalker" instead of "!steamid http://steamcommunity.com/id/robinwalker/".
# I highly recommend keeping this set to True. Setting it to false just confuses a bunch of players into accidentally entering their Steam nicknames.
# e.g. Jim tries typing "!steamid Jim", and the bot ends up finding "http://steamcommunity.com/id/Jim/" (who is someone else), and Jim can't figure
# out why the bot can never find his lobbies.
onlyAllowFullProfileURLs = True

# Set this to False if you don't want users to be able to request their lobby URL via Direct Messages/Whispers
allowDirectMessages = True

# Rate limiting: each user can only ask the bot for this many things per day. This stops you from breaking the daily request limit for your Steam API key.
maxDailyRequestsPerUser = 60
maxTotalDailyRequests = 45000

# Image spam limiting: How often the bot will post the public_profile_instructions.jpg image for people with private profiles
allowImagePosting = True
imagePostingCooldownSeconds = 60 * 10

#######
######################################
