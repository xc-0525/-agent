import os
from tavily import TavilyClient

def get_attraction(city: str, weather: str)->str:
    """
    查询推荐指定城市的景点,使用Tavily API获取。
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY环境变量未设置")
    tavily= TavilyClient(api_key=api_key)
    query = f"{city}在{weather}天气下推荐景点"
    try:
        response = tavily.search(query=query,search_depth="basic",include_answer=True)
        if response.get('answer'):
            return response['answer']
        formatted_results = []
        for result in response.get("results",[]):
            formatted_results.append(f"{result['title']}：{result['content']}")
        if not formatted_results:
            return "抱歉，没有找到推荐的景点。"
        return "根据搜索为你找到以下信息：\n" + "\n".join(formatted_results)
    except Exception as e:
        return f"使用Tavily API查询{city}的景点失败：-{e}"
