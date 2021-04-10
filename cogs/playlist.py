import os
import string
import random
import shutil
import asyncio

from discord.ext import commands
import discord
import youtube_dl
    
class Playlist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.client = discord.Client()

        
    @commands.command(name="download")
    async def _download(self,ctx,link):
        '''Download a youtube playlist or video into a zip of mp3s'''
        print("Downloading playlist requested by " + ctx.author.display_name)
        #Fetch info
        opts = {"quiet": True, "no_warnings": True}
        try:
            with youtube_dl.YoutubeDL(opts) as ydl:
                data = ydl.extract_info(link,download=False,process=False)
        except:
            ctx.send("Please provide a valid link of a non-private YouTube playlist or video")
            return
        if 'entries' in data:
            videos = list(data['entries'])
        else:
            videos = [data]
        length = len(videos)

            
        file_id = ''.join(random.choice(string.ascii_letters) for i in range(10))
        file_loc = '/home/jiayang/upload/' + file_id 
        os.mkdir(file_loc)
        msg = await ctx.send('**Downloading playlist**\n' + ":green_circle:" * 0 + ":large_blue_diamond:" + ":purple_circle:" * 10)
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio/best',
            'outtmpl': file_loc + '/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            completed = 0
            for video in videos:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(['https://youtube.com/watch?v=' + video['id']])
                completed += 1
                pct = completed / length
                greens = int(pct * 10)
                purples = 10 - greens
                s = "**Downloading Playlist**\n" + ":green_circle:" * greens + ":large_blue_diamond:" + ":purple_circle:" * purples
                await msg.edit(content=s)
            shutil.make_archive(file_loc, 'zip', file_loc) 
        except Exception as e:
            await ctx.send("There was an error in processing your request. Make sure all the videos in the playlist exist.")
            print(e)
        shutil.rmtree(file_loc)
        await ctx.send(ctx.author.mention + " Compilation is done! Download it here: " + "https://upload.jiayang.dev/?id=" + file_id)
        await ctx.send("The download will be deleted in 5 minutes.")
        await asyncio.sleep(5 * 60)
        os.remove(file_loc + '.zip')
        

    @commands.command(name="download-mp4")
    async def _download_mp4(self,ctx,link):
        '''Download a youtube playlist or video into a zip of mp3s'''
        print("Downloading playlist requested by " + ctx.author.display_name)
        #Fetch info
        opts = {"quiet": True, "no_warnings": True}
        try:
            with youtube_dl.YoutubeDL(opts) as ydl:
                data = ydl.extract_info(link,download=False,process=False)
        except:
            ctx.send("Please provide a valid link of a non-private YouTube playlist or video")
            return
        if 'entries' in data:
            videos = list(data['entries'])
        else:
            videos = [data]
        length = len(videos)

            
        file_id = ''.join(random.choice(string.ascii_letters) for i in range(10))
        file_loc = '/home/jiayang/upload/' + file_id 
        os.mkdir(file_loc)
        msg = await ctx.send('**Downloading playlist**\n' + ":green_circle:" * 0 + ":large_blue_diamond:" + ":purple_circle:" * 10)
        ydl_opts = {
            'quiet': True,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': file_loc + '/%(title)s.%(ext)s'
        }
        try:
            completed = 0
            for video in videos:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(['https://youtube.com/watch?v=' + video['id']])
                completed += 1
                pct = completed / length
                greens = int(pct * 10)
                purples = 10 - greens
                s = "**Downloading Playlist**\n" + ":green_circle:" * greens + ":large_blue_diamond:" + ":purple_circle:" * purples
                await msg.edit(content=s)
            shutil.make_archive(file_loc, 'zip', file_loc) 
        except Exception as e:
            await ctx.send("There was an error in processing your request. Make sure all the videos in the playlist exist.")
            print(e)
        shutil.rmtree(file_loc)
        await ctx.send(ctx.author.mention + " Compilation is done! Download it here: " + "https://upload.jiayang.dev/?id=" + file_id)
        await ctx.send("The download will be deleted in 5 minutes.")
        await asyncio.sleep(5 * 60)
        os.remove(file_loc + '.zip')
def setup(bot):
    bot.add_cog(Playlist(bot))
