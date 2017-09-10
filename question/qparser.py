import question


class Finder:

    def __init__(self, path):
        self.path = path
        self.area_list = self.load()

    def load(self):
        return question.load(self.path)