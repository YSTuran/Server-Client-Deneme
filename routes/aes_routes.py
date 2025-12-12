from flask import Blueprint, render_template, request, jsonify
from cipher.aes import aes_encrypt, aes_decrypt

aes_bp = Blueprint("aes_bp", __name__, url_prefix="/aes")

SERVER_XOR_KEY = 123 

def xor_text(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)

@aes_bp.route("/", methods=["GET"])
def page():
    return render_template("aes.html")

@aes_bp.route("/send", methods=["POST"])
def send():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Beklenen JSON body yok."}), 400

    text = data.get("text", "")
    key = data.get("key", "")
    mode = data.get("mode", "encrypt")

    if mode == "encrypt":
        # text = XOR'lu plaintext
        original_text = xor_text(text, SERVER_XOR_KEY)

        if len(original_text) != 16:
            return jsonify({"error": "Metin 16 karakter olmalı!"}), 400

    if len(key) != 16:
        return jsonify({"error": "Anahtar 16 karakter olmalı."}), 400

    try:
        if mode == "encrypt":
            encrypted = aes_encrypt(original_text, key)
            return jsonify({"encrypted": encrypted})

        else:
            decrypted = aes_decrypt(text, key)
            decrypted_xor = xor_text(decrypted, SERVER_XOR_KEY)

            return jsonify({"decrypted": decrypted_xor})

    except Exception as e:
        return jsonify({"error": "AES işleme hatası", "detail": str(e)}), 500
