import os
import sys
from pathlib import Path
from utils import VedioSrtAdder

ffmpeg_dir = Path(__file__).parent / "ffmpeg/bin"
os.environ["PATH"] = str(ffmpeg_dir) + os.pathsep + os.environ["PATH"]

if __name__ == "__main__":
    vsa = VedioSrtAdder()
    files = sys.argv[1:]

    todo = []
    if len(files) == 1 and Path(files[0]).is_dir():
        for f in Path(files[0]).rglob("*.mp4"):
            todo.append(f)
    for f in todo:
        vsa.run(f)
    else:
        for f in files:
            vsa.run(f)
