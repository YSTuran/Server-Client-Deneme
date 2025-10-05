from flask import Flask, request, jsonify, render_template
from typing import List, Dict

app = Flask(__name__)


INBOX: List[Dict] = []


def caesar_encrypt(plain: str, shift: int) -> str:
    result_chars = []
    for ch in plain:
        if 'a' <= ch <= 'z':
            result_chars.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= ch <= 'Z':
            result_chars.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        else:
            result_chars.append(ch)
    return ''.join(result_chars)

def vigenere_encrypt(plain: str, key: str) -> str:
    if not key:
        return plain
    res = []
    j = 0
    key = key
    for ch in plain:
        k = key[j % len(key)]
        if 'a' <= ch <= 'z':
            shift = ord(k.lower()) - ord('a')
            res.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
            j += 1
        elif 'A' <= ch <= 'Z':
            shift = ord(k.lower()) - ord('a')
            res.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.json or {}
    message = data.get('message', '')
    method = (data.get('method') or 'caesar').lower()
    key = data.get('key', '') 
    cipher_text = message

    try:
        if method == 'caesar':           
            shift = int(key) if str(key).isdigit() else 3
            cipher_text = caesar_encrypt(message, shift)

        elif method == 'vigenere':
            cipher_text = vigenere_encrypt(message, str(key))

        elif method == 'railfence' or method == 'rail-fence' or method == 'rail':
            rails = int(key) if str(key).isdigit() and int(key) > 0 else 3
            cipher_text = rail_fence_encrypt(message, rails)

        else:
            return jsonify({"error": "Bilinmeyen yöntem"}), 400

    except Exception as e:
        return jsonify({"error": "Şifreleme sırasında hata", "detail": str(e)}), 500

  
    INBOX.append({
        "plain": message,
        "cipher": cipher_text,
        "method": method,
        "meta": {"key": key}
    })

    return jsonify({"cipher": cipher_text})

@app.route('/inbox', methods=['GET'])
def inbox():
    return jsonify({"messages": INBOX[-20:]})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
