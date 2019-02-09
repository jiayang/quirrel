import urllib
import json
from pathlib import Path

import youtube_dl

#Setup
YT_API = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={}&key={}"
with open('secret/keys.json') as keys:
    api_keys = json.loads(keys.read())
YT_KEY = api_keys['youtube']
YT_VIDEO_BASE = 'https://www.youtube.com/watch?v={}'
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': 'songs/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
}

#Searches for the url
def get_url(message):
    url = ' '.join(message.content.split(' ')[1:])
    if 'youtube.com' not in url:
        url = search(url)
    return url

#Download the info only
def download_info(message):
    url = get_url(message)
    if url == None:
        return None
    try:
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            download_target = ydl.prepare_filename(info)
            #Setup file name
            targ = download_target.split('.')
            targ[-1] = 'wav'
            targ = '.'.join(targ)
    except:
        return None

    #Format the data
    data = {}
    data['target'] = targ
    data['title'] = info['title']
    data['link'] = info['url']
    data['thumbnail'] = info['thumbnails'][0]['url']
    data['url'] = url

    return data

def download(url):
    '''Downloads the video specified by the URL'''
    #Search could not find anything
    if url == None:
        return None
    #Downloads the video with the url
    try:
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            download_target = ydl.prepare_filename(info)

            #Setup file name
            targ = download_target.split('.')
            targ[-1] = 'wav'
            targ = '.'.join(targ)
            config = Path(targ)

            #Only download if it doesn't already exist
            if not config.is_file():
                ydl.download([url])
    except:
        return None

def search(query):
    '''Searches for the query, returns the complete link to the video'''
    search_url = YT_API.format(query.replace(' ','+'),YT_KEY)
    results = json.loads(urllib.request.urlopen(search_url).read())
    if len(results['items']) == 0:
        return None
    return YT_VIDEO_BASE.format(results['items'][0]['id']['videoId'])
