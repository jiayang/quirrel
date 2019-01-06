from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import discord

class Music:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join',)
    async def _join(self,ctx):
        '''Join the voice channel'''
        await self.bot.join_voice_channel(ctx.message.author.voice_channel)
        await ctx.message.delete()



def setup(bot):
    bot.add_cog(Music(bot))
