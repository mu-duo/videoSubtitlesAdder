import ffmpeg
from pathlib import Path


class VideoProcessor:
    def __init__(self):
        pass

    def video_to_audio(self, video_path: Path, audio_path: Path):
        # use ffmpeg to extract audio from video
        print("🎬 video_path =", video_path)
        print("🎧 audio_path =", audio_path)
        print(
            "Exists? video:",
            Path(video_path).exists(),
            "audio dir:",
            Path(audio_path).parent.exists(),
        )

        stream = ffmpeg.input(str(Path(video_path).absolute()))
        stream = ffmpeg.output(stream, str(Path(audio_path).absolute()))
        print("🧩 Command:", ffmpeg.compile(stream))
        stream.run(overwrite_output=True)

    def add_srt(self, video_path, srt, output_path):
        # use ffmpeg to add srt(file_obj) subtitles to video

        src_path = str(srt).replace("\\", "/")

        ffmpeg.input(str(video_path.absolute())).output(
            str(output_path), vf=f"subtitles={src_path}"
        ).run(overwrite_output=True)
