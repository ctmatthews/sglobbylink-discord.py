# sglobbylink-discord.py
A Discord bot made using [discord.py](https://github.com/Rapptz/discord.py) that posts the link to your current Steam game lobby when you type `!lobby`, so other people can easily join your game without having to be on your friends list. It's intended to be used in the matchmaking channel of Fighting Game Community Discord servers, but it could be useful for other types of games too. Feel free to integrate it into Discord bots of your own, or use it on your community's server!

![Someone typing !lobby, and the bot posting the lobby link](https://github.com/itsmrpeck/sglobbylink-discord.py/blob/master/lobby_link.png "Example Usage")

# Commands

- `!steamid`: use this to tell the bot your Steam ID, by entering your full Steam profile URL or just the last part. e.g. `!steamid http://steamcommunity.com/id/robinwalker/` or `!steamid robinwalker`.
- `!lobby`: makes the bot post your lobby link, so people can click it and join your game. NOTE: The bot can't get your lobby ID if your Steam profile is set to private, or if you are set to Appear Offline on your Steam friends.

![Editing My Privacy Settings on a Steam profile, with My Profile and Game Details both set to Public](https://github.com/itsmrpeck/sglobbylink-discord.py/blob/master/public_profile.png "Public Profile")

# Installation

- Download and install [discord.py](https://github.com/Rapptz/discord.py)
- Download/clone this repository, or just save [main.py](https://github.com/itsmrpeck/sglobbylink-discord.py/blob/master/main.py) to wherever you're going to run your bot. You can rename it to something else if you want, or even integrate it into your existing Discord bot if you're feeling ambitious.
- Get a Discord bot token and Steam API key, and paste them in the appropriate places near the top of main.py. If you don't have them, you can get them from https://discordapp.com/developers/applications/me and https://steamcommunity.com/dev/apikey .
