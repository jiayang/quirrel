from discord.ext import commands
import discord
import asyncio

SUPERUSERS = {178663053171228674: "blue", 166636618701209600: "blue", 172920250432487425: "red", 204363647370264586: "red", 218801604147544075: "blue", 198561020787032064: "red", 219937777096196097: "blue", 155861732550639617: "red", 208353857992916992: "red"} #gameboytre, jt, gren, skate, apple, cryp, irre, res, sound
class Rejoin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        if (guild.id == 166995343249113088):
            if (member.id in SUPERUSERS):
                channel = guild.get_channel(556513668125163538)
                invite = await channel.create_invite(max_uses = 1)
                user = self.bot.get_user(member.id)
                if user in await guild.bans():
                    await guild.unban(user)
                    await user.send(content="Hello! I don't know why you got **banned**, but if you ever want to rejoin, here you go!")
                else:
                    await user.send(content="Hello! I don't know why you got **kicked** or **left**, but if you ever want to rejoin, here you go!")
                await user.send(content=invite)
            
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if (guild.id == 166995343249113088):
            if (member.id in SUPERUSERS):
                esteemedmember = guild.get_role(322834336976207872)
                innerrole = None
                if (SUPERUSERS[member.id] == 'blue'):
                    innerrole = guild.get_role(554522751231197205)
                if (SUPERUSERS[member.id] == 'red'):
                    innerrole = guild.get_role(554514491384135680)
                await member.edit(roles = [esteemedmember, innerrole])
    
        
        
def setup(bot):
    bot.add_cog(Rejoin(bot))
