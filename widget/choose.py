import sys
import os
from PyQt5.QtWidgets import QApplication, QSizePolicy, QToolTip, QWidget, QWidgetItem, QSpacerItem, QLabel, QPushButton, QFrame, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from base import BaseWidget
import paths


CANCEL = "\x00cancel"


class QPushLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, pixmap, sended, master=None):
        super().__init__(master)
        self.pixmap = pixmap
        self.sended = sended
        self.build_inter()

    def build_inter(self):
        self.setPixmap(self.pixmap)

    def mouseReleaseEvent(self, *args, **kwargs):
        self.clicked.emit()

    def text(self):
        return CANCEL


class Choose(BaseWidget):
    title = "选择"
    icon = "choose.png"

    choosed = pyqtSignal(str)

    def __init__(self, ch_list, master=None):
        super().__init__(master, Choose.title, Choose.icon)
        self.ch_type, *self.ch_list = ch_list
        self.build_inter()

    def build_inter(self):
        with open("choose.qss") as f:
            self.setStyleSheet(f.read())

        self.setObjectName("choose")

        QToolTip.setFont(QFont("苹方-简", 16))

        self.main_vbox = QVBoxLayout()
        self.setLayout(self.main_vbox)

        temp = QPixmap(os.path.join(paths.IMAGE, "exit.png"))
        self.exit_icon = temp.scaled(40, 40, Qt.KeepAspectRatio)

        self.exit_btn = QPushLabel(self.exit_icon, CANCEL, master=self)
        self.exit_btn.clicked.connect(self.choose)
        self.exit_btn.move(15, 15)

        self.ch_prompt = QLabel("请选择{}".format(self.ch_type), self)
        self.ch_prompt.setFont(QFont("苹方-简", 30))
        self.ch_prompt.setObjectName("ch_title")
        self.hbox_top = QHBoxLayout()
        self.hbox_top.addStretch(1)
        self.hbox_top.addWidget(self.ch_prompt)
        self.hbox_top.addStretch(1)

        self.ch_prompt2 = QLabel("您不能选择未开放的{}".format(self.ch_type), self)
        self.ch_prompt2.setFont(QFont("苹方-简", 24))
        self.ch_prompt2.setObjectName("ch_title")
        self.hbox_top2 = QHBoxLayout()
        self.hbox_top2.addStretch(1)
        self.hbox_top2.addWidget(self.ch_prompt2)
        self.hbox_top2.addStretch(1)

        self._btn_layout = []
        for ch, choosable in self.ch_list:
            btn = QPushButton(ch, self)
            btn_font = QFont("苹方-简", 18)
            btn_font.setBold(True)
            btn.setFont(btn_font)
            btn.setFixedWidth(280)
            btn.setFixedHeight(52)
            if choosable:
                btn.setObjectName("choosable_btn")
                btn.clicked.connect(self.choose)
            else:
                btn.setObjectName("unchoosable_btn")
                btn.setToolTip("请先尝试完成之前的内容")
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(btn)
            hbox.addStretch(1)
            self._btn_layout.append(hbox)

        self.main_vbox.addStretch(6)
        self.main_vbox.addLayout(self.hbox_top)
        self.main_vbox.addStretch(1)
        self.main_vbox.addLayout(self.hbox_top2)
        self.main_vbox.addStretch(15)
        for layout in self._btn_layout:
            self.main_vbox.addLayout(layout)
            self.main_vbox.addStretch(1)
        self.main_vbox.addStretch(5)

        self.show()

    def choose(self):
        result = self.sender().text()
        self.choosed.emit(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Choose(["难度", ("简单", True), ("普通", True), ("困难", False)])
    w.resize(460, 733)
    sys.exit(app.exec_())
