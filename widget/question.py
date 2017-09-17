import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QLabel, QPushButton, QProgressBar, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal
from displayed import CDisplayFrame
from base import BaseWidget
import paths


class Question(BaseWidget):

	title = "题目"
	icon = "question.png"

	submit = pyqtSignal(bool)

	def __init__(self, question, progress, master=None):
		super().__init__(master, Question.title, Question.icon)
		self.question = question
		self.progress = progress
		self.build_inter()

	def build_inter(self):
		with open("question.qss") as f:
			self.setStyleSheet(f.read())

		self.setObjectName("question_main")

		self.main_vbox = QVBoxLayout()
		self.setLayout(self.main_vbox)

		self.prg_bar = QProgressBar(self.title_frame)
		self.prg_bar.setObjectName("progress_bar")
		self.prg_bar.setRange(1, self.progress[0])
		self.prg_bar.setValue(self.progress[1])
		self.prg_bar.setFixedWidth(self.width() * 75 / 100)
		self.prg_bar.setFormat("{}/{}".format(self.progress[1], self.progress[0]))
		self.main_vbox.addWidget(self.prg_bar)

		self.qst_content = CDisplayFrame(self.question.content, qss=open("qstc.qss").read())
		self.main_vbox.addWidget(self.qst_content)

		options = self.question.options()
		if options:
			self.qst_option_frame = QFrame()
			for option in options:
				pass

		self.main_vbox.addWidget(self.prg_bar)

		self.show()

	def press_submit(self):
		pass


if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = Question(None)
	w.resize(460, 733)
	sys.exit(app.exec_())