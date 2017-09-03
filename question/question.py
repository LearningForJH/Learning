import base64
import pickle


class Element:
    TEXT = 0
    IMAGE = 1

    def __init__(self, etype):
        self.etype = etype


class Text(Element):

    def __init__(self, text):
        super().__init__(Element.TEXT)
        self.text = text


class Image(Element):

    def __init__(self, content):
        super().__init__(Element.IMAGE)
        self.content = content


class Content:

    def __init__(self, elements_set):
        self.content = elements_set


class Choice:

    def __init__(self, content):
        self.content = content


class Choices:

    def __init__(self, choices):
        self.choices = choices


class Question:
    BLANK_FILLING = 0
    MULTIPLE_CHOICING = 1

    def __init__(self, qtype, content, answer):
        self.qtype = qtype
        self.content = content
        self.answer = answer

    def check(self, answer, exact=False):
        if not exact:
            if answer.upper() == self.answer.upper():
                return True
        else:
            if answer == self.answer:
                return True
        return False


class BlankFilling(Question):

    def __init__(self, content, answer):
        super().__init__(Question.BLANK_FILLING, content, answer)


class MultipleChoicing(Question):

    def __init__(self, content, answer, choices):
        super().__init__(Question.MULTIPLE_CHOICING, content, answer)
        self.choices = choices

ALL = "all"


def load_all(fpath):
    with open(fpath, "rb") as f:
        cipher = f.read()
    content = base64.decodestring(cipher)
    unpickled = [pickle.loads(obj + b".") for obj in content.split(b".") if obj]
    return unpickled
