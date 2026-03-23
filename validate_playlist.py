import os
import yt_dlp
from mutagen.easyid3 import EasyID3
from config import MUSIC_DIR

PLAYLIST_URL = "PLAYLIST_URL"
OUTPUT = "playlist.m3u"


songs = {}

def get_yt_playlist(url):
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True,
    }

    songs = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        for entry in info["entries"]:
            title = entry.get("title", "")
            songs.append(title.lower())

    return songs

def scan_music():
    files = {}

    for root, _, fs in os.walk(MUSIC_DIR):
        for f in fs:
            if f.endswith(".mp3"):
                path = os.path.join(root, f)
                meta = EasyID3(path)
                title = meta.get("title", [""])[0]
                key = title.lower()

                rel = os.path.relpath(path, MUSIC_DIR)

                files[key] = rel

    return files

def match(playlist, library):
    result = []

    for yt_song in playlist:
        matched_song = library.get(yt_song)
        if matched_song:
            result.append(matched_song)
            print("Match:", matched_song)
        else:
            print("Missing:", yt_song)

    return result

yt_playlist = get_yt_playlist(PLAYLIST_URL)
library = scan_music()
matches = match(yt_playlist, library)