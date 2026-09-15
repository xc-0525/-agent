import requests


def get_weather(city: str)->str:
    """
    通过wttr.in查询指定城市的实时天气。
    """
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data=response.json()
        current_condition=data['current_condition'][0]
        weather_desc =current_condition['weatherDesc'][0]['value']
        temp_c =current_condition['temp_C']

        return f"{city}的天气是{weather_desc}，温度是{temp_c}摄氏度。"
    except requests.exceptions.RequestException as e:
        return f"查询{city}的天气失败：-{e}"
    except (KeyError, IndexError) as e:
        return f"错误：可能是城市名错误。-{e}"
