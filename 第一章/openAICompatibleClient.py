from openai import OpenAI
class OpenAICompatibleClient:
    def __init__(self,model: str, api_key: str,base_url: str):
        self.model= model
        self.client = OpenAI(api_key=api_key,base_url=base_url)

    def generate(self, prompt: str,system_prompt: str) -> str:
        """
        正在调用指定LLM模型生成
        """
        print(f"正在调用{self.model}模型生成：{prompt}")
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )
            answer =response.choices[0].message.content
            print(f"{self.model}模型响应成功，生成：{answer}")
            return answer
        except Exception as e:
            print(f"{self.model}模型生成失败：{e}")
            return f"生成失败：{e}"
            