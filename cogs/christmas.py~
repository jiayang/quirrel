import random
import os

import asyncio
from discord.ext import commands
from discord import opus
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import discord




OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']
def load_opus_lib():
    if opus.is_loaded():
        return True

    for opus_lib in OPUS_LIBS:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass


if not discord.opus.is_loaded():
    load_opus_lib()

    

class Christmas(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.songs = os.listdir('christmassongs')
#        print('\n'.join(self.songs))
        self.last_played = None
        self.vc = None
        self.channel = None
        self.stop = True
        self.i = 0
        
    async def get_voice_client(self,guild):
        '''Gets the voice client for the specified guild'''
        clients = self.bot.voice_clients
        for client in clients:
            if client.guild == guild:
                return client
        return None

    @commands.command(name="dothething",hidden=True)
    async def _play(self, ctx):
        '''Loop the christmas music'''
        guild = ctx.guild #==============================================<====== change to self.bot.get_guild(166995343249113088)
        voice = await self.get_voice_client(guild)
        await ctx.message.delete()
        self.stop = False
        #If there is no voice client in the specified guild
        if voice == None:
            #Connect to the channel of the sender if possible
            self.channel = ctx.author.voice.channel
            voice = await self.channel.connect()
        self.vc = voice
        await self.next()

    async def next(self):
        to_play = self.songs[self.i]
        self.last_played = to_play
        self.i += 1
        if self.i == len(self.songs):
            random.shuffle(self.songs)
            while self.songs[0] == self.last_played:
                random.shuffle(self.songs)
            self.i = 0
        if self.stop:
            return
        if not self.vc.is_connected():
            self.vc = await self.channel.connect()
        print(f'Now playing {to_play}')
        self.vc.play(discord.FFmpegPCMAudio('christmassongs/' + to_play), after=self.after)

    def after(self,e):
        print('Ended')
        asyncio.run_coroutine_threadsafe(asyncio.sleep(50), self.vc.loop)
        asyncio.run_coroutine_threadsafe(self.next(), self.vc.loop)

    @commands.command(name="stopthething",hidden=True)
    async def _stop(self,ctx):
        '''Stop the thing'''
        self.stop = True
        await self.vc.disconnect()






def setup(bot):
    bot.add_cog(Christmas(bot))
