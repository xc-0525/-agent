import re
import os
from openAICompatibleClient import OpenAICompatibleClient
from system_prompt import agent_system_prompt
from tools.available_tools import available_tools
from dotenv import load_dotenv
load_dotenv()


api_key=os.getenv("LLM_API_KEY")
base_url = os.getenv("LLM_BASE_URL")
model_id = os.getenv("LLM_MODEL_ID")
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")



llm=OpenAICompatibleClient(
    model=model_id,
    api_key=api_key,
    base_url=base_url
    )

def run_agent(user_prompt:str)->str:
    prompt_history = [f"用户请求     {user_prompt}"]
    final_answer = "抱歉，Agent 在限定步数（5次）内未能得出最终结论，请检查日志。"
    print(f"用户输入：{user_prompt}\n"+"="*40)
    
    called_tools = set()

    for i in range(5):
        print(f"这是第{i+1}次循环")
        full_prompt = "\n".join(prompt_history)
        llm_output = llm.generate(full_prompt,system_prompt=agent_system_prompt)
        

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

        action_str = action_str.replace("调用工具：", "").replace("结束任务：", "").strip()

        if "Finish" in action_str:
            start_idx = action_str.find("[")
            end_idx = action_str.rfind("]")
            
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                final_answer = action_str[start_idx + 1 : end_idx]
            else:
                final_answer = action_str.split("Finish")[-1].strip("[] \n")
                
            print(f"任务完成，最终答案: {final_answer}")
            break
        
        try:    
            tool_match = re.search(r"(\w+)\(", action_str)
            args_match = re.search(r"\((.*)\)", action_str)
        
        
            if tool_match and args_match:
                tool_name = tool_match.group(1)
                args_str = args_match.group(1)
                kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

                if tool_name in called_tools:
                    observation = f"错误：{tool_name} 工具已经调用过了，禁止重复调用。请直接根据已有的信息输出 Finish[最终答案] 来完成任务。"
                elif tool_name in available_tools:
                    observation = available_tools[tool_name](**kwargs)
                    called_tools.add(tool_name) 
                else:
                    observation = f"错误:未定义的工具 '{tool_name}'"
            else:
                final_answer = action_str
                print(f"模型输出自然语言，作为最终答案: {final_answer}")
                break
        except:
            observation = "错误: 无法解析工具调用格式，请严格使用 get_weather(city=\"城市\") 或 get_attraction(city=\"城市\", weather=\"天气\") 或 Finish[最终答案] 格式。"
        
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)
    
    
    return final_answer
