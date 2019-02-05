from discord.ext import commands
from discord import opus
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import discord
import youtube_dl

import asyncio

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

class Music:

    def __init__(self, bot):
        self.bot = bot
        self.queues = dict()

    async def get_voice_client(self,guild):
        '''Gets the voice client for the specified guild'''
        clients = self.bot.voice_clients
        for client in clients:
            if client.guild == guild:
                return client
        return None

    @commands.command(name='join',)
    async def _join(self,ctx):
        '''Join the voice channel'''
        voice = ""
        if ctx.author.voice.channel != None and ctx.author.voice.channel.guild == ctx.guild:
            voice = await ctx.author.voice.channel.connect()
        else:
            await ctx.send('Not in a voice channel')
        await ctx.message.delete()

    @commands.command(name='leave',)
    async def _leave(self,ctx):
        '''Leaves the voice channel'''
        client = await self.get_voice_client(ctx.guild)
        if client != None:
            await client.disconnect()
        await ctx.message.delete()

    @commands.command(name='play',)
    async def _play(self,ctx):
        voice = await self.get_voice_client(ctx.guild)
        await ctx.message.delete()
        if voice == None:
            if ctx.author.voice == None:
                await ctx.send('Not in a voice channel!')
                return
            voice = await ctx.author.voice.channel.connect()
        url = ctx.message.content.split(' ')[1]
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'songs/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            download_target = ydl.prepare_filename(info)
            ydl.download([url])
        targ = download_target.split('.')
        targ[-1] = 'wav'
<<<<<<< Updated upstream

        loop = voice.loop
        voice.play(discord.FFmpegPCMAudio('.'.join(targ)),
                    after=lambda e: asyncio.run_coroutine_threadsafe(voice.disconnect(), loop))
=======
        targ = '.'.join(targ)

        if voice not in self.queues:
            self.queues[voice] = Playlist(self, voice)
        self.queues[voice].add(targ)

        if not voice.is_playing():
            await self.queues[voice].play()



class Playlist:

    def __init__(self,bot,voice):
        self.vc = voice
        self.bot = bot
        self.queue = []
        self.is_checking = False

    def add(self,path):
        self.queue += [path]

    async def play(self):
        vc = self.vc
        targ = self.queue.pop(0)
        vc.play(discord.FFmpegPCMAudio(targ),after=self.play)
        if not self.is_checking:
            await self.leave_on_end()

    async def leave_on_end(self):
        self.is_checking = True
        while True:
            if len(self.queue) == 0 and not self.vc.is_playing():
                await self.vc.disconnect()
                return


>>>>>>> Stashed changes

def setup(bot):
    bot.add_cog(Music(bot))
