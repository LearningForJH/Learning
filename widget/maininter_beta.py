import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QWidgetItem, QSpacerItem, QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QPoint
from base import BaseWidget
from study import Study, _areas, _info_list
import paths


# BOTTOM_ICON RGB
# NOT SELECTED: 120, 120, 120
# SELECTED: 0, 175, 255
# SELECTING: 240, 240, 240


class QPushLabel(QLabel):
    released = pyqtSignal()
    pressed = pyqtSignal()

    def __init__(self, master, pixmaps):
        super().__init__(master)
        self.pixmaps = pixmaps
        self.build_inter()

    def build_inter(self):
        self.setPixmap(self.pixmaps["not_selected"])
        self.setAlignment(Qt.AlignCenter)

        self.setContentsMargins(0, 0, 0, 0)

    def mousePressEvent(self, event):
        self.selecting()
        self.pressed.emit()

    def selecting(self):
        self.setPixmap(self.pixmaps["selecting"])

    def mouseReleaseEvent(self, event):
        self.have_selected()
        self.released.emit()

    def have_selected(self):
        self.setPixmap(self.pixmaps["selected"])

    def cancel(self):
        self.setPixmap(self.pixmaps["not_selected"])


class MainInter(BaseWidget):
    title = ""
    icon = "main.png"

    STUDY_IMAGE_WIDTH = 55
    STUDY_IMAGE_HEIGHT = 36
    SETTING_IMAGE_WIDTH = 48
    SETTING_IMAGE_HEIGHT = 48

    def __init__(self, master=None):
        super().__init__(master, MainInter.title, MainInter.icon)
        self.build_inter()

    def build_inter(self):
        with open("maininter.qss", "r") as f:
            self.setStyleSheet(f.read())
        self.setObjectName("maininter")

        self.main_vbox = QVBoxLayout()
        self.setLayout(self.main_vbox)

        self.main_area_hbox = QHBoxLayout()

        self.study_nsl_pht = QPixmap(os.path.join(
            paths.IMAGE, "study_not_selected.png")).scaled(MainInter.STUDY_IMAGE_WIDTH, MainInter.STUDY_IMAGE_HEIGHT)
        self.study_sl_pht = QPixmap(os.path.join(
            paths.IMAGE, "study_selected.png")).scaled(MainInter.STUDY_IMAGE_WIDTH, MainInter.STUDY_IMAGE_HEIGHT)
        self.study_slg_pht = QPixmap(os.path.join(
            paths.IMAGE, "study_selecting.png")).scaled(MainInter.STUDY_IMAGE_WIDTH, MainInter.STUDY_IMAGE_HEIGHT)
        self.study_phts = {"not_selected": self.study_nsl_pht,
                           "selected": self.study_sl_pht,
                           "selecting": self.study_slg_pht}
        self.study_pht_btn = QPushLabel(self, self.study_phts)

        self.setting_nsl_pht = QPixmap(os.path.join(
            paths.IMAGE, "setting_not_selected.png")).scaled(MainInter.SETTING_IMAGE_WIDTH, MainInter.SETTING_IMAGE_HEIGHT, Qt.KeepAspectRatio)
        self.setting_sl_pht = QPixmap(os.path.join(
            paths.IMAGE, "setting_selected.png")).scaled(MainInter.SETTING_IMAGE_WIDTH, MainInter.SETTING_IMAGE_HEIGHT, Qt.KeepAspectRatio)
        self.setting_slg_pht = QPixmap(os.path.join(
            paths.IMAGE, "setting_selecting.png")).scaled(MainInter.SETTING_IMAGE_WIDTH, MainInter.SETTING_IMAGE_HEIGHT, Qt.KeepAspectRatio)
        self.setting_phts = {"not_selected": self.setting_nsl_pht,
                             "selected": self.setting_sl_pht,
                             "selecting": self.setting_slg_pht}
        self.setting_pht_btn = QPushLabel(self, self.setting_phts)

        self.btn_and_frame_list = [(self.study_pht_btn, self.study_widget
                                    ), (self.setting_pht_btn, self.setting_widget)]

        self.init_btn_and_frame()

        self.bottom_frame = QFrame()
        self.bottom_frame.setObjectName("bottom_frame")
        self.bottom_frame.setContentsMargins(0, 0, 0, 0)
        self.bottom_hbox = QHBoxLayout()
        self.bottom_frame.setLayout(self.bottom_hbox)

        self.bottom_hbox.addStretch(2)
        self.bottom_hbox.addWidget(self.study_pht_btn)
        self.bottom_hbox.addStretch(1)
        self.bottom_hbox.addWidget(self.setting_pht_btn)
        self.bottom_hbox.addStretch(2)

        self.main_vbox.addLayout(self.main_area_hbox)
        self.main_vbox.addWidget(self.bottom_frame)
        self.main_vbox.setContentsMargins(0, 0, 0, 0)

        self.show()

    def init_btn_and_frame(self):
        for btn, _ in self.btn_and_frame_list:
            btn.released.connect(self.choose)
            btn.pressed.connect(self._switch_color)
        self.btn_and_frame_list[0][0].have_selected()
        self.main_area_hbox.addWidget(self.btn_and_frame_list[0][1]())

    def clear(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if isinstance(item, QWidgetItem):
                item.widget().close()
            elif isinstance(item, QSpacerItem):
                continue
            else:
                self.clear(item.layout())

    def choose(self):
        sender = self.sender()
        for btn, frame in self.btn_and_frame_list:
            if btn == sender:
                self.clear(self.main_area_hbox)
                self.main_area_hbox.addWidget(frame())
                continue
            btn.cancel()

    def _switch_color(self):
        sender = self.sender()
        for btn, frame in self.btn_and_frame_list:
            if btn == sender:
                continue
            btn.cancel()

    def study_widget(self):
        study = Study(_areas, _info_list)
        study.setContentsMargins(0, 0, 0, 0)
        return study

    def setting_widget(self):
        return QWidget(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainInter()
    w.setGeometry(0, 0, 725, 825)
    sys.exit(app.exec_())
