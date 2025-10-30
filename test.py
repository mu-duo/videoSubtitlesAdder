import requests
import json
from datetime import timedelta

api_key = "sk-ymszbsrriovdlqklguokxndjnoaweaaainsiiukxthnvxliv"
api_url = "https://api.siliconflow.cn/v1/audio/transcriptions"


class SimpleAudioTranslator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def seconds_to_srt_time(self, seconds):
        """将秒数转换为SRT时间格式"""
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        seconds = int(td.total_seconds() % 60)
        milliseconds = int((td.total_seconds() - int(td.total_seconds())) * 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    def call_siliconflow_api(self, audio_url, target_language="zh"):
        payload = {
            "audio_url": audio_url,
            "target_language": target_language,
            "response_format": "srt",  # 或者 "verbose_json" 然后自己转换
        }

        response = requests.post(api_url, headers=self.headers, json=payload)
        return response.json()

    def save_srt_file(self, srt_content, output_path):
        """保存SRT内容到文件"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(srt_content)


def transcribe_audio(audio_file_path, api_key, model="FunAudioLLM/SenseVoiceSmall"):
    """
    将音频文件转换为文本

    Args:
        audio_file_path (str): 音频文件路径
        api_key (str): API密钥
        model (str): 模型名称，默认为 FunAudioLLM/SenseVoiceSmall

    Returns:
        str: 转录的文本内容
    """

    # API端点
    url = "https://api.siliconflow.cn/v1/audio/transcriptions"

    # 请求头
    headers = {"Authorization": f"Bearer {api_key}"}

    # 准备表单数据
    files = {"file": open(audio_file_path, "rb")}

    data = {"model": model}

    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, files=files, data=data)

        # 检查请求是否成功
        response.raise_for_status()

        # 解析响应
        result = response.json()
        return result["text"]

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

    except Exception as err:
        print(f"其他错误: {err}")
        return None


# 使用示例
if __name__ == "__main__":
    AUDIO_FILE = "test.mp3"  # 支持常见音频格式如wav, mp3等

    # 调用转录函数
    transcribed_text = transcribe_audio(AUDIO_FILE, api_key, "IndexTeam/IndexTTS-2")

    if transcribed_text:
        print("转录结果:")
        print(transcribed_text)
    else:
        print("转录失败")
