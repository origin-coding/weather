from typing import List

from pyecharts.charts import Bar, Line
from pyecharts import options as opts
from pathlib import Path
from datetime import datetime

from pyecharts.globals import ThemeType


def visualize_current_data(data: dict) -> str:
    """
    使用柱状图可视化实时空气数据
    :param data: 获取到的当前空气数据
    :return 返回渲染的html文件的URI
    """
    # 获取数据
    x_axis: List[str] = ["Pm2.5", "Pm10", "CO", "NO2", "SO2", "O3"]
    data_keys: List[str] = ["pm25", "pm10", "co", "no2", "so2", "o3"]
    y_axis = [data.get(key, 0) for key in data_keys]

    # 创建图表
    bar: Bar = (Bar(init_opts=opts.InitOpts(theme=ThemeType.CHALK, page_title="实时空气数据"))
        .add_xaxis(x_axis)
        .add_yaxis("浓度 单位mg/m3", y_axis)
        .set_global_opts(opts.TitleOpts(
        title=f"各种污染物浓度  今日AQI指数：{data.get('aqi', 0)}",
        subtitle=datetime.now().strftime("%Y-%m-%d")))
    )

    # 渲染图表，得到文件路径并且返回对应的URI
    file_path = bar.render("./current.html")
    return str(Path(file_path).as_uri())


def visualize_history_data(dataset: List[dict]):
    """
    使用折线图可视化历史空气数据
    :param dataset: 获取到的历史空气数据
    :return: 渲染出来的HTML文件的URI
    """
    # 获取数据
    time_series = [data["time"] for data in dataset]
    aqi_series = [data.get("aqi", None) for data in dataset]
    pm25_series = [data.get("pm25", None) for data in dataset]
    pm10_series = [data.get("pm10", None) for data in dataset]
    o3_series = [data.get("o3", None) for data in dataset]
    no2_series = [data.get("no2", None) for data in dataset]
    so2_series = [data.get("so2", None) for data in dataset]
    co_series = [data.get("co", None) for data in dataset]

    # 创建图表
    line: Line = (Line(init_opts=opts.InitOpts(theme=ThemeType.CHALK, page_title="历史空气数据"))
        .add_xaxis(time_series)
        # 除Pm2.5以外，其他污染物默认不选中
        .add_yaxis("AQI指数", aqi_series, is_selected=False)
        .add_yaxis("Pm2.5浓度", pm25_series)
        .add_yaxis("Pm10浓度", pm10_series, is_selected=False)
        .add_yaxis("O3浓度", o3_series, is_selected=False)
        .add_yaxis("NO2浓度", no2_series, is_selected=False)
        .add_yaxis("SO2浓度", so2_series, is_selected=False)
        .add_yaxis("CO浓度", co_series, is_selected=False)
        .set_global_opts(title_opts=opts.TitleOpts(
        title="AQI指数和空气污染物浓度（单位：mg/m3）",
        subtitle=datetime.now().strftime("%Y-%m-%d")),
        legend_opts=opts.LegendOpts(pos_bottom="2%")
    )
    )

    # 渲染图表
    file_path = line.render("./history.html")
    return str(Path(file_path).as_uri())
