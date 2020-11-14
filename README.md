# TheGreatDtr-Bot
This is a backup of files related to the development of a personalised Discord Bot for a private server, taken from my Repl.it.

## License
Since this is as informal as it gets, this README also contains the basic gist of what I allow you to do with my work.

Feel free to use this for everything, just *credit me* and don't try starting up the same bot on a different environment.

## Installation notes:
`from legacy.redlight import keep_alive`

Among the many modules this bot uses is the Flask module. Flask allows me to create a custom webpage (app in Flask) that I can ping using an UptimeRobot monitor, allowing me to keep the bot running without needing to keep my Repl.it open.

Flask isn't used directly, though, but in combination with a threading.Thread function in a separate script. keep_alive() is the function that encapsulates all of this. The reason threading is needed is because running an app instance from Flask goes indefinitely on its own, and using Thread allows the program to bypass this indefinite process and proceed with the program.

`from main_fam.early_rave import Early`
`from main_fam.hhc import Happy`
`from poke_world.pokemon import Pokedex as Poke`

This program makes use of multiple folder to store programs and additional files, which are referenced in the import section. In addition, Repl.it's file management system assumes the directory that contains main.py to be associated with the main directory, so writing the full path of a file or script is not required. As I continue to import my files for backup I'll also be creating new folders to host them.

> TOKEN = os.environ.get('DISCORD_TOKEN')
> GUILD = os.environ.get('DISCORD_GUILD')

This program makes use of the environmental variable system to retrieve secret variables and values. These are stored in a hidden .env file that hopefully will not be visible to anyone outside yours truly. This variables contain information needed to create a connection between the program and the application instance on Discord.
