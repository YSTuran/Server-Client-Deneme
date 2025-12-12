from flask import Blueprint, render_template, request, jsonify
from cipher.des import des_encrypt, des_decrypt

des_bp = Blueprint("des_bp", __name__)

SERVER_XOR_KEY = 123

def xor_text(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)

@des_bp.route("/des", methods=["GET"])
def page():
    return render_template("des.html")


def expand_7_to_8_key(key7: str) -> str:
    bits = "".join(f"{ord(c):07b}" for c in key7)

    result = ""
    for i in range(8):
        chunk = bits[i*7:(i+1)*7]
        ones = chunk.count("1")
        parity = "1" if ones % 2 == 0 else "0"
        result += chunk + parity

    key_bytes = [result[i:i+8] for i in range(0, 64, 8)]
    real_key = "".join(chr(int(b, 2)) for b in key_bytes)

    return real_key


@des_bp.route("/des/send", methods=["POST"])
def des_send():
    data = request.get_json() or {}
    xor_text_from_client = data.get("text", "")
    key = data.get("key", "")

    if len(xor_text_from_client) != 8:
        return jsonify({"error": "Metin 8 karakter olmalı"}), 400

    if len(key) != 7:
        return jsonify({"error": "Anahtar 7 karakter olmalı"}), 400

    try:
        original_text = xor_text(xor_text_from_client, SERVER_XOR_KEY)

        real_key = expand_7_to_8_key(key)

        encrypted = des_encrypt(original_text, real_key)

        decrypted = des_decrypt(encrypted, real_key)
        decrypted_xor = xor_text(decrypted, SERVER_XOR_KEY)

    except Exception as e:
        return jsonify({"error": f"DES hatası: {str(e)}"}), 400

    return jsonify({
        "encrypted": encrypted,
        "decrypted": decrypted_xor
    })
