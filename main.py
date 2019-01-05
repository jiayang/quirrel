import discord
from discord.ext import commands
import git

startup_extensions=['admin','guild','survey','upburst','weather'] # Discontinued: basketball
bot = commands.Bot(command_prefix='!')
token = open('secret/token.txt','r').read().strip()


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    bot.run(token)
