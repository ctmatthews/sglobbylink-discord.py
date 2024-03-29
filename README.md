# NO LONGER WORKING OR MAINTAINED
Apparently this bot no longer works. I have not tested it myself, but I assume it's through some combination of Python, discord.py or or the Steam Web API making a breaking change somewhere. In the time since I made this bot, I programmed the lobby link feature directly into Skullgirls (the main fighting game I was playing at the time) and [Chessplosion](https://store.steampowered.com/app/1571220/Chessplosion) (my own game with rollback netcode), and I'm not a web programmer or Python programmer so I have no interest in updating this bot myself or maintaining this repo. If you want to make a fixed version of this bot, I recommend forking it and making your own repo.

# sglobbylink-discord.py
A Discord bot made using [discord.py](https://github.com/Rapptz/discord.py) that posts the link to your current Steam game lobby when you type `!lobby`, so other people can easily join your game without having to be on your friends list. It's intended to be used in the matchmaking channel of Fighting Game Community Discord servers, but it could be useful for other types of games too. Feel free to integrate the code into your own Discord bot, or use it as-is on your community's server!
![Someone typing !lobby, and the bot posting the lobby link](https://github.com/ctmatthews/sglobbylink-discord.py/blob/master/example_lobby_link.png "Example Usage")

# Commands

- `!steamid`: use this to tell the bot your Steam ID, by entering your full Steam profile URL e.g. `!steamid http://steamcommunity.com/id/robinwalker/`. You can get this URL by opening the main Steam window, hovering over your name (next to Store/Library/Community), clicking Profile, right-clicking the page background and choosing Copy Page URL.
  - *NOTE: Unfortunately everyone has to do this step, even people who have already linked their Steam account to their Discord account. This is out of my control; Discord does not allow bots to read Steam account data from people's Discord profiles.*
- `!lobby`: makes the bot post your lobby link, so people can click it and join your game.
  - *NOTE: The bot can't get your lobby ID if your Steam profile is set to private or if you are set to Appear Offline on your Steam friends. This is out of my control; it's just how the Steam Web API works. There is a workaround if you don't want to force everyone to make their Steam accounts public: create a Steam account for the bot, generate a Steam Web API key using that account, and let people add the bot to their Steam friends list. This lets the bot see all of their friends-only Steam profile details, including their lobby ID.*

![Editing My Privacy Settings on a Steam profile, with My Profile and Game Details both set to Public](https://github.com/ctmatthews/sglobbylink-discord.py/blob/master/public_profile.png "Public Profile")

# Overview Video

https://www.youtube.com/watch?v=aIhaKxGLxBc

# Installation

- Download and install Python and [discord.py](https://github.com/Rapptz/discord.py)
  - **NOTE: The bot requires Python 3.6 or higher, and discord.py 1.0 or higher. Unfortunately both Python and discord.py made several breaking changes across versions, so I can't make the bot backwards-compatible with older versions.**
- Download/clone this repository, or just save [main.py](https://github.com/ctmatthews/sglobbylink-discord.py/blob/master/main.py), [settings_sglobbylink.py](https://github.com/ctmatthews/sglobbylink-discord.py/blob/master/settings_sglobbylink.py) and [public_profile_instructions.jpg](https://github.com/ctmatthews/sglobbylink-discord.py/blob/master/public_profile_instructions.jpg) to wherever you're going to run your bot. You can rename main.py to something else if you want, or even integrate its code into your existing Discord bot if you're feeling ambitious.
- Get a Discord bot token and Steam API key, and paste them in the appropriate places near the top of settings_sglobbylink.py. If you don't have them, you can get them from https://discordapp.com/developers/applications/me and https://steamcommunity.com/dev/apikey .

# Support

This bot can be used free of charge because I want to support the wider Fighting Game Community as much as possible. However, it takes time for me to update, maintain and support it. If you would like to help support my work, buy my videogames at:

https://store.steampowered.com/franchise/ctmatthews

https://ctmatthews.itch.io/
