from pypinyin import lazy_pinyin


def process_state(state: str) -> str:
    if state == "西藏":
        return "tibet"
    if state == "陕西":
        return "shaanxi"
    if state == "内蒙古":
        return "inner%20mongolia"

    return "".join(lazy_pinyin(state))


def process_city(city: str) -> str:
    if city == "哈尔滨":
        return "harbin"
    if city == "建瓯":
        return "jian'ou"
    if city == "保定":
        return "baoding%20shi"
    if city == "沧州":
        return "cangzhou%20shi"
    if city == "衡水":
        return "hengshui%20shi"
    if city == "大兴安岭":
        return "da%20hinggan%20ling"

    return "".join(lazy_pinyin(city))
