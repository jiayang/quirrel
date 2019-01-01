from discord.ext import commands
import discord

from util import SurveyBuilder

async def prompt(ctx,q,garbage):
    '''Helper to prompt user, returns response'''
    def check(message):
        return message.author == ctx.author
    sent = await ctx.send(q)
    response = await ctx.bot.wait_for('message', check=check, timeout = 120)
    garbage.append(sent)
    garbage.append(response)
    return response
