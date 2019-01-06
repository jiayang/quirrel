from discord.ext import commands
import discord

import asyncio

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
        '''Clears messages. You can specify a user.'''
        await ctx.message.delete()
        msgs_to_delete = []
        amount = 10
        #If the args contain an int, use that to specify of amount of msgs to delete
        for arg in args:
            if arg.isdigit():
                amount = int(arg)
                break
        del_users = set()
        #Delete msgs from specific user
        for arg in args:
            if arg.strip('<@!>').isdigit():
                usr = self.bot.get_user(int(arg.strip('<@!>')))
            else:
                usr = None
            if usr != None:
                nd = 0
                async for msg in ctx.history(limit=200):
                    #If number of deleted hits the amount wanted
                    if nd == amount:
                        break
                    if msg.author == usr:
                        msgs_to_delete.append(msg)
                        nd += 1
                del_users.add(usr)
        #If no user is specified, delete last msgs from anyone
        if len(del_users) == 0:
            nd = 0
            async for msg in ctx.history(limit=200):
                if nd == amount:
                    break
                msgs_to_delete.append(msg)
                nd += 1
        for msg_group in [msgs_to_delete[i:i + 100] for i in range(0, len(msgs_to_delete), 100)]:
            await ctx.channel.delete_messages(set(msg_group))
        a = await ctx.send('_Woosh_ what {} messages were you talking about?'.format(amount))
        await asyncio.sleep(2)
        await a.delete()

    @commands.command(name='me')
    async def _me(self, ctx):
        user = ctx.message.author
        embed = discord.Embed(title=f"**{user.display_name}**", colour=discord.Colour(0xd19bf1), description=user.name + "#" + str(user.discriminator))
        embed.add_field(name='User id:', value=str(user.id))
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.set_footer(text=f'User created at {ctx.message.author.created_at}')

        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Guild(bot))
