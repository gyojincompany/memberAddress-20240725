# pyqt5 패키지 설치
# pymysql 패키지 설치

import pymysql
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("ui/member2.ui")[0]
# 제작해 놓은 ui 불러오기

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("회원 주소록 프로그램")

        self.join_btn.clicked.connect(self.member_join)  # 회원입력 버튼이 클릭되면 회원입력함수를 호출
        self.idcheck_btn.clicked.connect(self.memberid_check)  # idcheck 버튼이 클릭되면 아이디 가입 가능 여부 확인함수를 호출
        self.joinreset_btn.clicked.connect(self.join_reset)  # 회원가입 초기화 버튼이 클릭되면 모든 입력사항 초기화
        self.search_btn.clicked.connect(self.search_memberinfo)  # 회원조회 버튼이 클릭되면 회원정보를 가져오는 함수 호출
        self.searchreset_btn.clicked.connect(self.search_reset)  # 회원조회 출력내용 초기화
        self.modify_btn.clicked.connect(self.modify_memberinfo)  # 정보수정 버튼이 클릭되면 회원정보수정 함수 호출
        self.memberlist_btn.clicked.connect(self.member_list)  # 회원리스트 조회 버튼 클릭시 회원리스트 출력 함수 호출

    def member_list(self):
        conn = pymysql.connect(user="root", password="12345", host="localhost", db="memberdb")

        sql = f"SELECT * FROM membertbl"
        # SQL문이 실행되었을때 반환되는 값->1 or 0
        # 기존에 가입된 아이디면 1, 가입되지 않은 아이디면 0이 반환

        cur = conn.cursor()  # 커서 생성
        cur.execute(sql)
        result = cur.fetchall()  # SQL문 실행결과가 반환->튜플
        print(result)

        cur.close()
        conn.close()

        result_list = []

        for member in result:
            memberid = member[0]
            memberpw = member[1]
            membername = member[2]
            memberemail = member[3]
            memberaddr = member[4]
            memberphone = member[5]

            temp_list = [memberid, memberpw, membername, memberemail, memberaddr, memberphone]

            result_list.append(temp_list)

        # print(result_list)

            self.outputTable(result_list)



    def outputTable(self, memberlist):  # 도선정보검색결과를 테이블 위젯에 출력하는 함수
        self.listTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.listTable.setColumnCount(7)  # 출력되는 테이블을 6열로 설정
        self.listTable.setRowCount(len(memberlist))  # 출력되는 테이블의 행 갯수 설정
        self.listTable.verticalHeader().setVisible(False)  # 행번호 안나오게 설정
        self.listTable.setSelectionBehavior(QAbstractItemView.SelectRows)  # Row 단위 선택
        # self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 셀 에디트 불가

        # 테이블의 첫 행(열 이름) 설정
        self.listTable.setHorizontalHeaderLabels(["번호", "아이디", "비밀번호", "이름", "이메일", "주소", "전화번호"])
        # 각 칼럼의 넓이 지정(총 길이 780을 5등분)
        self.listTable.setColumnWidth(0, 20)
        self.listTable.setColumnWidth(1, 60)
        self.listTable.setColumnWidth(2, 70)
        self.listTable.setColumnWidth(3, 70)
        self.listTable.setColumnWidth(4, 100)
        self.listTable.setColumnWidth(5, 150)
        self.listTable.setColumnWidth(6, 100)
        # 테이블에 출력되는 검색결과 수정 금지 기능 추가

        rownum = 0
        for i, member in enumerate(memberlist):  # i-> 0~9
            rownum = i + 1  # 행번호
            memberid = member[0]  # 아이디
            memberpw = member[1]  # 비밀번호
            membername = member[2]  # 이름
            memberemail = member[3]  # 이메일
            memberaddr = member[4]  # 주소
            memberphone = member[5]  # 전화번호

            self.listTable.setItem(i, 0, QTableWidgetItem(str(rownum)))
            self.listTable.setItem(i, 1, QTableWidgetItem(memberid))
            self.listTable.setItem(i, 2, QTableWidgetItem(memberpw))
            self.listTable.setItem(i, 3, QTableWidgetItem(membername))
            self.listTable.setItem(i, 4, QTableWidgetItem(memberemail))
            self.listTable.setItem(i, 5, QTableWidgetItem(memberaddr))
            self.listTable.setItem(i, 6, QTableWidgetItem(memberphone))

        self.listTable.resizeRowsToContents()

    def member_join(self):  # 회원 입력 처리 함수
        memberid = self.joinid_input.text()  # 유저가 입력한 회원아이디 가져오기
        memberpw = self.joinpw_input.text()  # 유저가 입력한 회원비밀번호 가져오기
        membername = self.joinname_input.text()  # 유저가 입력한 회원이름 가져오기
        memberemail = self.joinemail_input.text()  # 유저가 입력한 회원이메일 가져오기
        memberaddr = self.joinaddress_input.text()  # 유저가 입력한 회원주소 가져오기
        memberphone = self.joinphone_input.text()  # 유저가 입력한 회원전화번호 가져오기

        if memberid == "":
            QMessageBox.warning(self, "필수입력값 오류", "아이디는 필수 입력 사항입니다!")
        elif len(memberid) < 5 or len(memberid) > 15:
            QMessageBox.warning(self, "아이디 크기 오류", "아이디는 5~15 글자 이어야 합니다!")
        elif memberpw == "":
            QMessageBox.warning(self, "필수입력값 오류", "비밀번호는 필수 입력 사항입니다!")
        elif len(memberpw) < 5 or len(memberpw) > 15:
            QMessageBox.warning(self, "비밀번호 크기 오류", "비밀번호는 5~15 글자 이어야 합니다!")
        elif membername == "":
            QMessageBox.warning(self, "필수입력값 오류", "이름은 필수 입력 사항입니다!")
        elif memberemail == "":
            QMessageBox.warning(self, "필수입력값 오류", "이메일은 필수 입력 사항입니다!")
        elif memberaddr == "":
            QMessageBox.warning(self, "필수입력값 오류", "주소는 필수 입력 사항입니다!")
        elif self.memberid_check() == 1:
            pass
        else:
            conn = pymysql.connect(user="root", password="12345", host="localhost", db="memberdb")

            sql = f"INSERT INTO membertbl VALUES('{memberid}','{memberpw}','{membername}','{memberemail}','{memberaddr}','{memberphone}')"

            cur = conn.cursor()  # 커서 생성
            success = cur.execute(sql)  # sql문을 db에 실행->성공 1 실패 0
            
            if success == 1:
                QMessageBox.information(self, "회원가입성공", "축하합니다. 회원가입이 성공하였습니다.")
            else:
                QMessageBox.warning(self, "회원가입실패", "회원가입이 실패하였습니다!")

            cur.close()
            conn.commit()
            conn.close()

    def memberid_check(self):  # 가입가능 아이디 확인 체크 함수
        memberid = self.joinid_input.text()  # 유저가 입력한 회원아이디 가져오기

        if memberid == "":
            QMessageBox.warning(self, "필수입력값 오류", "아이디는 필수 입력 사항입니다!")
        else:

            conn = pymysql.connect(user="root", password="12345", host="localhost", db="memberdb")

            sql = f"SELECT COUNT(*) FROM membertbl WHERE memberid='{memberid}'"
            # SQL문이 실행되었을때 반환되는 값->1 or 0
            # 기존에 가입된 아이디면 1, 가입되지 않은 아이디면 0이 반환

            cur = conn.cursor()  # 커서 생성
            cur.execute(sql)
            result = cur.fetchall()  # SQL문 실행결과가 반환->튜플
            # print(result)

            if result[0][0] == 1:
                QMessageBox.warning(self, "가입불가아이디", "이미 가입된 아이디 입니다.")
            else:
                QMessageBox.warning(self, "가입가능아이디", "가입 가능한 아이디 입니다.")

            cur.close()
            conn.close()

            return result[0][0]

    def member_check(self):  # 가입되어있는 아이디 여부 확인 체크 함수
        memberid = self.searchid_input.text()  # 유저가 입력한 회원아이디 가져오기

        conn = pymysql.connect(user="root", password="12345", host="localhost", db="memberdb")

        sql = f"SELECT COUNT(*) FROM membertbl WHERE memberid='{memberid}'"
        # SQL문이 실행되었을때 반환되는 값->1 or 0
        # 기존에 가입된 아이디면 1, 가입되지 않은 아이디면 0이 반환

        cur = conn.cursor()  # 커서 생성
        cur.execute(sql)
        result = cur.fetchall()  # SQL문 실행결과가 반환->튜플
        # print(result)

        cur.close()
        conn.close()

        return result[0][0]  # return 값이 1이면 회원정보조회 가능한 아이디(기존에 가입된 아이디)
    
    def join_reset(self):  # 회원가입정보 입력내용 초기화
        self.joinid_input.clear()
        self.joinpw_input.clear()
        self.joinname_input.clear()
        self.joinemail_input.clear()
        self.joinaddress_input.clear()
        self.joinphone_input.clear()

    def search_memberinfo(self):  # 회원정보 조회 함수
        memberid = self.searchid_input.text()  # 회원정보를 조회하려는 아이디 가져오기

        if memberid == "":
            QMessageBox.warning(self, "필수입력값 오류", "아이디는 필수 입력 사항입니다!")
        elif self.member_check() == 0:
            QMessageBox.warning(self, "회원정보 오류", "회원으로 가입되지 않은 아이디입니다!")
        else:
            conn = pymysql.connect(user="root", password="12345", host="localhost", db="memberdb")

            sql = f"SELECT * FROM membertbl WHERE memberid='{memberid}'"

            cur = conn.cursor()  # 커서 생성
            cur.execute(sql)
            result = cur.fetchall()  # SQL문 실행결과가 반환->튜플

            # print(result)

            self.searchpw_input.setText(result[0][1])  # 비밀번호를 출력
            self.searchname_input.setText(result[0][2])  # 이름을 출력
            self.searchemail_input.setText(result[0][3])  # 이메일을 출력
            self.searchaddr_input.setText(result[0][4])  # 주소를 출력
            self.searchphone_input.setText(result[0][5])  # 전화번호를 출력

            cur.close()
            conn.close()

    def modify_memberinfo(self):  # 회원정보 수정 함수
        memberid = self.searchid_input.text()  # 아이디 가져오기
        memberpw = self.searchpw_input.text()  # 비밀번호 가져오기
        membername = self.searchname_input.text()  # 이름 가져오기
        memberemail = self.searchemail_input.text()  # 이메일 가져오기
        memberaddr = self.searchaddr_input.text()  # 주소 가져오기
        memberphone = self.searchphone_input.text()  # 전화번호 가져오기

        conn = pymysql.connect(user="root", password="12345", host="localhost", db="memberdb")

        sql = f"UPDATE membertbl SET memberpw='{memberpw}', membername='{membername}', memberemail='{memberemail}', memberaddr='{memberaddr}', memberphone='{memberphone}' WHERE memberid='{memberid}'"

        cur = conn.cursor()  # 커서 생성
        success = cur.execute(sql)

        if success == 1:  # 회원정보 수정 성공
            QMessageBox.warning(self, "회원정보수정 성공", "회원정보가 성공적으로 수정되었습니다.")
        else:
            QMessageBox.warning(self, "회원정보수정 실패", "회원정보 수정이 실패하였습니다.")

        cur.close()
        conn.commit()
        conn.close()


    def search_reset(self):  # 회원조회정보 출력내용 초기화
        self.searchid_input.clear()
        self.searchpw_input.clear()
        self.searchname_input.clear()
        self.searchemail_input.clear()
        self.searchaddr_input.clear()
        self.searchphone_input.clear()



app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())


