from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from lxml import html
import requests

def get_all_teams():
    team_page = requests.get('https://ccl.mpcleague.com/team/')
    tree = html.fromstring(team_page.content)
    teams = tree.xpath('//a[@class="team-name"]/text()')

    return teams


def get_closest_team(name):
    teams = get_all_teams()
    best_team = ''
    best_team_score = 0
    for team in teams:
        rat = fuzz.token_sort_ratio(name, team)
        if rat > best_team_score:
            best_team_score = rat
            best_team = team
    if best_team_score < 0.5:
        return None
    return best_team

def get_team_roster(name):
    team_page = requests.get('https://ccl.mpcleague.com/team/view/'+name.replace(" ","_"))
    tree = html.fromstring(team_page.content)
    teams = tree.xpath('//a[@class="player-name-link"]/text()')
    return teams
