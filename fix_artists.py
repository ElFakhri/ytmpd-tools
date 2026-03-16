from mutagen import File
import os
from config import MUSIC_DIR

def unique_preserve_order(items):
    seen = set()
    result = []
    for item in items:
        if item.lower() not in seen:
            seen.add(item.lower())
            result.append(item)
    return result

def fix_artists():
    for root, dirs, files in os.walk(MUSIC_DIR):
        for file in files:
            path = os.path.join(root, file)

            try:
                audio = File(path, easy=True)
                if not audio:
                    continue

                artists = audio.get("artist")
                if not artists:
                    continue

                fixed = []

                for entry in artists:
                    split = [a.strip() for a in entry.split(",")]
                    fixed.extend(split)

                fixed = unique_preserve_order(fixed)

                if artists != fixed:
                    audio["artist"] = fixed
                    audio.save()
                    print(f"Fixed: {path} -> {fixed}")

            except Exception as e:
                print(f"Skipped: {path}")

if __name__ == "__main__":
    fix_artists()