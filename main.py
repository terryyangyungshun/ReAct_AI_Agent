import json
from dotenv import load_dotenv
import os
from agent import CustomerServiceAgent
from op_llm_client import OllamaClient
from tools.query_product_data import query_by_product_name
from tools.calc import calculate
from tools.read_promotions import read_store_promotions
from openai import OpenAI

load_dotenv()
import re


def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)


def get_client(config):
    if config['openai'].get('use_model', True):
        return OpenAI(api_key=os.environ.get("API_KEY"))
    else:
        return OllamaClient()


def get_max_iterations(config):
    # 根據所選模型決定最大迭代次數
    if config['ollama']['use_model']:
        return config['ollama']['max_iterations']
    elif config['openai']['use_model']:
        return config['openai']['max_iterations']
    else:
        return 10  # 若未啟用任何模型，則設定預設迭代次數


def main():
    config = load_config()
    try:
        # 取得服務端實例（OpenAI API 或 Ollama Restful API）
        client = get_client(config)

        # 實例化客服 Agent
        agent = CustomerServiceAgent(client, config)
    except Exception as e:
        print(f"初始化 AI 客戶端時發生錯誤: {str(e)}")
        print("請檢查您的設定，並確保 AI 服務已啟動。")
        return

    tools = {
        "query_by_product_name": query_by_product_name,
        "read_store_promotions": read_store_promotions,
        "calculate": calculate,
    }

    # 主迴圈，支援多次用戶輸入
    while True:
        query = input("請輸入您的問題，或輸入『退出』結束: ")
        if query.lower() == '退出':
            break

        iteration = 0
        max_iterations = get_max_iterations(config)
        while iteration < max_iterations:  # 內部迴圈處理每一筆 query
            try:
                result = agent(query)
                print(result)
                action_re = re.compile(r'^Action: (\w+): (.*)$')
                actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
                if actions:
                    action_parts = result.split("Action:", 1)[1].strip().split(": ", 1)
                    tool_name = action_parts[0]
                    tool_args = action_parts[1] if len(action_parts) > 1 else ""
                    if tool_name in tools:
                        try:
                            observation = tools[tool_name](tool_args)
                            query = f"Observation: {observation}"
                        except Exception as e:
                            query = f"Observation: Error occurred while executing the tool: {str(e)}"
                    else:
                        query = f"Observation: Tool '{tool_name}' not found"
                elif "Answer:" in result:
                    print(f"客服回覆：{result.split('Answer:', 1)[1].strip()}")
                    break  # 收到答案後結束內部迴圈
                else:
                    query = "Observation: No valid action or answer found. Please provide a clear action or answer."

            except Exception as e:
                print(f"處理問題時發生錯誤: {str(e)}")
                print("請檢查您的設定，並確保 AI 服務已啟動。")
                break

            iteration += 1

        if iteration == max_iterations:
            print("已達到最大迭代次數但仍未獲得最終答案。")


if __name__ == "__main__":
    main()
