from util import dio

from discord.ext import commands
import discord
import asyncio
import requests

class Image(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def fetch(key):
        payload = {
            'uid': 1024,
            'key': key
        }
        r = requests.get('https://img.jiayang.dev/search/', params=payload)
        return r
        
    @commands.command(name='image', aliases=['i'])
    async def _image(self,ctx, *args):
        '''Displays the image from a user-specific library saved'''
        await ctx.send('Heads up! I moved the images so you can now do `;[emote]`')
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
        elif r.status_code == 401:
            await ctx.send('That keyword already exists. Use another')
        else:
            await ctx.send('Successfully added. A list of all emotes can be found using !emotes')
        await ctx.message.delete()

    @commands.command(name='emotes')
    async def _list_links(self, ctx):
        r = requests.get('https://img.jiayang.dev/search/', params={'uid' : 1024})
        if r.status_code != 200:
            await ctx.send('Error: something went wrong')
        else:
            await ctx.send(r.text)

    @commands.command(name='delete')
    async def _delete_emote(self, ctx, *args):
        key = ' '.join(args)
        r = requests.get('https://img.jiayang.dev/delete/', params={'uid': 1024, 'key': key})
        if r.status_code == 403:
            await ctx.send('Error: could not find an emote with key: ' + key)
        else:
            await ctx.send('Sucessfully deleted: ' + key)
        await ctx.message.delete()
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        '''If the message begins with ; , try to use the emote/whatever is associated'''
        if msg.content[0] == ';':
            key = msg.content[1:]
            r = Image.fetch(key)
            if r.status_code == 200:
                await msg.delete()
                await msg.channel.send(r.text)

def setup(bot):
    bot.add_cog(Image(bot))
