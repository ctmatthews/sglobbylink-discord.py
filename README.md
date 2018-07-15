# sglobbylink-discord.py
A discord bot made using [discord.py](https://github.com/Rapptz/discord.py) that posts the link to your current Steam game lobby when you type `!lobby`, so other people can join your game having to be on your friends list. It's intended to be used in the matchmaking channel of fighting game community Discord servers, but it could be useful for other types of games too. Feel free to integrate it into Discord bots of your own, or use it on your community's server!

# Commands

- `!steamid`: tells the bot your Steam ID, using the name in your profile URL. e.g. `!steamid mrpeck` if your Steam profile is http://steamcommunity.com/id/mrpeck
- `!lobby`: makes the bot post your lobby link, so they can click it and join your game.

# Troubleshooting

- The bot can't get your lobby ID if your Steam profile is set to private, or if you are set to Appear Offline on your Steam friends.
- You need to have a Discord bot token and Steam API key to run this bot. Enter them in the appropriate places at the top of main.py. If you don't have them, you can get them from https://discordapp.com/developers/applications/me and https://steamcommunity.com/dev/apikey .
