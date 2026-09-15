import re
import os
from openAICompatibleClient import OpenAICompatibleClient
from system_prompt import agent_system_prompt
from available_tools import available_tools

api_key = "19684bdae9974be7a2a81bea153c8288.rLbKypbZ6vZFFHfc"
base_url = "https://open.bigmodel.cn/api/paas/v4"
model_id="glm-4-flash"
TAVILY_API_KEY="YOUR_Tavily_KEY"
os.environ['TAVILY_API_KEY'] = TAVILY_API_KEY
    
llm=OpenAICompatibleClient(
    model=model_id,
    api_key=api_key,
    base_url=base_url
    )


user_prompt = "你好,我想知道北京的天气，然后帮我推荐一个景点。"
prompt_history = [f"用户请求     {user_prompt}"]

print(f"用户输入：{user_prompt}\n"+"="*40)
for i in range(5):
    print(f"这是第{i+1}次循环")
    full_prompt = "\n".join(prompt_history)
    llm_output = llm.generate(full_prompt,system_prompt=agent_system_prompt)
    match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("已截断多余的 Thought-Action 对")
    print(f"模型输出:\n{llm_output}\n")
    prompt_history.append(llm_output)
    
    action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
    if not action_match:
        observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)
        continue
    action_str = action_match.group(1).strip()

    if action_str.startswith("Finish"):
        final_answer = re.match(r"Finish\[(.*)\]", action_str).group(1)
        print(f"任务完成，最终答案: {final_answer}")
        break
    
    tool_name = re.search(r"(\w+)\(", action_str).group(1)
    args_str = re.search(r"\((.*)\)", action_str).group(1)
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

    if tool_name in available_tools:
        observation = available_tools[tool_name](**kwargs)
    else:
        observation = f"错误:未定义的工具 '{tool_name}'"

    observation_str = f"Observation: {observation}"
    print(f"{observation_str}\n" + "="*40)
    prompt_history.append(observation_str)
