import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from base import BaseWidget
import paths


class AuthInter(BaseWidget):
    title = "登录"
    icon = "auth.png"

    def __init__(self, master=None):
        super().__init__(master, AuthInter.title, AuthInter.icon)
        self.build_inter()

    def build_inter(self):
        with open("auth.qss", "r") as f:
            self.setStyleSheet(f.read())
        self.setObjectName("main")

        self.main_vbox = QVBoxLayout()
        self.setLayout(self.main_vbox)

        self.prompt_lb = QLabel("您的首次登录", self)
        self.prompt_lb.setFont(QFont("苹方-简", 30))
        self.prompt_lb.setObjectName("login_prompt")
        self.hbox_top = QHBoxLayout()
        self.hbox_top.addStretch(1)
        self.hbox_top.addWidget(self.prompt_lb)
        self.hbox_top.addStretch(1)

        self.small_lb = QLabel("需要您输入姓名以供教师查看", self)
        self.small_lb.setFont(QFont("苹方-简", 20))
        self.small_lb.setObjectName("login_prompt")
        self.hbox_center = QHBoxLayout()
        self.hbox_center.addStretch(1)
        self.hbox_center.addWidget(self.small_lb)
        self.hbox_center.addStretch(1)

        self.name_edit = QLineEdit(self)
        name_font = QFont("苹方-简", 22)
        name_font.setBold(True)
        self.name_edit.setFont(name_font)
        self.name_edit.setFixedWidth(300)
        self.name_edit.setFixedHeight(52)
        self.name_edit.setPlaceholderText(self.tr(" Name"))
        self.name_edit.setObjectName("name_edit")
        self.name_edit.textChanged.connect(self.std_adjust)
        self.name_edit.editingFinished.connect(self._submit)
        self.hbox_bottom = QHBoxLayout()
        self.hbox_bottom.addStretch(1)
        self.hbox_bottom.addWidget(self.name_edit)
        self.hbox_bottom.addStretch(1)

        self.submit_btn = QPushButton("确定", self)
        btn_font = QFont("苹方-简", 18)
        btn_font.setBold(True)
        self.submit_btn.setFont(btn_font)
        self.submit_btn.setFixedWidth(300)
        self.submit_btn.setFixedHeight(52)
        self.submit_btn.setObjectName("submit")
        self.submit_btn.clicked.connect(self._submit)
        self.hbox_btn = QHBoxLayout()
        self.hbox_btn.addStretch(1)
        self.hbox_btn.addWidget(self.submit_btn)
        self.hbox_btn.addStretch(1)

        self.main_vbox.addStretch(12)
        self.main_vbox.addLayout(self.hbox_top)
        self.main_vbox.addStretch(2)
        self.main_vbox.addLayout(self.hbox_center)
        self.main_vbox.addStretch(14)
        self.main_vbox.addLayout(self.hbox_bottom)
        self.main_vbox.addStretch(3)
        self.main_vbox.addLayout(self.hbox_btn)
        self.main_vbox.addStretch(42)

        self.show()

    def std_adjust(self):
        text = self.name_edit.text()
        text = " " + text.strip()
        self.name_edit.setText(text)

    def _submit(self):
        text = self.name_edit.text()
        self.submit(text)

    def submit(self, text):
        if not text and self.hasFocus():
            QMessageBox.warning(
                self, "System", "Please input a VALID name instead of spacings or none")
            return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AuthInter()
    w.resize(460, 733)  # 690x1100
    sys.exit(app.exec_())
