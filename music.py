import asyncio
from discord.ext import commands
from discord import opus
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import discord

from util import yt_search

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

    @commands.command(name='leave', aliases = ['stop'])
    async def _leave(self,ctx):
        '''Leaves the voice channel'''
        client = await self.get_voice_client(ctx.guild)
        if client != None:
            await client.disconnect()
            if client in self.queues:
                self.queues[client].clear()
        await ctx.message.delete()

    @commands.command(name='play',)
    async def _play(self,ctx):
        '''Plays the song given the url from YouTube OR a search query'''
        voice = await self.get_voice_client(ctx.guild)
        await ctx.message.delete()
        #If there is no voice client in the specified guild
        if voice == None:
            if ctx.author.voice == None:
                await ctx.send('Not in a voice channel!')
                return
            #Connect to the channel of the sender if possible
            voice = await ctx.author.voice.channel.connect()

        #Downloads the song's info
        data = yt_search.download_info(ctx.message)

        #Could not download the info for some reason
        if data == None:
            await ctx.send('Sorry, I could not find that video. Proper usage: _!play search query here_  **OR**  _!play LINK_')
            return

        #If the playlist exists for the selected server, just add the song to the playlist
        if voice not in self.queues:
            self.queues[voice] = Playlist(self, voice)
        self.queues[voice].add(data['entries'][0])

        embed = discord.Embed(title=f"Queued **{data['title']}**", color = 16744272)
        embed.set_author(name=self.bot.user.name, icon_url = self.bot.user.avatar_url)
        embed.description = f"[Link]({data['link']})"
        embed.set_thumbnail(url=data['thumbnail'])
        await ctx.send(embed=embed)

        #If the player is not playing already, initiate the process
        if not voice.is_playing():
            await self.queues[voice].play()

        for entry in data['entries'][1:]:
            self.queues[voice].add(entry)

    @commands.command(name='skip',)
    async def _skip(self,ctx):
        '''Skips the current playing song'''
        voice = await self.get_voice_client(ctx.guild)
        await ctx.message.delete()

        if voice == None or not voice.is_playing():
            await ctx.send('There is nothing to skip!')
            return

        await self.queues[voice].skip(ctx)

    @commands.command(name='queue',)
    async def _queue(self,ctx):
        '''Displays the current queue'''
        voice = await self.get_voice_client(ctx.guild)
        await ctx.message.delete()
        if voice == None:
            await ctx.send('I am not connected to the server!')
            return

        playlist = self.queues[voice]

        if len(playlist.queue) == 0 and not playlist.vc.is_playing():
            await ctx.send('There is nothing in the queue')
            return

        #Format the embed for FANCY return
        s = ''
        for i in range(len(playlist.queue)):
            s += f"{i+1}. {playlist.queue[i]['title']}\n"
        embed = discord.Embed(title=f"Current Queue For **{ctx.guild.name}**", color = 16744272)
        if playlist.vc.is_playing():
            embed.add_field(name='**Now Playing**', value=playlist.now_playing)
        if s != '':
            embed.add_field(name='**Next**', value=s)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

class Playlist:

    def __init__(self,bot,voice):
        self.vc = voice
        self.loop = self.vc.loop
        self.bot = bot
        self.clear()

    #Adds the song's data to the queue, downloads the song if there are less than 5 songs left in the queue that are already downloaded
    def add(self,data):
        self.queue += [data]
        if self.last_queued < 4:
            asyncio.run_coroutine_threadsafe(yt_search.download(self.queue[self.last_queued+1]['url']), self.loop)
            self.last_queued += 1

    #Repeatedly play until the queue is out of songs
    async def play(self):
        vc = self.vc

        #Nothing left
        if self.last_queued == -1:
            asyncio.run_coroutine_threadsafe(asyncio.sleep(15), self.loop)
            asyncio.run_coroutine_threadsafe(vc.disconnect(), self.loop)
            self.clear()
            return

        data = self.queue.pop(0)
        self.last_queued -= 1
        targ = data['target']
        self.now_playing = data['title']
        vc.play(discord.FFmpegPCMAudio(targ),
                    after= self.after)

        #If there are songs left to queue and not all the spots have already been taken, queue the song
        if self.last_queued < 4 and len(self.queue) > self.last_queued + 1:
            yt_search.download(self.queue[self.last_queued+1]['url'])
            self.last_queued += 1

    #Wait a few ms before playing the next song - prevents abrupt transitions
    def after(self,e):
        asyncio.run_coroutine_threadsafe(asyncio.sleep(20), self.loop)
        asyncio.run_coroutine_threadsafe(self.play(), self.loop)

    #Clears everything for future use
    def clear(self):
        self.queue = []
        self.now_playing = ''
        self.last_queued = -1

    #Skips the currently playing by just calling stop
    async def skip(self,ctx):
        await ctx.send(f'Skipped: **{self.now_playing}**')

        #Stop triggers the 'after' function which plays the next song
        self.vc.stop()

def setup(bot):
    bot.add_cog(Music(bot))
