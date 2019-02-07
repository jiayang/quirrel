import urllib
import json

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

def download(message):
    '''Downloads the message by first searching for the video if the message is not a link'''
    url = message.content.split(' ')[1]
    if 'youtube.com' not in url:
        url = search(message.content.split(' ')[1])

    #Search could not find anything
    if url == None:
        return None
    #Downloads the video with the url
    try:
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            download_target = ydl.prepare_filename(info)
            ydl.download([url])
    except:
        return None

    #Format the data
    targ = download_target.split('.')
    targ[-1] = 'wav'
    targ = '.'.join(targ)
    data = {}
    data['target'] = targ
    data['title'] = info['title']
    data['link'] = info['url']
    data['thumbnail'] = info['thumbnails'][0]['url']

    return data

def search(query):
    '''Searches for the query, returns the complete link to the video'''
    results = json.loads(urllib.request.urlopen(YT_API.format(YT_KEY, query.replace(' ','+'))).read())
    if len(results['items']) == 0:
        return None
    return YT_VIDEO_BASE.format(results['items'][0]['id']['videoId'])
