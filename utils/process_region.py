from pypinyin import lazy_pinyin


def process_state(state: str) -> str:
    """
    根据省份返回第三方API需要的省份格式
    :param state: 需要处理的省份名称
    :return: 处理后的省份名称
    """
    # 首先处理特殊项
    if state == "西藏":
        return "tibet"
    if state == "陕西":
        return "shaanxi"
    if state == "内蒙古":
        return "inner%20mongolia"

    # 一般项直接转换成拼音即可
    return "".join(lazy_pinyin(state))


def process_city(city: str) -> str:
    """
    根据城市名返回第三方API需要的省市格式
    :param city: 需要处理的城市名称
    :return: 处理后的城市名称
    """
    # 首先处理特殊项
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

    # 一般项直接转换成拼音
    return "".join(lazy_pinyin(city))
