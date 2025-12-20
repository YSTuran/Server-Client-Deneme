import numpy as np
import math

ALPHABET_SIZE = 26

def prepare_text(text, n):
    text = text.upper()
    text = "".join(c for c in text if c.isalpha())
    padding = (n - len(text) % n) % n
    text += "X" * padding
    return text

def mod_inverse(a, m):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Determinant terslenemez")

def hill_encrypt(text, key):
    key = np.array(key)
    n = int(math.sqrt(len(key)))
    key = key.reshape(n, n)

    text = prepare_text(text, n)
    result = ""

    for i in range(0, len(text), n):
        block = np.array([ord(c) - 65 for c in text[i:i+n]])
        res = key.dot(block) % ALPHABET_SIZE
        result += "".join(chr(int(x) + 65) for x in res)

    return result

def hill_decrypt(text, key):
    key = np.array(key)
    n = int(math.sqrt(len(key)))
    key = key.reshape(n, n)

    det = int(round(np.linalg.det(key))) % ALPHABET_SIZE
    det_inv = mod_inverse(det, ALPHABET_SIZE)

    adj = np.round(det * np.linalg.inv(key)).astype(int)
    inv_key = (det_inv * adj) % ALPHABET_SIZE

    result = ""

    for i in range(0, len(text), n):
        block = np.array([ord(c) - 65 for c in text[i:i+n]])
        res = inv_key.dot(block) % ALPHABET_SIZE
        result += "".join(chr(int(x) + 65) for x in res)

    return result
