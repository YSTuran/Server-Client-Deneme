from flask import Flask, request, jsonify, render_template
import socket
import random
import numpy as np
from typing import List, Dict

app = Flask(__name__)
INBOX: List[Dict] = []


def caesar_encrypt(plain: str, shift: int) -> str:
    result = []
    for ch in plain:
        if 'a' <= ch <= 'z':
            result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= ch <= 'Z':
            result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        elif ch == ' ':
            result.append('*')
        else:
            result.append(ch)
    return ''.join(result)

def caesar_decrypt(cipher: str, shift: int) -> str:
    result = []
    for ch in cipher:
        if 'a' <= ch <= 'z':
            result.append(chr((ord(ch) - ord('a') - shift) % 26 + ord('a')))
        elif 'A' <= ch <= 'Z':
            result.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
        elif ch == '*':
            result.append(' ')
        else:
            result.append(ch)
    return ''.join(result)

def vigenere_encrypt(plain: str, key: str) -> str:
    if not key:
        return plain
    res, j = [], 0
    for ch in plain:
        if ch == ' ':
            res.append('*')
        elif ch.isalpha():
            shift = ord(key[j % len(key)])
            if ch.isupper():
                res.append(chr((ord(ch) - 65 + (shift - 65 if key[j % len(key)].isupper() else shift - 97)) % 26 + 65))
            else:
                res.append(chr((ord(ch) - 97 + (shift - 65 if key[j % len(key)].isupper() else shift - 97)) % 26 + 97))
            j += 1
        else:
            res.append(ch)
    return ''.join(res)

def vigenere_decrypt(cipher: str, key: str) -> str:
    if not key:
        return cipher
    res, j = [], 0
    for ch in cipher:
        if ch == '*':
            res.append(' ')
        elif ch.isalpha():
            shift = ord(key[j % len(key)])
            if ch.isupper():
                res.append(chr((ord(ch) - 65 - (shift - 65 if key[j % len(key)].isupper() else shift - 97)) % 26 + 65))
            else:
                res.append(chr((ord(ch) - 97 - (shift - 65 if key[j % len(key)].isupper() else shift - 97)) % 26 + 97))
            j += 1
        else:
            res.append(ch)
    return ''.join(res)

def rail_fence_encrypt(plain: str, rails: int) -> str:
    plain = plain.replace(' ', '*')
    if rails <= 1:
        return plain
    fence = [''] * rails
    rail, direction = 0, 1
    for ch in plain:
        fence[rail] += ch
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    return ''.join(fence)

def rail_fence_decrypt(cipher: str, rails: int) -> str:
    if rails <= 1:
        return cipher
    pattern, rail, direction = [], 0, 1
    for _ in cipher:
        pattern.append(rail)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    fence, pos = [''] * rails, 0
    for r in range(rails):
        for i in range(len(cipher)):
            if pattern[i] == r:
                fence[r] += cipher[pos]
                pos += 1
    res = ''
    for i in range(len(cipher)):
        res += fence[pattern[i]][0]
        fence[pattern[i]] = fence[pattern[i]][1:]
    return res.replace('*', ' ')

def substitution_encrypt(plain: str, key: str) -> str:
    alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
    alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if len(key) != 26 or len(set(key.lower())) != 26:
        raise ValueError("Anahtar 26 harf içermeli ve tekrarsız olmalı")
    table = str.maketrans(alphabet_lower + alphabet_upper, key.lower() + key.upper())
    text = plain.replace(' ', '*')
    return text.translate(table)

def substitution_decrypt(cipher: str, key: str) -> str:
    alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
    alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if len(key) != 26 or len(set(key.lower())) != 26:
        raise ValueError("Anahtar 26 harf içermeli ve tekrarsız olmalı")
    table = str.maketrans(key.lower() + key.upper(), alphabet_lower + alphabet_upper)
    text = cipher.translate(table)
    return text.replace('*', ' ')

def mod_inverse(a: int, m: int) -> int:
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Matrisin determinantı modüler ters alınamaz")

def hill_encrypt(plain: str, key_matrix: List[List[int]]) -> str:
    plain = plain.replace(" ", "").lower()
    while len(plain) % len(key_matrix) != 0:
        plain += 'x'
    n = len(key_matrix)
    result = ''
    for i in range(0, len(plain), n):
        block = [ord(ch) - ord('a') for ch in plain[i:i+n]]
        cipher_block = np.dot(key_matrix, block) % 26
        result += ''.join(chr(int(num) + ord('a')) for num in cipher_block)
    return result

def hill_decrypt(cipher: str, key_matrix: List[List[int]]) -> str:
    n = len(key_matrix)
    det = int(round(np.linalg.det(key_matrix))) % 26
    det_inv = mod_inverse(det, 26)
    key_matrix_inv = (det_inv * np.round(det * np.linalg.inv(key_matrix)).astype(int)) % 26
    result = ''
    for i in range(0, len(cipher), n):
        block = [ord(ch) - ord('a') for ch in cipher[i:i+n]]
        plain_block = np.dot(key_matrix_inv, block) % 26
        result += ''.join(chr(int(num) + ord('a')) for num in plain_block)
    return result

def polybius_encrypt(plain: str) -> str:
    square = [['A','B','C','D','E'],
              ['F','G','H','I','K'],
              ['L','M','N','O','P'],
              ['Q','R','S','T','U'],
              ['V','W','X','Y','Z']]
    result = []
    for ch in plain.upper():
        if ch == ' ':
            result.append('*')
        elif ch == 'J': 
            ch = 'I'
        found = False
        for i in range(5):
            for j in range(5):
                if square[i][j] == ch:
                    result.append(f"{i+1}{j+1}")
                    found = True
                    break
            if found: break
    return ' '.join(result)

