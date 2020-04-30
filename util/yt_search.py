import os

import urllib
import json
from pathlib import Path

import youtube_dl


YT_VIDEO_API = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={}&key={}"
YT_PLAYLIST_API = "https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={}&key={}"
YT_PLAYLIST_ITEMS = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&key={}&maxResults=50"
YT_PLAYLIST_ITEMS_PAGINATION = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&key={}&pageToken={}&maxResults=50"
YT_PLAYLIST_BASE = 'https://www.youtube.com/playlist?list={}'
YT_KEY = os.getenv("YOUTUBE_API_KEY")
YT_VIDEO_BASE = 'https://www.youtube.com/watch?v={}'
YDL_OPTIONS = {
    'quiet': True,
    'format': 'bestaudio/best',
    'outtmpl': 'songs/%(id)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
}

#Searches for the url
def get_urls(message):
    '''Gets the YouTube Data API v3 entries of every single video in the playlist / or just the single video'''
    url = ' '.join(message.content.split(' ')[1:])
    try:
        #If it's a playlist
        if 'list=' in url:
            i = url.find('list=')
            pid = url[i + 5: i + 39] #Hardcoded 34 character long playlist id
            playlist_url = YT_PLAYLIST_ITEMS.format(pid,YT_KEY)
            playlist = json.loads(urllib.request.urlopen(playlist_url).read())
            urls = [video for video in playlist['items']] #get the entries for each video
            while 'nextPageToken' in playlist: #since the api request limits each call to 50 results, use the pagination feature to dl the rest
                playlist_url = YT_PLAYLIST_ITEMS_PAGINATION.format(pid,YT_KEY,playlist['nextPageToken'])
                playlist = json.loads(urllib.request.urlopen(playlist_url).read())
                n_urls = [video for video in playlist['items']]
                urls += n_urls
            return urls
        #If it is a link at all
        if 'v=' in url and 'youtube.com' in url:
            i = url.find('v=')
            data = search(url[i + 2: i + 13]) #Hardcoded 11 character long video id
        else:
            data = search(url)

        if data == None:
            return None
        return [data]
    except:
        return None

#Download the info only
def download_info(urls):
    '''Gets the title,link,thumbnail of the playlist/video'''

    if urls == None:
        return None

    data = dict()

    #If it has just one entry (request was a single video), return that video's info
    if len(urls) == 1:
        data['title'] = urls[0]['snippet']['title']
        data['link'] = YT_VIDEO_BASE.format(urls[0]['id']['videoId'])
        data['thumbnail'] = urls[0]['snippet']['thumbnails']['default']['url']
    elif len(urls) > 1:
    #Return the playlist's info
        pid = urls[0]['snippet']['playlistId']
        playlist_url = YT_PLAYLIST_API.format(pid,YT_KEY)
        playlist = json.loads(urllib.request.urlopen(playlist_url).read())
        data['title'] = playlist['items'][0]['snippet']['title']
        data['link'] = YT_PLAYLIST_BASE.format(pid)
        data['thumbnail'] = playlist['items'][0]['snippet']['thumbnails']['default']['url']

    return data

def download(vid):
    '''Downloads the video specified by the video id'''
    #Search could not find anything
    if vid == None:
        return None

    #Downloads the video with the url
    url = YT_VIDEO_BASE.format(vid)
    data = {}
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

            data['target'] = targ
            data['url'] = url
            data['title'] = info['title']
            data['thumbnail'] = info['thumbnails'][0]['url']
            data['downloaded'] = True

            #DIAGNOSTIC print statements (WOOHOO)
            print(f'Downloading: {info["title"]}')
            return data
    except:
        return None

def search(query):
    '''Searches for the query, returns the complete link to the video'''
    search_url = YT_VIDEO_API.format(query.replace(' ','+'),YT_KEY)
    results = json.loads(urllib.request.urlopen(search_url).read())
    if len(results['items']) == 0:
        return None
    return results['items'][0]
