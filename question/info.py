import pickle
import base64


class Info:

	def __init__(self, text, info=None, english=None):
		self.text = text
		self.info = info
		self.english = english


def get_all(fpath):
	with open(fpath, "rb") as f:
		cipher = f.read()
	content = base64.decodestring(cipher)
	unpickled = [pickle.loads(obj + b".") for obj in content.split(b".") if obj]
	return unpickled