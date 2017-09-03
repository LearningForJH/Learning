import os
import sys
from PyQt5.QtWidgets import QFrame, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import paths


class QShadowFrame(QFrame):

	def __init__(self, master=None, only_pressed=True):
		super().__init__(master)
		self.only_pressed = only_pressed
		self._be_pressing = False
		self.build_inter()

	def build_inter(self):
		self.init_images()

		self.main_frame = QFrame()
		self.main_frame.setAlignment(Qt.AlignCenter)
		self.main_frame.setSizePolicy(self.sizePolicy())
		self.main_frame.setContentsMargins(0, 0, 0, 0)

		self.left_lb = QLabel(self)

		self.setContentsMargins(0, 0, 0, 0)

	def init_images(self):
		self._left = Image.open(os.path.join(paths.IMAGE, "left_shadow.png"))
		self._right = left.rotate(180)
		self._top = Image.open(os.path.join(paths.IMAGE, "top_shadow.png"))
		self._bottom = top.rotate(180)
		self.left = self._left.toqpixmap()
		self.left.fill()
		self.right = self._right.toqpixmap()
		self.right.fill()
		self.top = self._top.toqpixmap()
		self.top.fill()
		self.bottom = self._bottom.toqpixmap()
		self.bottom.fill()
		self.adjust_size()

	def adjust_size(self):
		self.left = self.left.scaled(self.left.width(), self.main_frame.height() + 2 * self.top.height())
		self.right = self.right.scaled(self.left.width(), self.left.height())
		self.top = self.top.scaled(self.main_frame.width(), self.top.height())
		self.bottom = self.bottom.scaled(self.top.width(), self.top.height())

	def update_lb(self):
		self.left_lb.setPixmap(self.left)
		self.right_lb.setPixmap(self.right)
		self.top_lb.setPixmap(self.top)
		self.bottom.setPixmap(self.bottom)

	def mousePressEvent(self, *args, **kwargs):
		pass

	def resizeEvent(self):
		if self.only_pressed and not self._be_pressing:
			return
		self.adjust_size()
		self.update_lb()