import yt_dlp

ydl_opts = {
    "js_runtimes": ["node"],
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