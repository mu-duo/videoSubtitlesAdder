from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
import soundfile as sf
import io


class VoiceProcesser:
    def __init__(self):
        self.model = load_silero_vad()
        self.sampling_rate = 16000
        self.threshold = 0.5
        self.min_speech_duration_ms = 250
        self.min_silence_duration_ms = 100

    def cut_voice_by_vad(self, voice_path):
        # rerurn list of (sub_audio, start_time, end_time)
        ret = []

        audio = read_audio(voice_path, sampling_rate=self.sampling_rate)
        speech_timestamps = get_speech_timestamps(
            audio,
            self.model,
            threshold=self.threshold,
            min_speech_duration_ms=self.min_speech_duration_ms,
            min_silence_duration_ms=self.min_silence_duration_ms,
            return_seconds=True,
        )

        for ts in speech_timestamps:
            start_time = ts["start"]
            end_time = ts["end"]
            sub_audio = audio[
                int(start_time * self.sampling_rate) : int(
                    end_time * self.sampling_rate
                )
            ]

            # covert sub audio to bytes
            sub_audio = self.tensor_to_wav_bytes(sub_audio)
            ret.append((sub_audio, start_time, end_time))
        return ret

    def tensor_to_wav_bytes(self, audio_array):
        audio_array = audio_array.numpy()
        buffer = io.BytesIO()

        # soundfile可以更好地处理音频格式转换
        sf.write(
            buffer, audio_array, self.sampling_rate, format="WAV", subtype="PCM_16"
        )
        buffer.seek(0)

        return buffer
