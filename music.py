from discord.ext import commands
from discord import opus
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import discord

OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']
def load_opus_lib():
    if opus.is_loaded():
        return True

    for opus_lib in OPUS_LIBS:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass


if not discord.opus.is_loaded():
    load_opus_lib()

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
