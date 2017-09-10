import socket
import threading
import message
from cipher import CipherMD5, CipherRSA


class SocketProxy(threading.Thread):

    def send(self, host, port, msg, timeout=None):
        bmsg = msg.encode("utf-8") if not isinstance(msg, bytes) else msg
        s = socket.socket()
        if timeout:
            s.setdefaulttimeout(timeout)
        try :
            s.connect((host, port))
        except socket.timeout:
            return False
        except ConnectionRefusedError:
            return False
        s.sendall(bmsg)
        s.close()
        return True

    def receive(self, host, port, listen=10, timeout=None):
        s = socket.socket()
        s.bind((host, port))
        s.listen(listen)
        s.setdefaulttimeout(timeout)

        while 1:
            conn, addr = s.accept()
            recv_list.append((conn, addr))
            self.parse(conn, addr)

        s.close()
        return recv_list

    def parse(self, *args, **kwargs):
        raise NotImplementedError()


class StudentServer(SocketProxy):

    def parse(self, conn, addr):
        pass
