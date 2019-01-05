import datetime

from discord.ext import commands
import discord

from util import dio

MAPS = {
    'valley' : 'Hidden Valley',
    'peaks' : 'Twin Peaks EXTREME',
    'pyramid' : 'Pyramid Remastered',
    'ama' : 'Amazon'
}
UPBURST_EMOJI = '<:upburst:451133832217755659>'


class Upburst:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roster',hidden=True)
    async def _roster_check(self,ctx):
        #if ctx.guild.id != 166995343249113088:
        #    return
        garbage = []
        num = await dio.prompt(ctx,'**Official Roster Check No.?**',garbage)
        when = await dio.prompt(ctx,'**When?:**',garbage)
        time = datetime.datetime.now().strftime('%m/%d/%Y')
        role = discord.utils.get(ctx.guild.roles, name='Esteemed Member')
        role_tag = ''
        if role != None:
            role_tag = role.mention
        await ctx.send(f'**Official Roster Check #{num.content}**             {role_tag}\n_{time}_\n\n_Please react with your corresponding ICON if you can make this AWESOME Scrimmage at {when.content}_')
        await ctx.channel.delete_messages(garbage)

    @commands.command(name='schedule',hidden=True)
    async def _schedule(self,ctx):
        #if ctx.guild.id != 166995343249113088:
        #    return
        garbage = [ctx.message]
        num = await dio.prompt(ctx,'**Week No.?**',garbage)
        maps = await dio.prompt(ctx,'**List off the maps being played during this battle** \nSeparate with spaces. Known nicknames: valley, peaks, pyramid',garbage)
        time = datetime.datetime.now().strftime('%m/%d/%Y')
        names = maps.content.split(' ')
        names = ', '.join([MAPS[i] if i in MAPS else i.capitalize() for i in names])
        when = await dio.prompt(ctx,'**When?:**',garbage)
        opponent = await dio.prompt(ctx,'**Who are our enemies?:**',garbage)
        role = discord.utils.get(ctx.guild.roles, name='Esteemed Member')
        role_tag = ''
        if role != None:
            role_tag = role.mention
        eu = await dio.prompt(ctx,'**Are they from the European continent?** (y/n)',garbage)
        while eu.content != 'y' and eu.content != 'n':
            eu = await dio.prompt(ctx,'**Are they European continent?** (y/n)',garbage)
        region = 'US'
        if eu.content == 'y':
            region += '/EU'
        mow = await dio.prompt(ctx,'**What is the message of the week?** (.none for none)',garbage)
        s = '**Message of the week:** '+mow.content
        if mow.content == '.none':
            s = ''
        await ctx.send(f'{UPBURST_EMOJI}**Upburst Wyverns Week #{num.content}**{UPBURST_EMOJI}            {role_tag}\n_{time}_\n\n**Maps** : {names}\n**Time** : {when.content}\n**Teams** : Upburst / {opponent.content}\n**Region** : {region}\n{s}')
        await ctx.channel.delete_messages(garbage)






def setup(bot):
    bot.add_cog(Upburst(bot))



#          _____                    _____                    _____                    _____                _____                    _____                    _____                    _____                    _____
#         /\    \                  /\    \                  /\    \                  /\    \              /\    \                  /\    \                  /\    \                  /\    \                  /\    \
#        /::\    \                /::\    \                /::\    \                /::\    \            /::\    \                /::\____\                /::\    \                /::\    \                /::\    \
#       /::::\    \              /::::\    \              /::::\    \              /::::\    \           \:::\    \              /::::|   |               /::::\    \              /::::\    \              /::::\    \
#      /::::::\    \            /::::::\    \            /::::::\    \            /::::::\    \           \:::\    \            /:::::|   |              /::::::\    \            /::::::\    \            /::::::\    \
#     /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \           \:::\    \          /::::::|   |             /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \
#    /:::/  \:::\    \        /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \           \:::\    \        /:::/|::|   |            /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \
#   /:::/    \:::\    \      /::::\   \:::\    \      /::::\   \:::\    \      /::::\   \:::\    \          /::::\    \      /:::/ |::|   |           /::::\   \:::\    \       \:::\   \:::\    \       \:::\   \:::\    \
#  /:::/    / \:::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \        /::::::\    \    /:::/  |::|   | _____    /::::::\   \:::\    \    ___\:::\   \:::\    \    ___\:::\   \:::\    \
# /:::/    /   \:::\ ___\  /:::/\:::\   \:::\____\  /:::/\:::\   \:::\    \  /:::/\:::\   \:::\    \      /:::/\:::\    \  /:::/   |::|   |/\    \  /:::/\:::\   \:::\    \  /\   \:::\   \:::\    \  /\   \:::\   \:::\    \
#/:::/____/  ___\:::|    |/:::/  \:::\   \:::|    |/:::/__\:::\   \:::\____\/:::/  \:::\   \:::\____\    /:::/  \:::\____\/:: /    |::|   /::\____\/:::/__\:::\   \:::\____\/::\   \:::\   \:::\____\/::\   \:::\   \:::\____\
#\:::\    \ /\  /:::|____|\::/   |::::\  /:::|____|\:::\   \:::\   \::/    /\::/    \:::\  /:::/    /   /:::/    \::/    /\::/    /|::|  /:::/    /\:::\   \:::\   \::/    /\:::\   \:::\   \::/    /\:::\   \:::\   \::/    /
# \:::\    /::\ \::/    /  \/____|:::::\/:::/    /  \:::\   \:::\   \/____/  \/____/ \:::\/:::/    /   /:::/    / \/____/  \/____/ |::| /:::/    /  \:::\   \:::\   \/____/  \:::\   \:::\   \/____/  \:::\   \:::\   \/____/
#  \:::\   \:::\ \/____/         |:::::::::/    /    \:::\   \:::\    \               \::::::/    /   /:::/    /                   |::|/:::/    /    \:::\   \:::\    \       \:::\   \:::\    \       \:::\   \:::\    \
#   \:::\   \:::\____\           |::|\::::/    /      \:::\   \:::\____\               \::::/    /   /:::/    /                    |::::::/    /      \:::\   \:::\____\       \:::\   \:::\____\       \:::\   \:::\____\
#    \:::\  /:::/    /           |::| \::/____/        \:::\   \::/    /               /:::/    /    \::/    /                     |:::::/    /        \:::\   \::/    /        \:::\  /:::/    /        \:::\  /:::/    /
#     \:::\/:::/    /            |::|  ~|               \:::\   \/____/               /:::/    /      \/____/                      |::::/    /          \:::\   \/____/          \:::\/:::/    /          \:::\/:::/    /
#      \::::::/    /             |::|   |                \:::\    \                  /:::/    /                                    /:::/    /            \:::\    \               \::::::/    /            \::::::/    /
#       \::::/    /              \::|   |                 \:::\____\                /:::/    /                                    /:::/    /              \:::\____\               \::::/    /              \::::/    /
#        \::/____/                \:|   |                  \::/    /                \::/    /                                     \::/    /                \::/    /                \::/    /                \::/    /
#                                  \|___|                   \/____/                  \/____/                                       \/____/                  \/____/                  \/____/                  \/____/
#
