from discord.ext import commands
import discord

class Test:

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='test',)
    async def _test(self,ctx):
        msg = await ctx.send('wow')
        await ctx.message.delete()    
        
        
def setup(bot):
    bot.add_cog(Test(bot))
