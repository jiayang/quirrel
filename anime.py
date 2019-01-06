import json
from urllib.request import urlopen

from discord.ext import commands
import discord

import asyncio



SEARCH_URL = 'https://api.jikan.moe/v3/search/anime?q='
ANIME_URL = 'https://api.jikan.moe/v3/anime/'

class Anime:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='anime')
    async def _anime(self, ctx, *args):
        '''Get anime info from name. Usage: !anime <anime_name>'''
        try:
            query = "%20".join(args);
            search_res = json.loads(urlopen(SEARCH_URL + query).read())
            anime_res = json.loads(urlopen(ANIME_URL + str(search_res['results'][0]['mal_id'])).read())

            embed = discord.Embed(title=f"**{anime_res['title']}**", colour=discord.Colour(0xd19bf1), description=f"[MAL Link]({anime_res['url']})\n" + anime_res['synopsis'].replace('(', "\n\n("))
            embed.set_thumbnail(url=anime_res['image_url'])
            embed.add_field(name="**Type**", value=anime_res['type'], inline=True)
            embed.add_field(name="**Episodes**", value=str(anime_res['episodes']), inline=True)
            embed.add_field(name="**Score**", value=str(anime_res['score']), inline=True)
            embed.add_field(name="**Status**", value=anime_res['status'], inline=True)


            await ctx.send(embed = embed)

        except:
            await ctx.send('API error, try again')

def setup(bot):
    bot.add_cog(Anime(bot))