# siliconflow API Key
API_KEY = "sk-ymszbsrriovdlqklguokxndjnoaweaaainsiiukxthnvxliv"

class AutomaticSpeechRecognition:
    MODEL_LIST = ["FunAudioLLM/SenseVoiceSmall", "TeleAI/TeleSpeechASR"]
    MODEL = MODEL_LIST[0]
    URL ="https://api.siliconflow.cn/v1/audio/transcriptions"

class TanslaterConfig:
    MODEL = "Qwen/QwQ-32B"
    URL = "https://api.siliconflow.cn/v1/chat/completions"

ASR_CONFIG = AutomaticSpeechRecognition()
TRANSLATER_CONFIG = TanslaterConfig()