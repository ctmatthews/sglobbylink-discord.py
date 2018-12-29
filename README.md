# sglobbylink-discord.py
A Discord bot made using [discord.py](https://github.com/Rapptz/discord.py) that posts the link to your current Steam game lobby when you type `!lobby`, so other people can easily join your game without having to be on your friends list. It's intended to be used in the matchmaking channel of Fighting Game Community Discord servers, but it could be useful for other types of games too. Feel free to integrate the code into your own Discord bot, or use it as-is on your community's server!

![Someone typing !lobby, and the bot posting the lobby link](https://github.com/itsmrpeck/sglobbylink-discord.py/blob/master/example_lobby_link.png "Example Usage")

# Commands

- `!steamid`: use this to tell the bot your Steam ID, by entering your full Steam profile URL e.g. `!steamid http://steamcommunity.com/id/robinwalker/`. You can get this URL by opening the main Steam window, hovering over your name (next to Store/Library/Community), clicking Profile, right-clicking the page background and choosing Copy Page URL.
- `!lobby`: makes the bot post your lobby link, so people can click it and join your game. NOTE: The bot can't get your lobby ID if your Steam profile is set to private, or if you are set to Appear Offline on your Steam friends. This is out of my control; it's just how the Steam Web API works.

![Editing My Privacy Settings on a Steam profile, with My Profile and Game Details both set to Public](https://github.com/itsmrpeck/sglobbylink-discord.py/blob/master/public_profile.png "Public Profile")

# Overview Video

https://www.youtube.com/watch?v=aIhaKxGLxBc

# Installation

- Download and install Python and [discord.py](https://github.com/Rapptz/discord.py)
  - **NOTE: I recommend using a version of Python 3.6, e.g. Python 3.6.8. The bot uses features that were added in Python 3.5, and unfortunately Discord.py is currently incompatible with Python 3.7 and above.**
- Download/clone this repository, or just save [main.py](https://github.com/itsmrpeck/sglobbylink-discord.py/blob/master/main.py), [settings_sglobbylink.py](https://github.com/itsmrpeck/sglobbylink-discord.py/blob/master/settings_sglobbylink.py) and [public_profile_instructions.jpg](https://github.com/itsmrpeck/sglobbylink-discord.py/blob/master/public_profile_instructions.jpg) to wherever you're going to run your bot. You can rename main.py to something else if you want, or even integrate its code into your existing Discord bot if you're feeling ambitious.
- Get a Discord bot token and Steam API key, and paste them in the appropriate places near the top of settings_sglobbylink.py. If you don't have them, you can get them from https://discordapp.com/developers/applications/me and https://steamcommunity.com/dev/apikey .
