import numpy as np

def prepare_text(s):
    s = s.replace(" ", "*")
    if len(s) % 2 == 1:
        s += "*"
    return s

def hill_encrypt(text, key):
    key = np.array(key).reshape(2,2)
    text = prepare_text(text)

    result = ""
    for i in range(0, len(text), 2):
        block = [ord(text[i]) - 65, ord(text[i+1]) - 65]
        res = key.dot(block) % 26
        result += chr(res[0] + 65) + chr(res[1] + 65)

    return result

def hill_decrypt(text, key):
    key = np.array(key).reshape(2,2)
    det = int(np.round(np.linalg.det(key)))
    det_inv = pow(det % 26, -1, 26)

    inv_key = det_inv * np.round(np.linalg.inv(key) * det).astype(int) % 26

    result = ""
    for i in range(0, len(text), 2):
        block = [ord(text[i]) - 65, ord(text[i+1]) - 65]
        res = inv_key.dot(block) % 26
        result += chr(res[0] + 65) + chr(res[1] + 65)

    return result.replace("*", " ")
