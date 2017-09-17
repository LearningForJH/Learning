import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
import paths


class BaseWidget(QWidget):
    def __init__(self, master, title, icon):
        super().__init__(master)
        self.master = master
        self.title = title
        self.icon = icon
        self.full_path = os.path.join(paths.IMAGE, self.icon)
        if self.master:
            self.build_master_inter()

    def build_master_inter(self):
        self.master.setWindowTitle(self.title)
        self.master.setWindowIcon(QIcon(self.full_path))
