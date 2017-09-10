import datetime
import uuid


def get_stime():
    tnow = datetime.datetime.now()
    return tnow.strftime("%Y-%m-%d %H:%M")


def get_mac():
    return hex(uuid.getnode())[-12:]
