from discord.ext import commands
from discord import opus
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import discord
import youtube_dl

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
        self.channel = None

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
        client = self.get_voice_client(ctx.guild)
        if client != None:
            await client.disconnect()
        await ctx.message.delete()

    @commands.command(name='play',)
    async def _play(self,ctx):
        url = (ctx.message.content.split(' ')[1]
        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'songs/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            download_target = ydl.prepare_filename(info)
            ydl.download([url])
        await voice.play(discord.FFmpegPCMAudio(download_target))
        await ctx.message.delete()
if 'entries' in result:
    # Can be a playlist or a list of videos
    video = result['entries'][0]
else:
    # Just a video
    video = result
def setup(bot):
    bot.add_cog(Music(bot))
