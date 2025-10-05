from flask import Flask, request, jsonify, render_template
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
        else:
            result.append(ch)
    return ''.join(result)

def caesar_decrypt(cipher: str, shift: int) -> str:
    return caesar_encrypt(cipher, -shift)


def vigenere_encrypt(plain: str, key: str) -> str:
    if not key:
        return plain
    res = []
    j = 0
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
    res = []
    j = 0
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
    rail = 0
    direction = 1
    for ch in plain:
        fence[rail] += ch
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    return ''.join(fence)

def rail_fence_decrypt(cipher: str, rails: int) -> str:
    if rails <= 1:
        return cipher
    pattern = []
    rail, direction = 0, 1
    for _ in cipher:
        pattern.append(rail)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    fence = [''] * rails
    pos = 0
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
    table = str.maketrans(alphabet + alphabet.upper(),
                          key + key.upper())
    return plain.translate(table)

def substitution_decrypt(cipher: str, key: str) -> str:
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    key = key.lower()
    if len(key) != 26 or len(set(key)) != 26:
        raise ValueError("Anahtar 26 harf içermeli ve tekrarsız olmalı")
    table = str.maketrans(key + key.upper(),
                          alphabet + alphabet.upper())
    return cipher.translate(table)



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
            INBOX.append({
                "plain": message,
                "encrypted": encrypted,
                "decrypted": decrypted,
                "method": "substitution",
                "key": key
            })
            return jsonify({
                "encrypted": encrypted,
                "decrypted": decrypted,
                "method": "substitution"
            })

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


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
