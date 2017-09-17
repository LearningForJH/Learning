import os
import sys
from io import BytesIO
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import paths


def get_width(text):
    return QLabel().fontMetrics().width(text)


class AgentContent:

    def __init__(self, obj, tag):
        self.obj = obj
        self.tag = tag

    def prepare(self):
        if self.tag == "text":
            lb = QLabel(self.obj)
        elif self.tag == "image":
            lb = QLabel()
            lb.setPixmap(self.obj)
        lb.setObjectName(self.tag)
        return lb


class CDisplayFrame(QFrame):

    def __init__(self, elements, qss="", master=None):
        super().__init__(master)
        self.master = master
        self.elements = elements.content
        self.qss = qss
        self.update_args()

    def build(self):
        self.setStyleSheet(self.qss)
        self.setObjectName("main")

        self.main_vbox = QVBoxLayout()
        self.setLayout(self.main_vbox)

        modr = self.max_width
        widgets = []
        elements = self.elements[:]

        while elements:
            entered_line = False
            ele = elements.pop(0)
            if ele.is_text():
                content = ele.content
                w = get_width(content)
                if w > modr:
                    separator = int(modr // self.single_width)
                    # Split extra characters into second line
                    wid = AgentContent(content[0:separator], "text")
                    ele.content = content[separator:-1] + content[-1]
                    elements.insert(0, ele)
                    modr = 0  # All spacing were used
                else:
                    wid = AgentContent(content, "text")
                    modr -= w
            else:
                #img_file = BytesIO(ele.content)
                img = QPixmap(ele.content)
                iw = img.width() * self.height / img.height()
                img = img.scaled(iw, self.height, Qt.KeepAspectRatio)
                if iw > modr:
                    if widgets:
                        wid = AgentContent(img, "image")
                        entered_line = True
                    else:
                        wid = AgentContent(img, "image")
                    modr = 0  # All spacing were used
                else:
                    wid = AgentContent(img, "image")
                    modr -= iw

            widgets.append(wid.prepare())

            if modr == 0:
                modr = self.max_width
                end_wid = widgets.pop(-1) if entered_line else None
                new_line = self.gathered_line(widgets)
                self.main_vbox.addLayout(new_line)
                widgets.clear()
                if end_wid:
                    widgets.append(end_wid)

        if widgets:
            new_line = self.gathered_line(widgets)
            self.main_vbox.addLayout(new_line)

        self.setContentsMargins(0, 0, 0, 0)

    def gathered_line(self, widgets):
        new_line = QHBoxLayout()
        for wid in widgets:
            new_line.addWidget(wid)
        new_line.addStretch(1)
        return new_line

    def update_args(self):
        self.max_width = self.master.width() if self.master else self.width()
        self.height = QLabel().fontMetrics().height()
        self.single_width = get_width("一")


class _Element:

    def __init__(self, content):
        self.content = content

    def is_text(self):
        return True


class _Text(_Element):
    pass


class _Image(_Element):

    def is_text(self):
        return False


class _Content:

    def __init__(self, elements_set):
        self.content = elements_set


STD_QSS = '''
QLabel{
    border:none;
}
'''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    text1 = _Text("岁的法国")
    #with open(os.path.join(paths.IMAGE, "study_selecting.png"), "rb") as f:
    #    image1 = _Image(f.read())
    image1 = _Image(os.path.join(paths.IMAGE, "study_selecting.png"))
    text2 = _Text("阿瑟斯"*40)
    #with open(os.path.join(paths.IMAGE, "study_not_selected.png"), "rb") as f:
    #    image2 = _Image(f.read())
    #with open(os.path.join(paths.IMAGE, "study_selected.png"), "rb") as f:
    #    image3 = _Image(f.read())
    image2 = _Image(os.path.join(paths.IMAGE, "study_not_selected.png"))
    image3 = _Image(os.path.join(paths.IMAGE, "study_selected.png"))
    content = _Content([text1, image1, image2, text2, image3])
    w = QWidget()
    w.resize(500, 500)
    frame = CDisplayFrame(content, qss=STD_QSS, master=w)
    vbox = QVBoxLayout()
    w.setLayout(vbox)
    vbox.addWidget(frame)
    frame.build()
    w.show()
    sys.exit(app.exec_())
