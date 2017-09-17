import base64
import pickle


class Element:

    def __init__(self, content):
        self.content = content

    def is_text(self):
        return True


class Text(Element):
    pass


class Image(Element):

    def is_text(self):
        return False


class Content:

    def __init__(self, elements_set):
        self.content = elements_set


class Question:

    def __init__(self, content, answer):
        self.content = content
        self.answer = answer

    def check(self, answer, exact=False):
        if not exact:
            answer = self.answer.upper()
            usr_answer = answer.upper()
        return answer == usr_answer

    def get_options(self, *args, **kwargs):
        return []

    def need_input(self, *args, **kwargs):
        return True


class BlankFilling(Question):

    def __init__(self, content, answer):
        super().__init__(content, answer)


class MultipleChoicing(Question):

    def __init__(self, content, answer, choices):
        super().__init__(content, answer)
        self._choices = choices

    def get_option(self):
        return self._choices

    def need_input(self):
        return False


class Area:
    CURR_ALL = "current_all"

    def __init__(self, name, questions):
        self.name = name
        self.questions = questions

    def _add_question(self, question, diff):
        self.questions[diff][1].append(question)

    def _add_diff(self, diff_name):
        self.questions[diff_name] = [0, []]

    def total_star(self):
        #(difficulty, stars)
        #(1, 15) (2, 20) ... (n, 10 + 5n)
        diff_rng = len(self.questions)
        return (25 * diff_rng + 5 * diff_rng ** 2) / 2

    def curr_star(self, diff):
        if diff != Area.CURR_ALL:
            return self.questions[diff][0]
        else:
            return sum(item[0] for item in self.questions.values())

    def add_star(self, star, diff):
        curr_star = self.questions[diff][0]
        if star <= curr_star:
            return
        self.questions[diff][0] = star


def load(fpath):
    with open(fpath, "rb") as f:
        cipher = f.read()
    content = base64.decodestring(cipher)
    unpickled = [pickle.loads(obj + b".")
                 for obj in content.split(b".") if obj]
    return unpickled
