import json
import requests

# Ollama 文件：https://github.com/ollama/ollama/blob/main/docs/api.md

class OllamaClient:
    # Ollama Restful API 預設託管在本地主機的 11434 埠口，但可以在啟動時透過指令變更：
    # sudo -u ollama nohup env OLLAMA_HOST=192.168.110.131:8005 OLLAMA_ORIGINS=* ollama serve > /var/log/ollama.log 2>&1 &
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    def chat_completions_create(self, model, messages, temperature=0.7):

        # /api/generate 端點用於針對給定提示產生回應/完成，詳細 API 文件請參考：https://github.com/ollama/ollama/blob/main/docs/api.md
        url = f"{self.base_url}/api/generate"

        # 可以使用 requests 函式庫 來呼叫 ollama 的 restful api， 需設定回應標頭
        headers = {'Content-Type': 'application/json'}

        # 以及資料變數
        payload = {
            "model": model,
            "prompt": self._format_messages(messages),
            "stream": False,
            "temperature": temperature
        }

        try:

            response = requests.post(url=url, headers=headers, data=json.dumps(payload))

            # 若為 200，則印出回應文字，否則印出錯誤。
            if response.status_code == 200:
                # 可從 JSON 物件中擷取正確的回應文字
                response_text = response.text
                data = json.loads(response_text)
                actual_response = data['response']
                return actual_response
            else:
                print("錯誤:", response.status_code, response.text)

        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"無法連線至 Ollama 伺服器 {self.base_url}。請確認 Ollama 已啟動且可存取。")
        except requests.exceptions.Timeout:
            raise TimeoutError(f"連線 Ollama 伺服器 {self.base_url} 請求逾時。伺服器可能過載或無回應。")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(f"指定的模型可能不存在於 Ollama 伺服器上。錯誤: {str(e)}")
            else:
                raise

    def _format_messages(self, messages):
        formatted_prompt = ""
        for message in messages:
            if message["role"] == "system":
                formatted_prompt += f"System: {message['content']}\n"
            elif message["role"] == "user":
                formatted_prompt += f"Human: {message['content']}\n"
            elif message["role"] == "assistant":
                formatted_prompt += f"Assistant: {message['content']}\n"
        return formatted_prompt.strip()

    def _parse_response(self, response):
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": response.get("response", "")
                    }
                }
            ]
        }