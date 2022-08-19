

from pyDes import des, CBC, PAD_PKCS5,ECB
import binascii

# 秘钥
KEY = "ctpstp@custominfo!@#qweASD"
# KEY = "ctpstp@c"

def des_encrypt(s):
    """
    DES 加密
    :param s: 原始字符串
    :return: 加密后字符串，16进制
    """
    secret_key = KEY  # 密码
    iv = secret_key  # 偏移
    # secret_key:加密密钥，CBC:加密模式，iv:偏移, padmode:填充
    des_obj = des(key=secret_key, mode=ECB, IV=iv, pad=None, padmode=PAD_PKCS5)
    # 返回为字节
    secret_bytes = des_obj.encrypt(s, padmode=PAD_PKCS5)
    # 返回为16进制
    return binascii.b2a_hex(secret_bytes)


def des_descrypt(s):
    """
    DES 解密
    :param s: 加密后的字符串，16进制
    :return:  解密后的字符串
    """
    secret_key = KEY
    iv = secret_key
    des_obj = des(key=secret_key, mode=ECB, IV=iv, pad=None, padmode=PAD_PKCS5)
    decrypt_str = des_obj.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return decrypt_str

# text = 'zhanglei'
# a = des_encrypt(text)
# print(a)
# print(des_descrypt(a))

data = "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"

print(des_descrypt(data))


# from pyDes import des, ECB, PAD_PKCS5
# import base64
#
# DES_SECRET_KEY = '12345678'
# s = "zhanglei"
# des_obj = des(DES_SECRET_KEY, ECB, DES_SECRET_KEY, padmode=PAD_PKCS5)
# des_bytes = des_obj.encrypt(s.encode('utf-8'))
# base64_result = str(base64.b64encode(des_bytes), encoding = 'utf-8')
# print(base64_result)
# hex_result = des_bytes.hex()
# print(hex_result)