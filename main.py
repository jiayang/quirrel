#main.py

import os

import settings
import discord
from discord.ext import commands

EXTENSIONS=['admin',
            'anime',
            'guild',
            'music',
            'survey',
            'weather',
            'rand',
            'rejoinupburst',
            'games',
#            'tcg',
            'playlist',
            'basketball',
            'image'
]

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
token = os.getenv("DISCORD_SECRET_TOKEN")

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

    #Custom playing status

    #DEFAULT
    #activity = discord.Game("near the Blue Lake")

    #FROZEN
    activity = discord.Activity()
    activity.type = discord.ActivityType.listening
    activity.name = 'an angel sing Vuelie'
    await bot.change_presence(activity=activity)

if __name__ == '__main__':
    for extension in EXTENSIONS:
        try:
            bot.load_extension('cogs.' + extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    bot.run(token)
