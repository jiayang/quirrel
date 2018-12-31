from discord.ext import commands

class Guild:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='members',)
    async def _members(self,ctx):
        '''Lists the members of the server'''
        members = '\n'.join([f"[{member.display_name}][{member.status}]" for member in ctx.guild.members])
        msg = await ctx.send(f"**Members Of {ctx.guild}**```md\n{members}```")
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Guild(bot))
