import urllib
import json
from pathlib import Path

import youtube_dl

#Setup
with open('secret/keys.json') as keys:
    api_keys = json.loads(keys.read())

YT_VIDEO_API = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={}&key={}"
YT_PLAYLIST_API = "https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={}&key={}"
YT_PLAYLIST_ITEMS = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&key={}"
YT_PLAYLIST_ITEMS_PAGINATION = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&key={}&pageToken={}"
YT_PLAYLIST_BASE = 'https://www.youtube.com/playlist?list={}'
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
    if 'list=' in url:
        i = url.find('list=')
        pid = url[i + 5: i + 39]
        playlist_url = YT_PLAYLIST_ITEMS.format(pid,YT_KEY)
        playlist = json.loads(urllib.request.urlopen(playlist_url).read())
        urls = [YT_VIDEO_BASE.format(video['snippet']['resourceId']['videoId']) for video in playlist['items']]
        while 'nextPageToken' in playlist:
            playlist_url = YT_PLAYLIST_ITEMS_PAGINATION.format(pid,YT_KEY,playlist['nextPageToken'])
            playlist = json.loads(urllib.request.urlopen(playlist_url).read())
            n_urls = [YT_VIDEO_BASE.format(video['snippet']['resourceId']['videoId']) for video in playlist['items']]
            urls += n_urls
        return urls
    if 'youtube.com' not in url:
        url = search(url)
    return [url]

#Download the info only
def download_info(message):
    urls = get_url(message)
    if urls == None:
        return None

    data = dict()
    data['entries'] = []
    for url in urls:
        print(url)
        try:
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                download_target = ydl.prepare_filename(info)
                #Setup file name
                targ = download_target.split('.')
                targ[-1] = 'wav'
                targ = '.'.join(targ)
        except:
            continue
        #Format the data
        entry = dict()
        entry['target'] = targ
        entry['title'] = info['title']
        entry['link'] = info['url']
        entry['thumbnail'] = info['thumbnails'][0]['url']
        entry['url'] = url
        data['entries'].append(entry)

    if len(data['entries']) == 0:
        return None
    if len(data['entries']) == 1:
        data['title'] = data['entries'][0]['title']
        data['link'] = data['entries'][0]['url']
        data['thumbnail'] = data['entries'][0]['url']
    else:
        url = ' '.join(message.content.split(' ')[1:])
        i = url.find('list=')
        pid = url[i + 5: i + 39]
        playlist_url = YT_PLAYLIST_API.format(pid,YT_KEY)
        playlist = json.loads(urllib.request.urlopen(playlist_url).read())
        data['title'] = playlist['items'][0]['snippet']['title']
        data['link'] = YT_PLAYLIST_BASE.format(pid)
        data['thumbnail'] = playlist['items'][0]['snippet']['thumbnails']['default']['url']

    return data

async def download(url):
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
    search_url = YT_VIDEO_API.format(query.replace(' ','+'),YT_KEY)
    results = json.loads(urllib.request.urlopen(search_url).read())
    if len(results['items']) == 0:
        return None
    return YT_VIDEO_BASE.format(results['items'][0]['id']['videoId'])
