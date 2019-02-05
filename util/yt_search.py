import youtube_dl

def download(message):
    url = message.content.split(' ')[1]
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'songs/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        download_target = ydl.prepare_filename(info)
        ydl.download([url])
    targ = download_target.split('.')
    targ[-1] = 'wav'
    targ = '.'.join(targ)
    return targ
