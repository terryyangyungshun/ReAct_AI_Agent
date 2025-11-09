from op_llm_client import OllamaClient


class CustomerServiceAgent:
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.messages = []
        self.system_prompt = """
        You are a Intelligent customer service assistant for e-commerce platform. It is necessary to answer the user's consultation about the product in a timely manner. If it has nothing to do with the specific product, you can answer it directly.
        output it as Answer: [Your answer here].
       
        Example :
        Answer: Is there anything else I can help you with
        
        If specific information about the product is involved, You run in a loop of Thought, Action, Observation.
        Use Thought to describe your analysis process.
        Use Action to run one of the available tools - then wait for an Observation.
        When you have a final answer, output it as Answer: [Your answer here].
        
        Available tools:
        1. query_by_product_name: Query the database to retrieve a list of products that match or contain the specified product name. This function can be used to assist customers in finding products by name via an online platform or customer support interface
        2. read_store_promotions: Read the store's promotion document to find specific promotions related to the provided product name. This function scans a text document for any promotional entries that include the product name.
        3. calculate: Calculate the final transaction price by combining the selling price and preferential information of the product


        When using an Action, always format it as:
        Action: tool_name: argument1, argument2, ...

        Example :
        Human: Do you sell football in your shop? If you sell soccer balls, what are the preferential policies now? If I buy it now, how much will I get in the end?
        Thought: To answer this question, I need to check the database of the background first.
        Action: query_by_product_name: football

        Observation: At present, I have checked that the ball is in stock, and I know its price is 120 yuan.

        Thought: I need to further inquire about the preferential policy of football
        Action: read_store_promotions: football

        Observation: The current promotional policy for this ball is: 10% discount upon purchase

        Thought: Now I need to combine the selling price and preferential policies of the ball to calculate the final transaction price
        Action: calculate: 120 * 0.9

        Observation: The final price of the ball was 108.0 yuan

        Thought: I now have all the information needed to answer the question.
        Answer:  According to your enquiry, we do sell soccer balls in our store, the current price is 120 yuan. At present, we offer a 10% discount on the purchase of football. Therefore, if you buy now, the final transaction price will be 108 yuan.

        Note: You must reply to the final result in ZH-TW
        
        Now it's your turn:
        """.strip()
        self.messages.append({"role": "system", "content": self.system_prompt})

    # __call__ 方法可以使得一個類別的實例可以像函式那樣被呼叫，提供了類別實例的「可呼叫」能力。
    # 當使用類別實例後面加上括號並傳遞參數時，就會觸發 __call__ 方法。
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        response = self.execute()
        if not isinstance(response, str):
            raise TypeError(f"預期 execute 回傳字串，實際獲得 {type(response)}")
        self.messages.append({"role": "assistant", "content": response})
        return response

    def execute(self):

        # 檢查 self.client 是否為 OllamaClient 類別的實例。這是型別安全的做法，確保 self.client 具有執行接下來程式碼所需的方法與屬性。
        if isinstance(self.client, OllamaClient):
            completion = self.client.chat_completions_create(
                model=self.config["ollama"]['model_name'],
                messages=self.messages,
                temperature=self.config["ollama"]['temperature']
            )

            # 如果 completion 是字典且包含 'message' 鍵，則嘗試從 message 中取得 content 鍵對應的值。如果沒有 content，則回傳空字串。
            if isinstance(completion, dict) and 'message' in completion:
                return completion['message'].get('content', '')
            # 如果 completion 直接是字串，則直接回傳該字串。
            elif isinstance(completion, str):
                return completion
            else:
                raise ValueError(f"OllamaClient 回傳了非預期的資料結構: {completion}")
        else:
            # 使用 OpenAI 的 GPT 系列模型
            completion = self.client.chat.completions.create(
                model=self.config['openai']['model_name'],
                messages=self.messages,
            )
            response = completion.choices[0].message.content
            if response != None:
                return completion.choices[0].message.content
            else:
                return "目前沒有正常產生回覆，請重新思考目前的問題，並再次嘗試"


if __name__ == '__main__':
    import json
    from openai import OpenAI

    # 載入全域的設定資訊
    with open('config.json', 'r') as f:
        config = json.load(f)

    # 測試目前環境下是否可以連線 OpenAI 的 GPT 模型，如果能正常回傳回覆，則代表目前環境的網路正常
    client = OpenAI()
    completion = client.chat.completions.create(
        model=config['openai']['model_name'],
        messages=[{"role": "user", "content": "你好，測試 OpenAI 模型在目前環境下的連線狀態"}],
        temperature=config['openai']['temperature'],
    )
    print(completion.choices[0].message.content)
