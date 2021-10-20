from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


def create_font() -> QFont:
    """
    用于产生宋体16号大小的字体变量
    :return: 特定字体和大小的字体变量
    """
    font: QFont = QFont()
    font.setFamily("宋体")
    font.setPixelSize(16)
    return font


def create_label(text: str) -> QLabel:
    f"""
    创建特定文字和固定样式的标签
    :param text: 标签的文字
    :return: 一个固定大小为{100, 30} 文字为{text} 字体为{create_font()} 且文字居中的标签
    """
    label: QLabel = QLabel()
    label.setFixedSize(100, 30)
    label.setText(text)
    label.setFont(create_font())
    label.setAlignment(Qt.AlignCenter)
    return label


def create_line_edit(placeholder: str) -> QLineEdit:
    f"""
    创建具有特定大小和提示信息的输入框
    :param placeholder: 需要的提示信息
    :return: 一个固定大小为{200, 30} 文字为{placeholder} 的输入框
    """
    edit: QLineEdit = QLineEdit()
    edit.setPlaceholderText(placeholder)
    edit.setFixedSize(200, 30)
    return edit


def create_push_button(text: str) -> QPushButton:
    f"""
    创建具有特定大小和文字的按钮
    :param text: 按钮的文字
    :return: 一个固定大小为{300, 40} 文字为{text} 的按钮
    """
    button: QPushButton = QPushButton()
    button.setText(text)
    button.setFixedSize(300, 40)
    button.setFont(create_font())
    return button
