import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
con = sqlite3.connect("mydatabase.sqlite")
cur = con.cursor()

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("dotochniy_fail.ui", self)
        self.pushButton.clicked.connect(self.update_result)
        self.modified = {}
        self.titles = None

    def update_result(self):
        result = cur.execute("SELECT * FROM genres WHERE sort=?",
                         (item_id := self.lineEdit.text(), )).fetchall()
        print(item_id)
        # Получили результат запроса, который ввели в текстовое поле
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с именем {item_id}")
            self.tableWidget.setColumnCount(len(result[0]))
            self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    uic = MyWidget()
    uic.show()
    sys.exit(app.exec_())