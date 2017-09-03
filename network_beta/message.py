from info import get_localip, get_stime, get_mac


def tobytes(data):
    return data.encode("utf-8") if not isinstance(data, bytes) else data


class BaseMessage:
    LINE_SEPARATOR = b"\n"
    ITEM_SEPARATOR = b":"

    def __init__(self):
        self._msg = []

    def add(self, value, tag=None):
        if tag:
            self.add_item(tag, value)
        else:
            self.add_tag(value)

    def add_item(self, key, value):
        bkey = tobytes(key)
        bvalue = tobytes(value)
        self._msg.append((bkey, bvalue))

    def add_tag(self, tag):
        btag = tobytes(tag)
        self._msg.append((btag,))

    def add_empty_line(self, num=1):
        btemp = b"\n" * (num - 1)
        self.add_tag(btemp)

    def tomsg(self):
        msg_list = [BaseMessage.ITEM_SEPARATOR.join(lst) for lst in self._msg]
        bmsg = BaseMessage.LINE_SEPARATOR.join(msg_list)
        return bmsg


class Message(BaseMessage):

    def __init__(self, action):
        super().__init__()
        self.build_msg()
        self.msg = super().tomsg()
        self.action = action

    def build_msg(self):
        self.add_item("Action", self.action)
        self.add_time()
        self.add_localip()
        self.add_mac()
        self.add_empty_line()

    def add_time(self, tag="Time"):
        self.add(get_stime(), tag=tag)

    def add_localip(self, tag="LoIP"):
        self.add(get_localip(), tag=tag)

    def add_mac(self, tag="LoMac"):
        self.add(get_mac(), tag=tag)


'''
class RadiatingIPMsg(Message):

    def __init__(self, n, e):
        self.n = n
        self.e = e
        super().__init__("Radiating")

    def build_msg(self):
        super().build_msg()
        self.add_item("n", str(self.n))
        self.add_item("e", str(self.e))
'''


class ReturnLocalKeyMsg(Message):
    def __init__(self, n, e):
        self.n = n
        self.e = e
        super().__init__("ReturnLocalKey")

    def build_msg(self):
        super().build_msg()
        self.add_item("n", str(self.n))
        self.add_item("e", str(self.e))


class ExchangeMsg(Message):

    def __init__(self, star, object_):
        self.star = star
        self.object_ = object_
        super().__init__("Exchange")

    def build_msg(self):
        super().build_msg()
        self.add_item("Stars", self.stars)
        self.add_item("Object", self.object_)


class DisconnectMsg(Message):

    def __init__(self):
        super().__init__("Disconnect")


class RecvMessage(BaseMessage):

    def __init__(self):
        self.meta_msg = b""
        self.recv_msg = ([], {})

    def parse(self, bmsg):
        self.meta_msg = bmsg
        msg = bmsg.decode("utf-8")
        lines = msg.split(BaseMessage.LINE_SEPARATOR)
        for line in lines:
            if not line:
                continue
            temp = line.split(BaseMessage.ITEM_SEPARATOR)
            length = len(temp)
            if length == 2:
                key, value = temp
                self.recv_msg[1][key] = value
            elif length == 1:
                self.recv_msg[0].append(temp)
            else :
                raise ValueError()
