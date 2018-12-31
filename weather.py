from discord.ext import commands
import urllib
import datetime
import json

from util import location

ICONS = dict()
ICONS['clear-day'] = '☀'
ICONS['clear-night'] = '🌛'
ICONS['cloudy'] = '☁'
ICONS['rain'] = '🌧'
ICONS['snow'] = '🌨'
ICONS['sleet'] = '🌧'
ICONS['wind'] = '🌥'
ICONS['fog'] = '☁'
ICONS['partly-cloudy-day'] = '🌥'
ICONS['partly-cloudy-night'] = '🌖'

WEATHER_API = "https://api.darksky.net/forecast/{}/{},{}"
with open('secret/keys.json') as keys:
    api_keys = json.loads(keys.read())
DSKY_KEY = api_keys['dark_sky']

class Weather:
    def __init__(self, bot):
        self.bot = bot

        self.loc_cache = {}

    @commands.command(name='weather')
    async def _weather(self,ctx, *args):
        '''To show the weather of a given location. !weather {location}'''
        try:
            coords = location.get_coordinates(args)
            loc_name = location.get_name(args)
            now = datetime.datetime.now()
            if (loc_name not in self.loc_cache) or (self.loc_cache[loc_name][0] != now.hour or abs(self.loc_cache[loc_name][1] - now.minute) > 10):
                weather = json.loads(urllib.request.urlopen(WEATHER_API.format(DSKY_KEY, coords[0], coords[1])).read())
                self.loc_cache[loc_name] = (now.hour,now.minute,weather['currently'])
                print('CALLED API: DARKSKY')
                data = self.loc_cache[loc_name][2]
                await ctx.send(await Weather.format(data,loc_name,now))
                await ctx.message.delete()
        except:
            await ctx.send('Error: Please provide a correct location. Usage: !weather {location}')
    async def format(data,loc_name,time):
        return "**{} at {}**\n**{}°F | {}°C\n**{} {}".format(loc_name,
                                                                time.strftime("%I:%M %p"),
                                                                int(round(float(data['temperature']))),
                                                                int(round(float(await Weather.f_to_c(data['temperature'])))),
                                                                ICONS[data['icon']],
                                                                data['summary'])

    async def f_to_c(n):
        return str((float(n)- 32) * 5. / 9)
def setup(bot):
    bot.add_cog(Weather(bot))
