import sys

from ui import MainWidget
from PyQt5.QtWidgets import QApplication


def main():
    app: QApplication = QApplication(sys.argv)
    main_widget = MainWidget()
    main_widget.show()
    return app.exec()


if __name__ == '__main__':
    exit(main())
