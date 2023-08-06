# -*- coding: utf-8 -*-

import base64
import json

from Crypto.Cipher import AES


# Decrypt Algorithm
#   See: https://open.feishu.cn/document/uYjL24iN/ugjMx4COyEjL4ITM


def decrypt(session_key, encrypted_data, iv):
    session_key = session_key.decode('hex')
    iv = iv.decode('hex')
    encrypted_data = base64.b64decode(encrypted_data)
    decipher = AES.new(session_key, AES.MODE_CBC, iv)
    decrypted_data = decipher.decrypt(encrypted_data)
    unpad = lambda s: s[0:-ord(s[-1])]
    decodedMessage = unpad(decrypted_data)
    data = json.loads(decodedMessage)
    return data
