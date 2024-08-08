# pyqt5 패키지 설치
# pymysql 패키지 설치

import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("ui/member.ui")[0]
# 제작해 놓은 ui 불러오기


class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("회원 주소록 프로그램")

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())