def polybius_decrypt(cipher: str) -> str:
    square = [['A','B','C','D','E'],
              ['F','G','H','I','K'],
              ['L','M','N','O','P'],
              ['Q','R','S','T','U'],
              ['V','W','X','Y','Z']]
    result = ''
    cipher = cipher.replace(' ', '')
    i = 0
    while i < len(cipher):
        if cipher[i] == '*':
            result += ' '
            i += 1
        else:
            row, col = int(cipher[i]) - 1, int(cipher[i+1]) - 1
            result += square[row][col]
            i += 2
    return result

def columnar_encrypt(plain: str, key: str) -> str:
    plain = plain.replace(' ', '*')
    key_order = sorted([(ch, i) for i, ch in enumerate(key)])
    n_cols = len(key)
    n_rows = int(np.ceil(len(plain) / n_cols))
    matrix = [['*'] * n_cols for _ in range(n_rows)]
    k = 0
    for i in range(n_rows):
        for j in range(n_cols):
            if k < len(plain):
                matrix[i][j] = plain[k]
                k += 1
    result = ''
    for _, j in key_order:
        for i in range(n_rows):
            result += matrix[i][j]
    return result

def columnar_decrypt(cipher: str, key: str) -> str:
    n_cols = len(key)
    n_rows = int(np.ceil(len(cipher) / n_cols))
    key_order = sorted([(ch, i) for i, ch in enumerate(key)])
    matrix = [[''] * n_cols for _ in range(n_rows)]
    k = 0
    for _, j in key_order:
        for i in range(n_rows):
            if k < len(cipher):
                matrix[i][j] = cipher[k]
                k += 1
    result = ''.join(matrix[i][j] for i in range(n_rows) for j in range(n_cols))
    return result.replace('*', ' ')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.json or {}
    message = data.get('message', '')
    method = (data.get('method') or 'caesar').lower()
    key = data.get('key', '')
    mode = (data.get('mode') or 'encrypt').lower()

    result = ""
    reverse = ""

    try:
        if method == 'caesar':
            shift = int(key) if str(key).isdigit() else 3
            if mode == 'encrypt':
                result = caesar_encrypt(message, shift)
                reverse = caesar_decrypt(result, shift)
            else:
                result = caesar_decrypt(message, shift)
                reverse = caesar_encrypt(result, shift)

        elif method == 'vigenere':
            if mode == 'encrypt':
                result = vigenere_encrypt(message, key)
                reverse = vigenere_decrypt(result, key)
            else:
                result = vigenere_decrypt(message, key)
                reverse = vigenere_encrypt(result, key)

        elif method in ['rail', 'railfence', 'rail-fence']:
            rails = int(key) if str(key).isdigit() and int(key) > 0 else 3
            if mode == 'encrypt':
                result = rail_fence_encrypt(message, rails)
                reverse = rail_fence_decrypt(result, rails)
            else:
                result = rail_fence_decrypt(message, rails)
                reverse = rail_fence_encrypt(result, rails)

        elif method == 'substitution':
            if mode == 'encrypt':
                result = substitution_encrypt(message, key)
                reverse = substitution_decrypt(result, key)
            else:
                result = substitution_decrypt(message, key)
                reverse = substitution_encrypt(result, key)

        elif method == 'hill':
            key_numbers = [int(x) for x in key.split(',')]
            size = int(len(key_numbers) ** 0.5)
            if size * size != len(key_numbers):
                raise ValueError("Anahtar kare matris olmalı")
            key_matrix = np.array(key_numbers).reshape(size, size)
            if mode == 'encrypt':
                result = hill_encrypt(message, key_matrix)
                reverse = hill_decrypt(result, key_matrix)
            else:
                result = hill_decrypt(message, key_matrix)
                reverse = hill_encrypt(result, key_matrix)

        elif method == 'polybius':
            if mode == 'encrypt':
                result = polybius_encrypt(message)
                reverse = polybius_decrypt(result)
            else:
                result = polybius_decrypt(message)
                reverse = polybius_encrypt(result)

        elif method in ['columnar', 'columnar transposition']:
            if mode == 'encrypt':
                result = columnar_encrypt(message, key)
                reverse = columnar_decrypt(result, key)
            else:
                result = columnar_decrypt(message, key)
                reverse = columnar_encrypt(result, key)

        else:
            return jsonify({"error": "Bilinmeyen yöntem"}), 400

        INBOX.append({
            "plain": message,
            "result": result,
            "reverse": reverse,
            "method": method,
            "mode": mode,
            "key": key
        })

        return jsonify({"result": result, "reverse": reverse})

    except Exception as e:
        return jsonify({"error": str(e)}), 400



@app.route('/caesar')
def caesar():
    return render_template('caesar.html')

@app.route('/railfence')
def railfence():
    return render_template('railfence.html')

@app.route('/substitution')
def substitution():
    return render_template('substitution.html')

@app.route('/hill')
def hill():
    return render_template('hill.html')

@app.route('/polybius')
def polybius():
    return render_template('polybius.html')

@app.route('/columnar')
def columnar():
    return render_template('columnar.html')


if __name__ == '__main__':
    local_ip = socket.gethostbyname(socket.gethostname())
    port = random.randint(5000, 9000)
    print(f"Uygulama {local_ip}:{port} adresinde çalışıyor...")
    app.run(debug=True, host=local_ip, port=port)
