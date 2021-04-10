import os

import urllib
import datetime
import json
from pytz import timezone
from discord.ext import commands
import discord

from util import location

ICONS = dict()
ICONS['clear-day'] = ('☀','https://imgur.com/nO5G8mJ.png')
ICONS['clear-night'] = ('🌛','https://imgur.com/snxDP2E.png')
ICONS['cloudy'] = ('☁','https://imgur.com/2DYiPx2.png')
ICONS['rain'] = ('🌧','https://imgur.com/E38juQg.png')
ICONS['snow'] = ('🌨','https://imgur.com/z1AcY1H.png')
ICONS['sleet'] = ('🌧','https://imgur.com/z1AcY1H.png')
ICONS['wind'] = ('🌥','https://imgur.com/YIAX7wm.png')
ICONS['fog'] = ('☁','https://imgur.com/2DYiPx2.png')
ICONS['partly-cloudy-day'] = ('🌥','https://imgur.com/2DYiPx2.png')
ICONS['partly-cloudy-night'] = ('🌖','https://imgur.com/snxDP2E.png')

WEATHER_API = "https://api.darksky.net/forecast/{}/{},{}"
DSKY_KEY = os.getenv("DARKSKY_API_KEY")

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.loc_cache = {}

    @commands.command(name='weather')
    async def _weather(self,ctx, *args):
        '''To show the weather of a given location. !weather {location}'''
        try:
            coords = location.get_coordinates(args)
            loc_name = location.get_name(args)
            now = datetime.datetime.now(timezone('EST'))
            if (loc_name not in self.loc_cache) or (self.loc_cache[loc_name][0] != now.hour or abs(self.loc_cache[loc_name][1] - now.minute) > 10):
                weather = json.loads(urllib.request.urlopen(WEATHER_API.format(DSKY_KEY, coords[0], coords[1])).read())
                self.loc_cache[loc_name] = (now.hour,now.minute,weather['currently'])
                print('CALLED API: DARKSKY')
            data = self.loc_cache[loc_name][2]
            await ctx.send(embed = await Weather.format(data,loc_name,now,ctx))
            await ctx.message.delete()
        except Exception as e:
            await ctx.send('Error: Please provide a correct location. Usage: !weather {location}')
            print(e)

    async def format(data,loc_name,time,ctx):
        embed = discord.Embed(title="**{} at {}**".format(loc_name,time.strftime("%I:%M %p")), color = 16744272)
        embed.set_author(name=ctx.author.name)
        embed.set_thumbnail(url=ICONS[data['icon']][1])
        embed.description='**{}°F | {}°C\n**{} {}'.format(int(round(float(data['temperature']))),
                                                        int(round(float(await Weather.f_to_c(data['temperature'])))),
                                                        ICONS[data['icon']][0],
                                                        data['summary'])
        return embed

    async def f_to_c(n):
        return str((float(n)- 32) * 5. / 9)

    def setup(bot):
    bot.add_cog(Weather(bot))
