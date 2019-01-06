from discord.ext import commands
import discord
import git

import datetime

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
            repo = git.Repo(os.getcwd())
            await ctx.send(f'{master.commit.author.name}: {master.commit.message}')
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
            self.bot.load_extension(module)
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            print('SUCCESSFULLY LOADED: ' + module)
            await ctx.send('SUCCESSFULLY LOADED: ' + module)

    @commands.command(name='servers', hidden=True)
    async def _servers(self, ctx):
        '''Lists all the servers the bot is a part of'''
        embed = discord.Embed(title='**Servers**', color = 16744272)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        for server in self.bot.guilds:
            embed.add_field(name=server.name,value=str(server.id))
        await ctx.send(embed=embed)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Admin(bot))
