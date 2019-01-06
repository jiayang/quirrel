from discord.ext import commands
from discord import opus
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import discord

opus.load_opus('bin/libopus-0.x86.dll')

class Music:

    def __init__(self, bot):
        self.bot = bot
        self.channel = None

    @commands.command(name='join',)
    async def _join(self,ctx):
        '''Join the voice channel'''
        if ctx.author.voice.channel != None and ctx.author.voice.channel.guild == ctx.guild:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send('Not in a voice channel')
        await ctx.message.delete()

    @commands.command(name='leave',)
    async def _leave(self,ctx):
        '''Leaves the voice channel'''
        clients = self.bot.voice_clients
        for client in clients:
            if client.guild == ctx.guild:
                await client.disconnect()
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Music(bot))
