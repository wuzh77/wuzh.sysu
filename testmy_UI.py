import math
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import pylab
import networkx as nx
import My_dijstra


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('最短路径')
        self.resize(700, 300)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowOpacity(0.94)
        self.init_UI()
        self.Str_path1 = ""
        self.Min_len1 = ""

    def init_UI(self):
        grid = QGridLayout()
        layout = QVBoxLayout()
        layout2 = QGridLayout()
        layout.setGeometry(QtCore.QRect(370, 0, 331, 431))
        layout.setContentsMargins(0, 0, 0, 0)
        # 第一个按钮
        my_button1 = QPushButton()
        my_button1.setEnabled(True)
        my_button1.setStyleSheet("QPushButton{\n"
                                 "        color: black;   \n"
                                 "        border-radius: 10px;  border: 2px groove gray;\n"
                                 "}")
        my_button1.setText('按下按钮显示最短路径')
        layout.addWidget(my_button1)
        my_button1.setFont(QFont("Microsoft YaHei"))

        # 第一个文本
        self.my_LineEdit = QLineEdit()
        self.my_LineEdit.setPlaceholderText('最短路径')
        self.my_LineEdit.setFont(QFont("Microsoft YaHei"))
        self.my_LineEdit.setReadOnly(True)
        self.my_LineEdit.setStyleSheet("LineEdit{\n"
                                       "        color: black;   \n"
                                       "        border-radius: 10px;  border: 2px groove gray;\n"
                                       "}"
                                       )
        layout.addWidget(self.my_LineEdit)

        # 第二个按钮
        my_button2 = QPushButton()
        my_button2.setEnabled(True)
        my_button2.setStyleSheet("QPushButton{\n"
                                 "        color: black;   \n"
                                 "        border-radius: 10px;  border: 2px groove gray;\n"
                                 "}")
        my_button2.setText('按下按钮显示最短路径长度')
        my_button2.setFont(QFont("Microsoft YaHei"))
        layout.addWidget(my_button2)

        # 第二个文本
        self.my_LineEdit1 = QLineEdit()
        self.my_LineEdit1.setPlaceholderText('最短路径长度')
        self.my_LineEdit1.setFont(QFont("Microsoft YaHei"))
        self.my_LineEdit1.setReadOnly(True)
        layout.addWidget(self.my_LineEdit1)

        # 第三个按钮
        my_button3 = QPushButton()
        my_button3.setEnabled(True)
        my_button3.setStyleSheet("QPushButton{\n"
                                 "        color: black;   \n"
                                 "        border-radius: 10px;  border: 2px groove gray;\n"
                                 "}")
        my_button3.setText("按下按钮可视化图")
        my_button3.setFont(QFont("Microsoft YaHei"))
        my_button3.clicked.connect(self.show_image)
        layout.addWidget(my_button3)

        # 设置标签
        my_Label1 = QLabel()
        my_Label1.setText("txt文件路径:")
        my_Label1.setFont(QFont("Microsoft YaHei"))
        layout2.addWidget(my_Label1, 0, 0, Qt.AlignLeft)

        # 创建文本框
        self.text1 = QLineEdit()
        self.text1.setPlaceholderText("输入文件路径")
        self.text1.setFont(QFont("Microsoft YaHei"))
        layout2.addWidget(self.text1, 0, 1, 1, 3, Qt.AlignLeft)

        # 创建确认按钮
        my_button4 = QPushButton()
        my_button4.setText("确认")
        my_button4.setStyleSheet("QPushButton{\n"
                                 "        color: black;   \n"
                                 "        border-radius: 10px;  border: 2px groove gray;\n"
                                 "}")
        my_button4.setFont(QFont("Microsoft YaHei"))
        layout2.addWidget(my_button4, 0, 4, Qt.AlignCenter)

        # 创建文件显示
        self.text2 = QTextEdit()
        self.text2.setPlaceholderText("文件信息")
        self.text2.setWordWrapMode(True)
        self.text2.setReadOnly(True)
        self.text2.setFont(QFont("Microsoft YaHei"))
        layout2.addWidget(self.text2, 1, 0, 1, 5, Qt.AlignCenter)

        grid.addLayout(layout, 0, 1)
        grid.addLayout(layout2, 0, 0)
        self.setLayout(grid)
        # 进行绑定
        my_button1.clicked.connect(self.show_MinlenPath)
        my_button2.clicked.connect(self.show_Minlen)
        my_button4.clicked.connect(self.get_info)

    def show_MinlenPath(self):
        self.my_LineEdit.setText(self.Str_path1)

    def show_Minlen(self):
        self.my_LineEdit1.setText(self.Min_len1)

    def show_image(self):
        pylab.show()

    def get_info(self):
        info = self.text1.text()
        self.Min_len1, self.Str_path1 = My_dijstra.Dijstra_1(info)
        my_showText = []
        f = open(info)
        for line in f:
            my_showText.append(line)
        str_myshowtext = "输入的信息为:\n"
        for l in my_showText:
            str_myshowtext += l
        self.text2.setText(str_myshowtext)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('C:/Users/17422/Desktop/logo.jpg'))
    ex = Example()
    ex.show()

    sys.exit(app.exec_())


