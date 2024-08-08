# pyqt5 패키지 설치
# pymysql 패키지 설치

import pymysql
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

        self.join_btn.clicked.connect(self.member_join)  # 회원입력 버튼이 클릭되면 회원입력함수를 호출

    def member_join(self):  # 회원 입력 처리 함수
        memberid = self.joinid_input.text()  # 유저가 입력한 회원아이디 가져오기
        memberpw = self.joinpw_input.text()  # 유저가 입력한 회원비밀번호 가져오기
        membername = self.joinname_input.text()  # 유저가 입력한 회원이름 가져오기
        memberemail = self.joinemail_input.text()  # 유저가 입력한 회원이메일 가져오기
        memberaddr = self.joinaddress_input.text()  # 유저가 입력한 회원주소 가져오기
        memberphone = self.joinphone_input.text()  # 유저가 입력한 회원전화번호 가져오기

        conn = pymysql.connect(user="root", password="12345", host="localhost", db="memberdb")

        sql = f"INSERT INTO membertbl VALUES('{memberid}','{memberpw}','{membername}','{memberemail}','{memberaddr}','{memberphone}')"

        cur = conn.cursor()  # 커서 생성
        success = cur.execute(sql)  # sql문을 db에 실행->성공 1 실패 0

        cur.close()
        conn.commit()
        conn.close()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())


