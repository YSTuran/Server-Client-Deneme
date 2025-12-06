import numpy as np
import math

def prepare_text(text, n):
    text = text.upper().replace(" ", "")
    padding = (n - len(text) % n) % n
    text += "X" * padding
    return text

def mod_inv(a, m):
    """a * x ≡ 1 (mod m) tamsayı mod inversi"""
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Matrisin determinantı mod 26 terslenemez!")

def hill_encrypt(text, key):
    key = np.array(key)
    n = int(math.sqrt(len(key)))
    if key.size != n*n:
        raise ValueError(f"Key boyutu {n}x{n} matris için uygun değil!")
    key = key.reshape(n, n)

    text = prepare_text(text, n)
    result = ""

    for i in range(0, len(text), n):
        block = np.array([ord(c)-65 for c in text[i:i+n]])
        res = key.dot(block) % 26
        result += "".join(chr(int(x)+65) for x in res)

    return result

def hill_decrypt(text, key):
    key = np.array(key)
    n = int(math.sqrt(len(key)))
    if key.size != n*n:
        raise ValueError(f"Key boyutu {n}x{n} matris için uygun değil!")
    key = key.reshape(n, n)

    # Determinant ve tersi
    det = int(round(np.linalg.det(key))) % 26
    det_inv = mod_inv(det, 26)

    inv_key = det_inv * np.round(np.linalg.inv(key) * det).astype(int) % 26

    result = ""
    for i in range(0, len(text), n):
        block = np.array([ord(c)-65 for c in text[i:i+n]])
        res = inv_key.dot(block) % 26
        result += "".join(chr(int(x)+65) for x in res)

    return result
