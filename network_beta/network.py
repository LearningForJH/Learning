import socket
import threading
import message
from cipher import CipherMD5, CipherRSA, CipherServerRSA


class SocketProxy:

    def send(self, host, port, msg, timeout=None):
        s = socket.socket()
        if timeout:
            s.setdefaulttimeout(timeout)
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            return False
        except socket.timeout:
            return False
        s.sendall(msg)
        s.close()
        return True

    def receive(self, host, port, listen, timeout=None):
        s = socket.socket()
        s.bind((host, port))
        s.listen(listen)
        if timeout:
            s.setdefaulttimeout(timeout)

        conn, addr = s.accept()
        s.close()
        return conn, addr


class StudentSocket:
    CONNECTED = 0
    DISCONNECTED = 1

    HOST = "localhost"
    PORT = 80
    MAX_LISTEN = 1

    RSA_KEY_LEN = 2048

    def __init__(self):
        self.state = Student.DISCONNECTED
        self.MD5 = None
        self.local_RSA = None
        self.server_RSA = None
        self.socket_proxy = SocketProxy()

    def __enter__(self, *args, **kwargs):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.exit()
        return self

    def start(self):
        self.init_secret_key()
        while self.state != StudentSocket.CONNECTED:
            try:
                self.connect()
            except ValueError:
                continue

    def exit(self):
        self.close_server()
        self.state = DISCONNECTED

    def close_server(self):
        disconnect = message.DisconnectMsg()
        msg = disconnect.msg
        self.send(msg)

    def init_secret_key(self):
        self.MD5 = CipherMD5()
        self.local_RSA = CipherRSA(StudentSocket.RSA_KEY_LEN)

    def connect(self):
        conn, addr = self.wait_until_connecting()
        data = conn.recv(4096)
        recv_msg = self.parse(data)
        if not recv_msg.recv_msg[0] == "Radiating":
            raise ValueError()
        n = recv_msg.recv_msg[1]["n"]
        e = recv_msg.recv_msg[1]["e"]
        self.set_server_RSA(int(n), int(e))
        self.server_host = addr[0]
        self.server_port = addr[1]
        self.state = StudentSocket.CONNECTED

    def wait_until_connecting(self, timeout=12):
        host = StudentSocket.HOST
        port = StudentSocket.PORT
        listen = StudentSocket.MAX_LISTEN
        return self.socket_proxy.receive(host, port, listen, timeout=timeout)

    def parse(self, data):
        recv_msg = message.RecvMessage()
        recv_msg.parse(data)
        return recv_msg

    def set_server_RSA(self, n, e):
        self.server_RSA = CipherServerRSA(n, e)

    def send(self, msg, timeout=12):
        md5 = self.get_md5(msg)
        msg = msg + md5
        msg = self.server_RSA.encrypt(msg)
        result = self.socket_proxy.send(self.server_host, self.server_port, msg, timeout=timeout)
        return result

    def decrypt(self, msg):
        msg = self.local_RSA.decrypt(msg)
        if self.is_tampered(msg):
            raise ValueError("The message has been tampered!")
        return self.main_content(msg)

    def is_tampered(self, msg):
        msg_md5 = msg[-32:].decode("utf-8")
        meta_msg = msg[:len(msg) - 32]
        if self.get_md5(meta_msg) == msg_md5:
            return True
        return False

    def get_md5(self, data):
        self.MD5.update(data)
        md5 = self.MD5.get_md5()
        self.MD5.clear()
        return md5

    def main_content(self, msg):
        return msg[:len(msg) - 32]
