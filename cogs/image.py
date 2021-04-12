from util import dio

from discord.ext import commands
import discord
import asyncio
import requests

class Image(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='image', aliases=['i'])
    async def _image(self,ctx, *args):
        '''Displays the image from a user-specific library saved'''
        if (len(args) == 0):
            await ctx.send('Error, you need to give a keyword that you added with **!a [keyword]**')
        key = " ".join(args)
        payload = {
            'uid': 1024,
            'key': key
        }
        r = requests.get('https://img.jiayang.dev/search/', params=payload)
        if r.status_code == 400:
            await ctx.send('Error, something went wrong. Try again later')
        else:
            await ctx.send(r.text)
        await ctx.message.delete()

    @commands.command(name='add', aliases=['a'])
    async def _add_image(self,ctx, *args):
        '''Add an image into a user's library'''
        if len(args) == 0:
            await ctx.send('Error, to properly use type !add [keyword], then you will be prompted to enter an image')
            return
        key = " ".join(args)
        garbage = []
        try:
            response = await dio.prompt(ctx, "**Enter the image**", garbage)
            await ctx.channel.delete_messages(garbage)
        except:
            await ctx.message.delete()
            return
        link = response.content
        if (link == ""):
            link = response.attachments[0].url
        payload = {'uid': 1024,
                   'key': key,
                   'link': link
                   }
        r = requests.post('https://img.jiayang.dev/add/', params=payload)
        if r.status_code == 400:
            await ctx.send('Error, to properly use type !add [keyword]')
        if r.status_code == 401:
            await ctx.send('That keyword already exists. Use another')
        await ctx.message.delete()
        
def setup(bot):
    bot.add_cog(Image(bot))
