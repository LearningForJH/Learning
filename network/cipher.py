from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import MD5


class CipherMD5:

    def __init__(self):
        self._md5 = MD5.new()

    def get_md5(self):
        return self._md5.hexdigest()

    def update(self, data):
        data = data.encode("utf-8") if not isinstance(data, bytes) else data
        self._md5.update(data)

    def clear(self):
        self._md5 = MD5.new()


class CipherRSA:

    def __init__(self, filename):
        with open(filename, "rb") as f:
            content = f.read()
        self._rsa = RSA.importKey(content)

    def encrypt(self, msg):
        cipher = PKCS1_OAEP.new(self._rsa)
        cip_msg = cipher.encrypt(msg)
        return cip_msg
