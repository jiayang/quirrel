from random import randint

from discord.ext import commands
import discord

class Rand:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='flip')
    async def _flip(self,ctx):
        '''Flips a coin'''
        a = randint(0,1)
        if a == 1:
            await ctx.send('💙 **Heads!**')
        else:
            await ctx.send('❤ **Tails!**')
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Rand(bot))
