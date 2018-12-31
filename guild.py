from discord.ext import commands
import discord

class Guild:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='members',)
    async def _members(self,ctx):
        '''Lists the members of the server'''
        members = '\n'.join([f"[{member.display_name}][{member.status}]" for member in ctx.guild.members])
        msg = await ctx.send(f"**Members Of {ctx.guild}**```md\n{members}```")
        await ctx.message.delete()

    @commands.command(name='test')
    async def _test(self,ctx):
        pass
def setup(bot):
    bot.add_cog(Guild(bot))
