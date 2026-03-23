import os
from pathlib import Path
import yt_dlp


def sanitize_filename(name: str) -> str:
    """Remove characters that break filenames."""
    forbidden = '<>:"/\\|?*'
    for ch in forbidden:
        name = name.replace(ch, '')
    return name.strip()


def fetch_playlist_titles(url: str):
    """Fetch playlist entries using yt-dlp without downloading."""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # faster, no deep metadata
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    if 'entries' not in info:
        raise ValueError("Not a playlist or no entries found.")

    titles = []
    for entry in info['entries']:
        if entry:
            title = sanitize_filename(entry.get('title', 'unknown'))
            titles.append(f"{title}.mp3")

    return titles, info.get('title', 'playlist')


def save_m3u(titles, playlist_name):
    """Save to MPD playlist directory."""
    mpd_dir = Path.home() / ".config/mpd/playlists"
    mpd_dir.mkdir(parents=True, exist_ok=True)

    filename = sanitize_filename(playlist_name) + ".m3u"
    filepath = mpd_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        for title in titles:
            f.write(title + "\n")

    return filepath


def main():
    url = input("Enter YouTube playlist URL: ").strip()

    print("Fetching playlist...")
    titles, playlist_name = fetch_playlist_titles(url)

    path = save_m3u(titles, playlist_name)

    print(f"\nSaved playlist to: {path}")
    print(f"Total tracks: {len(titles)}")


if __name__ == "__main__":
    main()