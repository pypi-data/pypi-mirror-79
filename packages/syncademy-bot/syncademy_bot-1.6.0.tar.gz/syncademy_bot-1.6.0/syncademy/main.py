# Syncademy Bot

# Imports
from syncademy.config import config
from syncademy.bot import discord_bot

# Variables
HEADERS = ['User_Id', 'User_Name', 'User_DisplayName', 'Emojis']
COGS_FOLDER = ['syncademy.cogs.syncademy', 'syncademy.cogs.googlesheet', 'syncademy.cogs.events']

# Cogs load
for extension in COGS_FOLDER:
    discord_bot.bot.load_extension(extension)

# Run bot
discord_bot.bot.run(config.get('discord', 'token'))
