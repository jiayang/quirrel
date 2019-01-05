from discord.ext import commands
import discord

class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx, module : str, pull = ''):
        """Reloads a module."""
        if pull == '-p':
            g = git.cmd.Git('.')
            g.pull()
            print('Pulled from git')
            await ctx.send('Successfully pulled from git')
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            print('SUCCESSFULLY RELOADED: ' + module)
            await ctx.send(('SUCCESSFULLY RELOADED: ' + module))

            @commands.command(name='load',hidden=True)
            async def _load(self, ctx, module : str, pull = ''):
                """Loads a module."""
                if pull == '-p':
                    g = git.cmd.Git('.')
                    g.pull()
                    print('Pulled from git')
                    await ctx.send('Successfully pulled from git')
                try:
                    bot.load_extension(module)
                except Exception as e:
                    print('{}: {}'.format(type(e).__name__, e))
                    await ctx.send('{}: {}'.format(type(e).__name__, e))
                else:
                    print('SUCCESSFULLY LOADED: ' + module)
                    await ctx.send('SUCCESSFULLY LOADED: ' + module)

def setup(bot):
    bot.add_cog(Admin(bot))
