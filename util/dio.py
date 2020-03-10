from discord.ext import commands
import discord
import asyncio

from util import SurveyBuilder

async def prompt(ctx,q,garbage):
    '''Helper to prompt user, returns response'''
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    sent = await ctx.send(q)
    response = await ctx.bot.wait_for('message', check=check, timeout = 120)
    garbage.append(sent)
    garbage.append(response)
    return response

async def prompt_timeout(ctx,q,garbage,time):
    '''Prompt user but specify a timeout'''
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    sent = await ctx.send(q)
    try:
        response = await ctx.bot.wait_for('message', check=check, timeout = time)
        garbage.append(response)
    except asyncio.TimeoutError:
        response = None
    garbage.append(sent)
    return response
    
