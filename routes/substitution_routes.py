from flask import Blueprint, render_template, request, jsonify
from cipher.substitution import substitution_encrypt, substitution_decrypt

substitution_bp = Blueprint("substitution_bp", __name__)

SERVER_XOR_KEY = 123

def xor_text(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)

@substitution_bp.route("/substitution", methods=["GET"])
def page():
    return render_template("substitution.html")

@substitution_bp.route("/substitution/send", methods=["POST"])
def substitution_send():
    data = request.get_json()
    xor_text_from_client = data.get("text", "").strip()
    key = data.get("key", "").strip()

    if not xor_text_from_client or len(key) != 26:
        return jsonify({"error": "Metin boş olamaz ve anahtar 26 karakter olmalı"}), 400

    try:
        original_text = xor_text(xor_text_from_client, SERVER_XOR_KEY)

        encrypted = substitution_encrypt(original_text, key)
        decrypted = substitution_decrypt(encrypted, key)

        decrypted_xor = xor_text(decrypted, SERVER_XOR_KEY)

    except Exception as e:
        return jsonify({"error": f"Şifreleme hatası: {str(e)}"}), 400

    return jsonify({
        "encrypted": encrypted,
        "decrypted": decrypted_xor
    })
