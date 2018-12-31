import json
import urllib

BING_API = 'http://dev.virtualearth.net/REST/v1/Locations?query={}&key={}'
with open('secret/keys.json') as keys:
    api_keys = json.loads(keys.read())
BING_KEY = api_keys['bing_api']



def get_raw_data(loc_args):
    '''This function gets the raw json data based of a search query'''
    url = BING_API.format('+'.join(loc_args),BING_KEY)
    response = urllib.request.urlopen(url)
    print('CALLED API: BING MAPS API')
    return json.loads(response.read())

def get_coordinates(loc_args):
    '''This function gets the coordinates based off a location search (uses the first result)'''
    data = get_raw_data(loc_args)
    return data['resourceSets'][0]['resources'][0]['point']['coordinates']

def get_name(loc_args):
    '''This function gets the name based off a location search (uses the first result)'''
    data = get_raw_data(loc_args)
    return data['resourceSets'][0]['resources'][0]['name']
