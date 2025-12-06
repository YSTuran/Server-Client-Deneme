from flask import Blueprint, render_template, request, jsonify
from cipher.substitution import substitution_encrypt, substitution_decrypt

substitution_bp = Blueprint("substitution_bp", __name__)

@substitution_bp.route("/substitution", methods=["GET"])
def page():
    return render_template("substitution.html")

@substitution_bp.route("/substitution/send", methods=["POST"])
def substitution_send():
    data = request.get_json()
    text = data.get("text", "").strip()
    key = data.get("key", "").strip()

    if not text or len(key) != 26:
        return jsonify({"error": "Metin boş olamaz ve anahtar 26 karakter olmalı"}), 400

    try:
        encrypted = substitution_encrypt(text, key)
        decrypted = substitution_decrypt(encrypted, key)
    except Exception as e:
        return jsonify({"error": f"Şifreleme hatası: {str(e)}"}), 400

    return jsonify({"encrypted": encrypted, "decrypted": decrypted})
