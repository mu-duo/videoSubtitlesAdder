import requests
from .config import TRANSLATER_CONFIG, API_KEY


class Translater:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
        }
        self.model = TRANSLATER_CONFIG.MODEL
        self.url = TRANSLATER_CONFIG.URL
        self.temperature = 0.3

    def translate(self, text, sorce_language="auto", target_language="en"):

        # 构造翻译指令
        if sorce_language == "auto":
            instruction = (
                f"请将以下内容翻译成{target_language}, 不要输出额外内容：{text}"
            )
        else:
            instruction = f"请将以下{sorce_language}内容翻译成{target_language}不要输出额外内容：{text}"

        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": instruction}],
            "temperature": self.temperature,
            "stream": False,
        }

        try:
            response = requests.post(
                f"{self.url}",
                headers=self.headers,
                json=data,
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"].strip()
                else:
                    raise Exception("API响应格式异常")
            else:
                raise Exception(
                    f"API请求失败: {response.status_code} - {response.text}"
                )

        except requests.exceptions.Timeout:
            raise Exception("请求超时，请重试")
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求错误: {str(e)}")

    def batch_translate(self, texts: list, **kwargs) -> list:
        results = []
        for [text, start_time, end_time] in texts:
            try:
                translated = self.translate(text, **kwargs)
                results.append((translated, start_time, end_time))
            except Exception as e:
                # results.append(f"翻译失败: {str(e)}")
                print(f"翻译失败: {str(e)}")
                results.append((text, start_time, end_time))
        return results


if __name__ == "__main__":
    translater = Translater()
    result = translater.translate("Hello, how are you?", target_language="zh")
    print(result)