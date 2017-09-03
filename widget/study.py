import sys
import os
from PyQt5.QtWidgets import QApplication, QSizePolicy, QWidget, QWidgetItem, QSpacerItem, QLabel, QPushButton, QFrame, QScrollArea, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
import paths


class QPushFrame(QFrame):
	clicked = pyqtSignal()

	ARROW_WIDTH = 20
	ARROW_HEIGHT = 30

	def __init__(self, master, text, photo, info_list):
		super().__init__(master)
		self.master = master
		self.text = text
		self.photo = photo
		self.info = [
			info_obj for info_obj in info_list if info_obj.text == self.text][0]
		self.build_inter()

	def build_inter(self):
		self.setSizePolicy(self.master.sizePolicy())
		self.setObjectName("push_frame")
		self.main_hbox = QHBoxLayout()
		self.setLayout(self.main_hbox)

		self.pht_lb = QLabel(self)
		self.pht_lb.setPixmap(self.photo)
		self.pht_vbox = QVBoxLayout()
		self.pht_vbox.addWidget(self.pht_lb)

		self.intro_title = QLabel(self.text, self)
		self.intro_title.setObjectName("intro_title")
		self.intro_title.setFont(QFont("苹方-简", 22))
		temp_intro = ""
		if self.info.english:
			temp_intro += self.info.english
		if self.info.info:
			temp_intro += self.info.info
		self.intro_content = QLabel(temp_intro, self)
		self.intro_content.setObjectName("intro_content")
		self.intro_content.setFont(QFont("苹方-简", 12))
		self.content_vbox = QVBoxLayout()
		self.content_vbox.addStretch(1)
		self.content_vbox.addWidget(self.intro_title)
		self.content_vbox.addWidget(self.intro_content)
		self.content_vbox.addStretch(1)

		temp = QPixmap(os.path.join(paths.IMAGE, "arrow.png"))
		temp_pht = temp.scaled(QPushFrame.ARROW_WIDTH, QPushFrame.ARROW_HEIGHT, Qt.KeepAspectRatio)
		self.go_pht = QLabel(self)
		self.go_pht.setPixmap(temp_pht)
		self.arrow_vbox = QVBoxLayout()
		self.arrow_vbox.addWidget(self.go_pht)

		self.main_hbox.addLayout(self.pht_vbox)
		self.main_hbox.addLayout(self.content_vbox)
		self.main_hbox.addStretch(1)
		self.main_hbox.addLayout(self.arrow_vbox)

	def mouseReleaseEvent(self, event):
		self.clicked.emit()


class Study(QWidget):
	Title = "学习"
	Icon = os.path.join(paths.IMAGE, "study.png")

	TOP_ICON_WIDTH = 50
	TOP_ICON_HEIGHT = 50
	MAIN_IMAGE_WIDTH = 100
	MAIN_IMAGE_HEIGHT = 100

	def __init__(self, finded, info_list, master=None):
		super().__init__(master)
		self.master = master
		self.finded = finded
		self.info_list = info_list
		if self.master:
			self.build_master_inter()
		self.build_inter()

	def build_master_inter(self):
		self.master.setWindowTitle(Study.Title)
		self.master.setWindowIcon(Study.Icon)

	def build_inter(self):
		self.top_icons = {}
		for index, subject in enumerate(self.finded[0]):
			if index == 0:
				continue
			temp = QPixmap(os.path.join(paths.IMAGE, subject + ".png"))
			temp_icon = temp.scaled(
				Study.TOP_ICON_WIDTH, Study.TOP_ICON_HEIGHT, Qt.KeepAspectRatio)
			self.top_icons[subject] = temp_icon

		self.mid_type_icon = {}
		self.mid_frames = []
		for index, type_ in enumerate(self.finded[1]):
			if index == 0:
				continue
			temp = QPixmap(os.path.join(paths.IMAGE, type_ + ".png"))
			temp_icon = temp.scaled(
				Study.MAIN_IMAGE_WIDTH, Study.MAIN_IMAGE_HEIGHT, Qt.KeepAspectRatio)
			self.mid_type_icon[type_] = temp_icon
			push_frame = QPushFrame(self, type_, temp_icon, self.info_list)
			push_frame.clicked.connect(self.choose_type)
			self.mid_frames.append(push_frame)

		self.build_main()

		self.show()

	def build_main(self):
		with open("study.qss", "r") as f:
			self.setStyleSheet(f.read())
		self.setObjectName("study_main")

		self.main_vbox = QVBoxLayout()
		self.setLayout(self.main_vbox)

		self.top_icon_lb = QLabel(self)
		self.top_icon_lb.setPixmap(self.top_icons["数学"])

		self.top_subj_lb = QLabel("数学", self)
		self.top_subj_lb.setFont(QFont("苹方-简", 22))

		self.top_frame = QFrame(self)
		self.top_frame.setObjectName("top_frame")
		self.top_column = QHBoxLayout()
		self.top_frame.setLayout(self.top_column)
		self.top_column.addWidget(self.top_icon_lb)
		self.top_column.addStretch(4)
		self.top_column.addWidget(self.top_subj_lb)
		self.top_column.addStretch(5)
		self.top_column.setContentsMargins(0, 0, 0, 0)

		self.main_vbox.addWidget(self.top_frame)

		self._center_area = QFrame(self)
		self._center_vbox = QVBoxLayout()
		self._center_area.setLayout(self._center_vbox)

		length = len(self.mid_frames)
		for frame in self.mid_frames:
			self._center_vbox.addWidget(frame)
			self._center_vbox.addStretch(1)
		self._center_vbox.setContentsMargins(0, 0, 0, 0)

		self.scroll_center = QScrollArea(self)
		self.scroll_center.setAlignment(Qt.AlignCenter)
		self.scroll_center.setObjectName("scroll_center")
		self.scroll_center.setWidget(self._center_area)
		self.scroll_center.setContentsMargins(0, 0, 0, 0)

		self.main_vbox.addWidget(self.scroll_center)

		self.main_vbox.setContentsMargins(0, 0, 0, 0)

	def clear(self, layout):
		for i in range(layout.count()):
			item = layout.itemAt(i)
			if isinstance(item, QWidgetItem):
				item.widget().close()
			elif isinstance(item, QSpacerItem):
				continue
			else:
				self.clear(item.layout())

	def choose_type(self):
		self.clear(self.main_vbox)
		type_ = self.sender().text


class Choose(QWidget):
	choose = pyqtSignal()

	Title = "选择"
	Icon = QIcon(os.path.join(paths.IMAGE, "choose.png"))

	NULL = "null"

	def __init__(self, ch_list, master=None):
		super().__init__(master)
		self.master = master
		self.ch_type, *self.ch_list = ch_list
		if self.master:
			self.build_master_inter()
		self.build_inter()

	def build_master_inter(self):
		self.master.setWindowTitle(Choose.Title)
		self.master.setWindowIcon(Choose.Icon)

	def build_inter(self):
		self.main_vbox = QVBoxLayout()
		self.setLayout(self.main_vbox)

		self.setObjectName("choose")


class _Info:

	def __init__(self, text, info=None, english=None):
		self.text = text
		self.info = info
		self.english = english


if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = Study([["学科", "数学"], ["类型", "代数", "几何", "统计",
							  "未知", "有理数"], ["难度", "简单", "普通", "困难"]], [_Info("代数", english="Algebra"), _Info("几何", english="Geometry"), _Info("统计", english="Statistics"), _Info("未知", english="Unknown"), _Info("有理数", english="Reasonable Number")])
	w.resize(460, 733)

	sys.exit(app.exec_())
