'''
I am discontinuing this module because it only works locally. stats.nba.com blocks API calls from DO and AWS :(
'''


from discord.ext import commands
import discord
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players,teams

from util import dio

class Basketball:

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='stats')
    async def _stats(self,ctx, *args):
        '''Retrieves the stats of an NBA player'''
        garbage = [ctx.message]
        bplayers = players.find_players_by_full_name(' '.join(args))
        if len(bplayers) == 0:
            await ctx.channel.delete_messages(garbage)
            s = ' '.join([i.capitalize() for i in args])
            await ctx.send('**Player not found**: ' + s)
            return
        #If there are many players returned from the search
        if len(bplayers) != 1:
            player = None
            list = '\n'.join([f'{i+1}. {bplayers[i]["full_name"]}' for i in range(len(bplayers))])
            while player == None:
                num = await dio.prompt(ctx,f'**Please select one of the following players. Type the number of the desired player**\n{list}',garbage)
                if num.content.isdigit() and int(num.content) > 0 and int(num.content) <= len(bplayers):
                    player = bplayers[int(num.content)-1]
        else:
            player = bplayers[0]
        id = player['id']
        stats = playercareerstats.PlayerCareerStats(player_id=id).career_totals_regular_season.get_dict()['data'][0]
        # Retrieve data, format into an embed
        name = player['full_name']
        games_played = stats[3]
        min_played = round(float(stats[5]))
        fgm = stats[6]
        fga = stats[7]
        points = float(stats[23])/float(games_played)
        rebounds = float(stats[17])/float(games_played)
        assists = float(stats[18])/float(games_played)
        pct = '{:.1%}'.format(float(fgm)/float(fga))
        embed = discord.Embed(title = f'**{name}**', color = 16744272)
        embed.add_field(name='Games Played', value = games_played)
        embed.add_field(name='Total Minutes Played', value = min_played)
        embed.add_field(name='Pts/Reb/Ast', value = '{} / {} / {}'.format(round(points,1),round(rebounds,1),round(assists,1)))
        embed.add_field(name='Field Goals Made', value = f'{fgm}/{fga}, {pct}')
        embed.set_thumbnail(url=f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{id}.png')
        await ctx.send(embed=embed)
        await ctx.channel.delete_messages(garbage)









def setup(bot):
    bot.add_cog(Basketball(bot))
