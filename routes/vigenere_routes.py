from flask import Blueprint, render_template, request, jsonify
from cipher.vigenere import vigenere_encrypt, vigenere_decrypt

vigenere_bp = Blueprint("vigenere_bp", __name__)

@vigenere_bp.route("/vigenere", methods=["GET"])
def page():
    return render_template("vigenere.html")

@vigenere_bp.route("/vigenere/send", methods=["POST"])
def vigenere_send():
    data = request.get_json()
    text = data.get("text", "")
    key = data.get("key", "")

    if not text or not key:
        return jsonify({"error": "Metin ve anahtar boş olamaz"}), 400

    try:
        encrypted = vigenere_encrypt(text, key)
        decrypted = vigenere_decrypt(encrypted, key)
    except Exception as e:
        return jsonify({"error": f"Şifreleme hatası: {str(e)}"}), 400

    return jsonify({"encrypted": encrypted, "decrypted": decrypted})

