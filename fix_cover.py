import subprocess
import tempfile
from pathlib import Path
from mutagen.id3 import ID3, APIC
from config import MUSIC_DIR

for mp3 in MUSIC_DIR.rglob("*.mp3"):
    try:
        audio = ID3(mp3)

        # get existing artwork
        apic = audio.getall("APIC")
        if not apic:
            continue

        img_data = apic[0].data

        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)

            original = tmp / "cover.png"
            square = tmp / "square.jpg"

            with open(original, "wb") as f:
                f.write(img_data)

            # crop to square
            subprocess.run([
                "ffmpeg",
                "-loglevel", "error",
                "-y",
                "-i", str(original),
                "-vf", "crop=min(iw\\,ih):min(iw\\,ih),scale=600:600",
                str(square)
            ], check=True)

            with open(square, "rb") as f:
                new_img = f.read()

        # replace artwork
        audio.delall("APIC")
        audio.add(APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=new_img
        ))
        audio.save()

        print("fixed:", mp3)

    except Exception as e:
        print("error:", mp3, e)