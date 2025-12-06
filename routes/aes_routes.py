from flask import Blueprint, render_template, request, jsonify
from cipher.aes import aes_encrypt, aes_decrypt

aes_bp = Blueprint("aes_bp", __name__, url_prefix="/aes")

@aes_bp.route("/", methods=["GET"])
def page():
    return render_template("aes.html")

@aes_bp.route("/send", methods=["POST"])
def send():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Beklenen JSON body yok."}), 400

    text = data.get("text", "")
    if not text:
        text = data.get("cipher", "")

    key = data.get("key", "")
    mode = data.get("mode", "encrypt")

    if not isinstance(text, str) or not isinstance(key, str):
        return jsonify({"error": "text ve key string olmalı."}), 400

    if mode == "decrypt":
        if len(text) != 32:
            return jsonify({"error": "Çözme için 32 hex karakter (16 byte) girin."}), 400
    else:
        if len(text) != 16:
            return jsonify({"error": "Metin 16 karakter olmalı."}), 400

    if len(key) != 16:
        return jsonify({"error": "Anahtar 16 karakter olmalı."}), 400

    try:
        if mode == "decrypt":
            result = aes_decrypt(text, key)
        else:
            result = aes_encrypt(text, key)
    except Exception as e:
        return jsonify({"error": "AES işleme hatası", "detail": str(e)}), 500

    if mode == "decrypt":
        return jsonify({"decrypted": result})
    else:
        return jsonify({"encrypted": result})