import json
from pathlib import Path
import requests
from datetime import datetime


def get_city_id(state: str, city: str) -> str:
    """
    获取对应的city_id
    :param state: 处理后的省份名称
    :param city: 处理后的城市名称
    :return: 如果找到了需要查找的地区，就返回相应的city_id，否则返回一个空串
    """
    with Path("./config.json").open(mode="r", encoding="UTF-8") as fp:
        config_data = json.load(fp)
        # 如果是直辖市，就只查询直辖市
        if state in ("beijing", "shanghai", "chongqing", "tianjin"):
            url = str(config_data["url"]["get_city_id_base"]) + state
        # 如果查询的不是直辖市，就查询state/city
        else:
            url = str(config_data["url"]["get_city_id_base"]) + state + "/" + city

    # 调用第三方API，获取数据
    response = requests.get(url)

    # code项如果出现在返回值，就说明没有找到，返回空串
    if "code" in json.loads(response.content.decode("UTF-8")):
        return ""
    # 找到对应的city_id，返回
    return json.loads(response.content.decode("UTF-8"))["id"]


def get_current_air_data(city_id: str):
    """
    根据city_id获取实时的空气数据
    :param city_id: 需要查询的城市的city_id
    :return: 返回一个字典，里面的内容是AQI指数和各种污染物的浓度
    """
    # 加载配置项，获取URL
    with Path("./config.json").open(mode="r", encoding="UTF-8") as fp:
        config_data = json.load(fp)
        url = str(config_data["url"]["get_current_air_data"]) + city_id
    # 获取数据
    response = requests.get(url)
    required_data = json.loads(response.content.decode("UTF-8"))["current"]

    # 提取需要的数据并返回
    result = {"aqi": required_data["aqi"]}
    for item in required_data["pollutants"]:
        # 这里如果没有找到的数据自动设为0
        result[item["pollutantName"]] = item["concentration"] if "concentration" in item else 0
    return result


def get_history_air_data(city_id: str):
    """
    根据city_id获取历史空气数据
    :param city_id: 需要查找城市的city_id
    :return: 返回一个列表，每一项都是一个字典，字典里包含时间、AQI指数和各种污染物的浓度
    """
    # 加载配置项，获取数据
    with Path("./config.json").open(mode="r", encoding="UTF-8") as fp:
        config_data = json.load(fp)
        url = str(config_data["url"]["get_history_air_data"]).format(city_id)
    response = requests.get(url)

    # 得到需要的结果并返回
    result = []
    for item in json.loads(response.content.decode("UTF-8"))["measurements"]["daily"]:
        result.append({
            # 这里时间格式化成日期就可以了，没有必要精确到毫秒
            "time": datetime.strptime(item["ts"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d"),
            "aqi": item["aqi"],  # 一般缺失的都是一两个污染物的数据，因此不会影响到AQI指数
            # 如果查询不到对应污染物的浓度，就设为0
            "pm25": item["pm25"]["concentration"] if "pm25" in item else 0,
            "pm10": item["pm10"]["concentration"] if "pm10" in item else 0,
            "o3": item["o3"]["concentration"] if "o3" in item else 0,
            "no2": item["no2"]["concentration"] if "no2" in item else 0,
            "so2": item["so2"]["concentration"] if "so2" in item else 0,
            "co": item["co"]["concentration"] if "co" in item else 0
        })
    return result
