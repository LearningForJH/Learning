import datetime
import uuid
import socket


def get_localip():
    s = socket.socket()
    s.connect(("www.baidu.com", 80))
    localip = s.getsockname()[0]
    return localip


def get_stime():
    tnow = datetime.datetime.now()
    return tnow.strftime("%Y-%m-%d %H:%M")


def get_mac():
    return hex(uuid.getnode())[-12:]
