import discord
from discord.ext import commands

startup_extensions=['guild','survey','upburst','weather'] # Discontinued: basketball
bot = commands.Bot(command_prefix='!')
token = open('secret/token.txt','r').read().strip()


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

#For debug
'''@bot.event
async def on_reaction_add(reaction,user):
    print(reaction.emoji)
    print(reaction.emoji.id)'''
    
@bot.command(name='reload', hidden=True)
async def _reload(ctx, module : str):
    """Reloads a module."""
    try:
        bot.unload_extension(module)
        bot.load_extension(module)
    except Exception as e:
        print('{}: {}'.format(type(e).__name__, e))
    else:
        print('SUCCESSFULLY RELOADED: ' + module)

@bot.command(name='load',hidden=True)
async def _load(ctx, module : str):
    """Loads a module."""
    try:
        bot.load_extension(module)
    except Exception as e:
        print('{}: {}'.format(type(e).__name__, e))
    else:
        print('SUCCESSFULLY LOADED: ' + module)



if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    bot.run(token)
