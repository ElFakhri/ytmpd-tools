import yt_dlp
from config import MUSIC_DIR

ydl_opts = {
    "paths": {"home": MUSIC_DIR},
    "js_runtimes": {"node": {"executable": "/usr/bin/node"}},
    "outtmpl": "%(track,title)s.%(ext)s",
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        },
        {
            "key": "EmbedThumbnail",
        },
        {
            "key": "FFmpegMetadata",
        }
    ],
    "writethumbnail": True,
}

url = "URL"

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])