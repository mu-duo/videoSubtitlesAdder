import requests
from .config import ASR_CONFIG, API_KEY


class AutomaticSpeechRecognizer:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
        }

    def audioTotext(self, audio):
        file = {"file": ("audio.wav", audio, "audio/wav")}
        data = {"model": ASR_CONFIG.MODEL}

        try:
            response = requests.post(
                ASR_CONFIG.URL, headers=self.headers, files=file, data=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP错误: {err}")
            if response.status_code == 400:
                print("请求参数错误")
            elif response.status_code == 401:
                print("认证失败，请检查API密钥")
            elif response.status_code == 404:
                print("接口不存在")
            elif response.status_code == 429:
                print("请求频率过高")
            elif response.status_code in [503, 504]:
                print("服务暂时不可用")
            return None

    def translate_text(self, text, target_language="en"):
        data = {
            "q": text,
            "target": target_language,
        }
        try:
            response = requests.post(
                "https://libretranslate.de/translate", data=data
            )
            response.raise_for_status()
            return response.json().get("translatedText", "")
        except requests.exceptions.HTTPError as err:
            print(f"HTTP错误: {err}")
            return ""

    def getVoiceInfo(self, audio_info_list):
        # audio_info_list: (audio, start_time, end_time)

        results = []
        for audio, start_time, end_time in audio_info_list:
            # tans audio to wav bytes
            response = self.audioTotext(audio)
            if response:
                text = response.get("text", "")
                results.append((text, start_time, end_time))

        return results
