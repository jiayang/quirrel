import discord
from discord.ext import commands

startup_extensions=['admin','anime','guild','survey','upburst','weather','music','rand','games','tcg'] # Discontinued: basketball
bot = commands.Bot(command_prefix='!')
token = open('secret/token.txt','r').read().strip()


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
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    bot.run(token)
