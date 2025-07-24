import discord
from discord.ext import commands
import json
import os

with open('config.json') as f:
    config = json.load(f)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

initial_extensions = [
    'cogs.logging_cog',
    'cogs.vote_cog',
    'cogs.say_cog',
    'cogs.config_cog',
    'cogs.welcomer_cog'
]

for ext in initial_extensions:
    bot.load_extension(ext)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

bot.run(config['token'])
