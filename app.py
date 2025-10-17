from flask import Flask, request, jsonify, render_template
import socket
import random
import numpy as np
from typing import List, Dict

app = Flask(__name__)
INBOX: List[Dict] = []


# --------------------------- Şifreleme Fonksiyonları --------------------------- #

def caesar_encrypt(plain: str, shift: int) -> str:
    result = []
    for ch in plain:
        if 'a' <= ch <= 'z':
            result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= ch <= 'Z':
            result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(ch)
    return ''.join(result)


def caesar_decrypt(cipher: str, shift: int) -> str:
    return caesar_encrypt(cipher, -shift)


def vigenere_encrypt(plain: str, key: str) -> str:
    if not key:
        return plain
    res, j = [], 0
    for ch in plain:
        if ch.isalpha():
            shift = ord(key[j % len(key)].lower()) - ord('a')
            base = ord('a') if ch.islower() else ord('A')
            res.append(chr((ord(ch) - base + shift) % 26 + base))
            j += 1
        else:
            res.append(ch)
    return ''.join(res)


def vigenere_decrypt(cipher: str, key: str) -> str:
    if not key:
        return cipher
    res, j = [], 0
    for ch in cipher:
        if ch.isalpha():
            shift = ord(key[j % len(key)].lower()) - ord('a')
            base = ord('a') if ch.islower() else ord('A')
            res.append(chr((ord(ch) - base - shift) % 26 + base))
            j += 1
        else:
            res.append(ch)
    return ''.join(res)


def rail_fence_encrypt(plain: str, rails: int) -> str:
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
    return res


def substitution_encrypt(plain: str, key: str) -> str:
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    key = key.lower()
    if len(key) != 26 or len(set(key)) != 26:
        raise ValueError("Anahtar 26 harf içermeli ve tekrarsız olmalı")
    table = str.maketrans(alphabet + alphabet.upper(), key + key.upper())
    return plain.translate(table)


def substitution_decrypt(cipher: str, key: str) -> str:
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    key = key.lower()
    if len(key) != 26 or len(set(key)) != 26:
        raise ValueError("Anahtar 26 harf içermeli ve tekrarsız olmalı")
    table = str.maketrans(key + key.upper(), alphabet + alphabet.upper())
    return cipher.translate(table)


# --------------------------- Hill Cipher Fonksiyonları --------------------------- #

def mod_inverse(a: int, m: int) -> int:
    """Modüler tersini bulur"""
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Matrisin determinantı modüler ters alınamaz (det ≡ 0 mod 26)")


def hill_encrypt(plain: str, key_matrix: List[List[int]]) -> str:
    plain = plain.replace(" ", "").lower()
    while len(plain) % len(key_matrix) != 0:
        plain += 'x'  # eksikse x ile doldur

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
    key_matrix_inv = (
        det_inv * np.round(det * np.linalg.inv(key_matrix)).astype(int)
    ) % 26

    result = ''
    for i in range(0, len(cipher), n):
        block = [ord(ch) - ord('a') for ch in cipher[i:i+n]]
        plain_block = np.dot(key_matrix_inv, block) % 26
        result += ''.join(chr(int(num) + ord('a')) for num in plain_block)
    return result


# --------------------------- Flask Rotaları --------------------------- #

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

    try:
        if method == 'caesar':
            shift = int(key) if str(key).isdigit() else 3
            result = caesar_encrypt(message, shift) if mode == 'encrypt' else caesar_decrypt(message, shift)
            reverse = caesar_decrypt(result, shift) if mode == 'encrypt' else caesar_encrypt(result, shift)

        elif method == 'vigenere':
            result = vigenere_encrypt(message, key) if mode == 'encrypt' else vigenere_decrypt(message, key)
            reverse = vigenere_decrypt(result, key) if mode == 'encrypt' else vigenere_encrypt(result, key)

        elif method in ['rail', 'railfence', 'rail-fence']:
            rails = int(key) if str(key).isdigit() and int(key) > 0 else 3
            result = rail_fence_encrypt(message, rails) if mode == 'encrypt' else rail_fence_decrypt(message, rails)
            reverse = rail_fence_decrypt(result, rails) if mode == 'encrypt' else rail_fence_encrypt(result, rails)

        elif method == 'substitution':
            encrypted = substitution_encrypt(message, key)
            decrypted = substitution_decrypt(encrypted, key)
            INBOX.append({"plain": message, "encrypted": encrypted, "decrypted": decrypted, "method": "substitution", "key": key})
            return jsonify({"encrypted": encrypted, "decrypted": decrypted, "method": "substitution"})

        elif method == 'hill':
            # Örnek: key = "3,3,2,5" => [[3,3],[2,5]]
            try:
                key_numbers = [int(x) for x in key.split(',')]
                size = int(len(key_numbers) ** 0.5)
                if size * size != len(key_numbers):
                    raise ValueError("Anahtar kare matris olmalı (örneğin 2x2 = 4 sayı)")
                key_matrix = np.array(key_numbers).reshape(size, size)
            except:
                raise ValueError("Anahtar formatı hatalı. Örnek: '3,3,2,5' (2x2 matris için)")

            if mode == 'encrypt':
                result = hill_encrypt(message, key_matrix)
                reverse = hill_decrypt(result, key_matrix)
            else:
                result = hill_decrypt(message, key_matrix)
                reverse = hill_encrypt(result, key_matrix)

        else:
            return jsonify({"error": "Bilinmeyen yöntem"}), 400

        INBOX.append({"plain": message, "result": result, "reverse": reverse, "method": method, "mode": mode, "key": key})
        return jsonify({"result": result, "reverse": reverse})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    local_ip = socket.gethostbyname(socket.gethostname())
    port = random.randint(5000, 9000)
    print(f"Uygulama {local_ip}:{port} adresinde çalışıyor...")
    app.run(debug=True, host=local_ip, port=port)
