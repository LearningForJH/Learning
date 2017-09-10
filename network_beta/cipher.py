from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Hash import MD5


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

    def compare(self, msg):
        temp = CipherMD5()
        temp.update(msg)
        if temp.get_md5() == self.get_md5():
            return True
        return False


class CipherRSA:

    def __init__(self, length):
        self._rsa = RSA.generate(length)

    def encrypt(self, msg):
        cipher = PKCS1_OAEP.new(self._rsa)
        cip_msg = cipher.encrypt(msg)
        return cip_msg

    def decrypt(self, msg):
        cipher = PKCS1_OAEP.new(self._rsa)
        con_msg = cipher.decrypt(msg)
        return con_msg

    def get_public_key(self):
        return self._rsa.n, self._rsa.e


class CipherServerRSA(CipherRSA):

    def __init__(self, n, e):
        self._rsa = RSA.RsaKey(n=n, e=e)

    def decrypt(self, *args, **kwargs):
        raise TypeError("Can't decrypt without private keys")
