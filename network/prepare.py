import json
import time
from pathlib import Path

import requests


def get_states_and_cities():
    result: dict = {}

    with Path("../config.json").open(mode="r", encoding="UTF-8") as fp:
        json_data = json.load(fp)
        key = json_data["api_key"]
        get_states_url = str(json_data["url"]["get_supported_state"]).format(key)
        print(get_states_url)
        states = json.loads(requests.get(get_states_url).content)
        print(states)
        for _ in states["data"]:
            state = _["state"]
            result[state] = []
            get_cities_url = str(json_data["url"]["get_supported_city"]).format(state, key)
            response = requests.get(get_cities_url)
            time.sleep(6)
            for _ in json.loads(response.content)["data"]:
                print(state)
                print(_["city"])
                result[state].append(_["city"])

    with Path("./states_and_cities.json").open(mode="w", encoding="UTF-8") as fp:
        json.dump(result, fp)


if __name__ == '__main__':
    get_states_and_cities()
