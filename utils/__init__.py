from .vedioProcesser import VideoProcessor
from .voiceProcesser import VoiceProcesser
from .srtProcesser import SrtProcesser
from .translater import Translater
from .asr import AutomaticSpeechRecognizer

import shutil
from pathlib import Path


class VedioSrtAdder:
    def __init__(self):
        self.video_processor = VideoProcessor()
        self.voice_processor = VoiceProcesser()
        self.tanslater = Translater()
        self.srtProcessor = SrtProcesser()
        self.asr = AutomaticSpeechRecognizer()

    def run(self, video_path, output_path=None):
        work_dir = Path("work_dir")
        work_dir.mkdir(exist_ok=True)

        # check output path
        video_path = Path(video_path).absolute()
        if output_path is None:
            output_path = (
                video_path.parent / f"{video_path.stem}_with_srt{video_path.suffix}"
            )
        else:
            output_path = Path(output_path)

        # extract audio from video
        audio_path = work_dir / "extracted_audio.wav"
        self.video_processor.video_to_audio(video_path, audio_path)

        # cut voice by vad
        audio_list = self.voice_processor.cut_voice_by_vad(audio_path)

        # convert audio to text
        audio_info_list = self.asr.getVoiceInfo(audio_list)
        for text, start_time, end_time in audio_info_list:
            print(f"Start: {start_time}, End: {end_time}, Text: {text}")

        # translate text
        asr_info = self.tanslater.batch_translate(
            audio_info_list,
            sorce_language="en",
            target_language="zh",
        )

        # generate srt
        srt_path = work_dir / "subtitles.srt"
        self.srtProcessor.generate_srt_file(asr_info, srt_path)

        # add srt to video
        self.video_processor.add_srt(video_path, srt_path, output_path)

        shutil.rmtree(work_dir)
