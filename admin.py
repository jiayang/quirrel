import os

from discord.ext import commands
import discord
import git
import datetime

DEV_IDS = [184002906981269505,178663053171228674]
class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx, module : str, pull = ''):
        """Reloads a module."""
        if ctx.author.id not in DEV_IDS:
            pass
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
        if ctx.author.id not in DEV_IDS:
            pass
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
        if ctx.author.id not in DEV_IDS:
            pass
        embed = discord.Embed(title='**Servers**', color = 16744272)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        for server in self.bot.guilds:
            embed.add_field(name=server.name,value=str(server.id))
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(name='presence', hidden=True)
    async def _change_presence(self,ctx,*args):
        '''Change the presence of the bot. Usage: !presence [TYPE] [MESSAGE_TO_BE_SHOWN]'''
        types = {
            'playing' : discord.ActivityType.playing,
            'streaming' : discord.ActivityType.streaming,
            'listening' : discord.ActivityType.listening,
            'watching' : discord.ActivityType.watching
        }
        activity = discord.Activity(type=types[arg[0]], name=' '.join(args[1:]))
        await bot.change_presence(activity=activity)

def setup(bot):
    bot.add_cog(Admin(bot))
