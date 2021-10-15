from discord.ext import commands
import discord
import asyncio

SUPERUSERS = {178663053171228674: "blue", #gameboytre
              166636618701209600: "blue", #jt
              738149388995526696: "red", #gren
              172920250432487425: "red", #gren new acc
              204363647370264586: "red", #skate
              218801604147544075: "blue", #apple
              198561020787032064: "red", #cryp
              219937777096196097: "blue", #irre
              155861732550639617: "red", #res
              208353857992916992: "red", #sound
              166573846642688001: "blue", #pyro
              182216076422152193: "blue", #swimming
              166692305783357440: "purple", #wiz
              167121567988318208: "purple" #moisti
}

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
                banned = False
                for ban in await guild.bans():
                    #print(ban)
                    if ban.user.id == member.id:
                        banned = True
                if banned:
                    await guild.unban(user)
                    await user.send(content="Hello! I don't know why you got **banned**, but if you ever want to rejoin, here you go!")
                else:
                    await user.send(content="Hello! I don't know why you got **kicked** or **left**, but if you ever want to rejoin, here you go!")
                    
                await user.send(content=invite)
                f = open("data/leave.txt", 'a')
                f.write(f'Created invite for {member.display_name}. The invite is ' + invite.url + '\n')
                f.close()

    @commands.Cog.listener()
    async def on_member_join(self, member):

        guild = member.guild
        if (guild.id == 166995343249113088):
            if (member.id in SUPERUSERS):
                executive = guild.get_role(322836458371284993)
                esteemedmember = guild.get_role(322834336976207872)
                innerrole = None
                if (SUPERUSERS[member.id] == 'blue'):
                    innerrole = guild.get_role(554522751231197205)
                if (SUPERUSERS[member.id] == 'red'):
                    innerrole = guild.get_role(554514491384135680)
                if (SUPERUSERS[member.id] == 'purple'):
                    innerrole = guild.get_role(554527990999154698)
                await member.edit(roles = [executive, esteemedmember, innerrole])
    
        
        
def setup(bot):
    bot.add_cog(Rejoin(bot))
