import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from ui.create_widgets import create_label, create_line_edit, create_push_button

from utils import process_state, process_city
from network import get_city_id, get_current_air_data, get_history_air_data
from visualize import visualize_current_data, visualize_history_data


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        # 创建标签
        self.state_label = create_label("请输入省份：")
        self.state_label.move(0, 0)
        self.state_label.setParent(self)

        self.city_label = create_label("请输入城市：")
        self.city_label.setParent(self)
        self.city_label.move(0, 30)

        # 创建输入框
        self.state_edit = create_line_edit("省份或直辖市")
        self.state_edit.move(100, 0)
        self.state_edit.setParent(self)

        self.city_edit = create_line_edit("城市名称")
        self.city_edit.move(100, 30)
        self.city_edit.setParent(self)

        # 创建查询按钮
        self.button = create_push_button("开始查询")
        self.button.move(0, 60)
        self.button.setParent(self)

        # 按钮添加槽函数
        self.button.clicked.connect(self.main_func)

        # 创建图表窗体类
        self.current_data_graph = None
        self.history_data_graph = None

    def main_func(self):
        # 获取输入的省市
        state = self.state_edit.text().strip()
        city = self.city_edit.text().strip()

        # 得到地区信息，用作后面图表的标题
        region = f"{state + '市' if state in ('北京', '上海', '重庆', '天津') else state + '省' + city + '市'}"
        print(region)

        # 处理省市信息并获取对应的city_id
        processed_state = process_state(state)
        processed_city = process_city(city)
        city_id = get_city_id(processed_state, processed_city)

        # 如果返回值为空串，表明输入的省市不存在，提示用户输入错误并清空输入框
        if len(city_id) == 0:
            QMessageBox.warning(self, "地区不存在", "您输入的地区有误，请重新输入")
            self.state_edit.clear()
            self.city_edit.clear()
            return

        # 获取当前城市的实时空气数据和历史空气数据，以图表的形式展现
        current_data = get_current_air_data(city_id)
        history_data = get_history_air_data(city_id)
        # 获取渲染的路径
        current_data_html_path = visualize_current_data(current_data)
        history_data_html_path = visualize_history_data(history_data)
        # 显示图表
        self.current_data_graph = GraphWidget(current_data_html_path, region, True)
        self.history_data_graph = GraphWidget(history_data_html_path, region, False)
        self.current_data_graph.show()
        self.history_data_graph.show()

        # 最后，清空输入
        self.state_edit.clear()
        self.city_edit.clear()




class GraphWidget(QWidget):
    def __init__(self, uri: str, region: str, current: bool):
        super().__init__()
        # 设置窗体大小和标题
        self.setFixedSize(920, 520)
        self.setWindowTitle(f"{region}{'实时' if current else '历史'}空气质量数据")

        # 加载网页
        self.view = QWebEngineView()
        self.view.setFixedSize(920, 520)
        self.view.move(0, 0)
        self.view.setParent(self)
        self.view.load(QUrl(uri))


if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    # main_widget = GraphWidget("file:///E:/python_exp/weather/current.html", "辽宁省沈阳市", True)
    # main_widget.show()
    main_widget = MainWidget()
    main_widget.show()
    exit(app.exec())
