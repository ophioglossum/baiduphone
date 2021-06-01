import base64
from Crypto.Cipher import PKCS1_v1_5
import hashlib
from Crypto.PublicKey import RSA
from config import app

"""
公钥签名
return base64加密字符串
"""
def EnRsaPublic(enstr):
    rsakey = RSA.importKey(app.RSA_PUBLIC_KEY)
    cipher = PKCS1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(enstr.encode('utf8')))
    return cipher_text.decode('utf8')

def EnMd5(enstr):
    m = hashlib.md5()
    m.update(enstr.encode('utf8'))
    return m.hexdigest()