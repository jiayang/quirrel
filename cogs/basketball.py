from discord.ext import commands
import discord
import json
from urllib.request import urlopen

from util import dio,matching,basketball_scraper

ALL_PLAYERS = "https://www.balldontlie.io/api/v1/players?page={}&per_page=100"
PLAYER_SEASON_AVG = "https://www.balldontlie.io/api/v1/season_averages?player_ids[]={}"
NBA_OFFICIAL_IDS = "https://raw.githubusercontent.com/bttmly/nba/master/data/players.json"
NBA_CONTRACTS = "https://www.basketball-reference.com/contracts/players.html"

class Basketball(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.players = []
        self.id_map = {}
        self.full_names = {}
        self.official = {}
        self.contracts = basketball_scraper.scrape_all_players_contracts(NBA_CONTRACTS)
        nextpage = 1
        while nextpage is not None:
            search = json.loads(urlopen(ALL_PLAYERS.format(nextpage)).read())
            for entry in search["data"]:
                frist = entry["first_name"]
                lsat = entry["last_name"]
                name = frist + " " + lsat
                self.players.append(name)
                self.players.append(frist)
                self.players.append(lsat)
                self.id_map[name] = entry["id"]
                self.id_map[frist] = entry["id"]
                self.id_map[lsat] = entry["id"]
                self.full_names[entry["id"]] = frist + " " + lsat
            nextpage = search["meta"]["next_page"]
        officials = json.loads(urlopen(NBA_OFFICIAL_IDS).read())
        for entry in officials:
            self.official[entry["firstName"] + " " + entry["lastName"]] = entry["playerId"]
        

    @commands.command(name='stats')
    async def _stats(self,ctx, *args):
        '''Retrieves the stats of an NBA player'''
        garbage = [ctx.message]

        name = " ".join(args)
        name = matching.get_closest(self.players, name)
        id = self.id_map[name]
        name = self.full_names[id]
        
        stats = json.loads(urlopen(PLAYER_SEASON_AVG.format(id)).read())["data"][0]

        min_played = stats["min"]
        fga = stats["fga"]
        fgm = stats["fgm"]
        points = stats["pts"]
        rebounds = stats["reb"]
        assists = stats["ast"]
        steals = stats["stl"]
        blocks = stats["blk"]
        turnovers = stats["turnover"]
        pct = stats["fg_pct"]
        threes = stats["fg3m"]
        threesa = stats["fg3a"]
        threes_pct = stats["fg3_pct"]
        ftm = stats["ftm"]
        fta = stats["fta"]
        ft_pct = stats["ft_pct"]
        
        official_id = None
        if name in self.official:
            official_id = self.official[name]

        embed = discord.Embed(title = f'**{name}**', color = 16744272)
        embed.add_field(name='PTS / REB / AST', value = '{} / {} / {}'.format(round(points,1),round(rebounds,1),round(assists,1)))
        embed.add_field(name='FGM / FGA / FG%', value = '{} / {} / {}%'.format(round(fgm,1),round(fga, 1), round(pct * 100, 1)))
        embed.add_field(name='3PM / 3PA / 3P%', value = '{} / {} / {}%'.format(round(threes,1), round(threesa,1),round(threes_pct * 100, 1)))
        embed.add_field(name='BLK / STL / TO', value = '{} / {} / {}'.format(round(blocks,1), round(steals, 1), round(turnovers, 1)))
        embed.add_field(name='FTM / FTA / FT%', value = '{} / {} / {}%'.format(round(ftm,1), round(fta, 1), round(ft_pct * 100, 1)))
        if official_id is not None:
            embed.set_thumbnail(url=f'https://cdn.nba.com/headshots/nba/latest/1040x760/{official_id}.png')
        await ctx.send(embed=embed)
        await ctx.channel.delete_messages(garbage)




    @commands.command(name='contract')
    async def _contract(self,ctx, *args):
        '''Retrieves the contract of an NBA player''' 
        garbage = [ctx.message]

        name = " ".join(args)
        name = matching.get_closest(self.players, name)
        id = self.id_map[name]
        name = self.full_names[id]

        official_id = None
        if name in self.official:
            official_id = self.official[name]

        contract = self.contracts[name]

        
        embed = discord.Embed(title = f'**{name}**', color = 16744272)
        for i in range(len(contract)):
            embed.add_field(name=self.contracts["METADATA"][i], value = contract[i])

        
        if official_id is not None:
            embed.set_thumbnail(url=f'https://cdn.nba.com/headshots/nba/latest/1040x760/{official_id}.png')
        await ctx.send(embed=embed)
        await ctx.channel.delete_messages(garbage)

def setup(bot):
    bot.add_cog(Basketball(bot))
