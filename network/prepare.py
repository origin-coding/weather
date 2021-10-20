import json
import time
from pathlib import Path

import requests


def get_states_and_cities():
    """
    用于获取全国支持的省市名单，便于查找不能通过转换成拼音的方式获取API需要的省市名称格式的地区
    """
    result: dict = {}

    # 这里路径写死了，因此无法在别的文件夹下执行
    with Path("../config.json").open(mode="r", encoding="UTF-8") as fp:
        json_data = json.load(fp)
        # 获取配置项
        key = json_data["api_key"]
        get_states_url = str(json_data["url"]["get_supported_state"]).format(key)
        print(get_states_url)
        # 获取省份
        states = json.loads(requests.get(get_states_url).content)
        print(states)
        # 针对每个省份，获取对应的城市名
        for _ in states["data"]:
            state = _["state"]
            result[state] = []
            get_cities_url = str(json_data["url"]["get_supported_city"]).format(state, key)
            response = requests.get(get_cities_url)
            time.sleep(6)  # 每次间隔时间设置为6秒，因为网站有QPM上限
            for _ in json.loads(response.content)["data"]:
                print(state)
                print(_["city"])
                result[state].append(_["city"])

    # 保存数据
    with Path("./states_and_cities.json").open(mode="w", encoding="UTF-8") as fp:
        json.dump(result, fp)


if __name__ == '__main__':
    get_states_and_cities()
