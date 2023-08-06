# Imports
from discord.ext import commands


# Initialize Discord Bot
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
