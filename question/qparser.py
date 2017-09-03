import os
import random
import question


class Finder:
	# CTS(Cascading Tags Sheets)
	STD_CTS = ("学科", "分类", "难度")

    def __init__(self, path, base_path):
        self.path = path
        self.base_path = base_path
        self.finded = self.find()

    def find(self, std_cts=Finder.STD_CTS):
        file_list = os.listdir(self.path)
        splitted = [fname.split(".") for fname in file_list]
        full_splitted += std_cts
        arranged = [item[index]
                    for index in range(len(std_cts)) for item in full_splitted]
        return arranged

    def load_file(self, cts, num):
        full_path = os.path.join(self.base_path, ".".join(cts))
        if not os.path.isfile(full_path):
            return list()
        questions = list(question.load_all(full_path))
        if num == question.ALL:
            return questions
        else:
            length = len(questions)
            if num >= length:
                return questions
            else:
                return self.choose(questions, length, num)

    def choose(self, questions, length, num):
        choice_len = max([num, length - num])
        temp = [questions.pop(random.randint(0, len(questions) - 1))
                for _ in range(choice_len)]
        if choice_len == num:
            return temp
        else:
            return questions
