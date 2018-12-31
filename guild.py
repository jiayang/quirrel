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

    @commands.command(name='clear',)
    async def _clear(self,ctx, *args):
        '''Clears messages, max 50. You can specify a user.'''
        await ctx.message.delete()
        msgs_to_delete = []
        amount = 10
        for arg in args:
            if arg.isdigit():
                amount = int(arg)
                if amount > 50:
                    await ctx.send('The limit is 50 messages. Why would you need more?')
                    return
                break
        del_users = set()
        for arg in args:
            if arg.strip('<@!>').isdigit():
                usr = self.bot.get_user(int(arg.strip('<@!>')))
            else:
                usr = None
            if usr != None:
                nd = 0
                async for msg in ctx.history(limit=200):
                    if nd == amount:
                        break
                    if msg.author == usr:
                        msgs_to_delete.append(msg)
                        nd += 1
                del_users.add(usr)
        if len(del_users) == 0:
            nd = 0
            async for msg in ctx.history(limit=200):
                if nd == amount:
                    break
                msgs_to_delete.append(msg)
                nd += 1
        for msg_group in [msgs_to_delete[i:i + 100] for i in range(0, len(msgs_to_delete), 100)]:
            await ctx.channel.delete_messages(set(msg_group))
        await ctx.send('_Woosh_ what {} messages were you talking about?'.format(amount))
def setup(bot):
    bot.add_cog(Guild(bot))
