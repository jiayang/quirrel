from random import randint,choice

from discord.ext import commands
import discord

DIGITS = ['1⃣','2⃣','3⃣','4⃣','5⃣','6⃣','7⃣','8⃣','9⃣','0⃣']

class Random:

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

    @commands.command(name='roll')
    async def _roll(self,ctx):
        '''Rolls a dice'''
        a = randint(0,5)
        await ctx.send(f'I rolled a **{a}!**')
        await ctx.message.delete()

    @commands.command(name='random')
    async def _random(self,ctx, *args):
        '''Randomly selects one of the choices. !random {choice1} {choice2} ...'''
        if len(args) == 0:
            await ctx.send("There's nothing to pick!")
        else:
            a = choice(args)
            await ctx.send(f'After long contemplation, I pick... **{a}!**')


def setup(bot):
    bot.add_cog(Random(bot))
