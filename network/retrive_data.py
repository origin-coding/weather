import json
from pathlib import Path
import requests
from datetime import datetime


def get_city_id(state: str, city: str) -> str:
    with Path("./config.json").open(mode="r", encoding="UTF-8") as fp:
        config_data = json.load(fp)
        if state in ("beijing", "shanghai", "chongqing", "tianjin"):
            url = str(config_data["url"]["get_city_id_base"]) + state
        else:
            url = str(config_data["url"]["get_city_id_base"]) + state + "/" + city
    response = requests.get(url)
    if "code" in json.loads(response.content.decode("UTF-8")):
        return ""

    return json.loads(response.content.decode("UTF-8"))["id"]


def get_current_air_data(city_id: str):
    with Path("./config.json").open(mode="r", encoding="UTF-8") as fp:
        config_data = json.load(fp)
        url = str(config_data["url"]["get_current_air_data"]) + city_id
    response = requests.get(url)
    required_data = json.loads(response.content.decode("UTF-8"))["current"]
    result = {"aqi": required_data["aqi"]}
    for item in required_data["pollutants"]:
        result[item["pollutantName"]] = item["concentration"] if "concentration" in item else 0
    return result


def get_history_air_data(city_id: str):
    with Path("./config.json").open(mode="r", encoding="UTF-8") as fp:
        config_data = json.load(fp)
        url = str(config_data["url"]["get_history_air_data"]).format(city_id)
    print(url)
    response = requests.get(url)
    result = []
    for item in json.loads(response.content.decode("UTF-8"))["measurements"]["daily"]:
        result.append({
            "time": datetime.strptime(item["ts"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d"),
            "aqi": item["aqi"],
            "pm25": item["pm25"]["concentration"] if "pm25" in item else 0,
            "pm10": item["pm10"]["concentration"] if "pm10" in item else 0,
            "o3": item["o3"]["concentration"] if "o3" in item else 0,
            "no2": item["no2"]["concentration"] if "no2" in item else 0,
            "so2": item["so2"]["concentration"] if "so2" in item else 0,
            "co": item["co"]["concentration"] if "co" in item else 0
        })

    return result
