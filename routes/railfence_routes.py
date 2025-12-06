from flask import Blueprint, render_template, request, jsonify
from cipher.railfence import railfence_encrypt, railfence_decrypt

railfence_bp = Blueprint("railfence_bp", __name__)

@railfence_bp.route("/railfence", methods=["GET"])
def page():
    return render_template("railfence.html")

@railfence_bp.route("/railfence/send", methods=["POST"])
def railfence_send():
    data = request.get_json()
    text = data.get("text", "")
    key = data.get("key", 2)

    if not text:
        return jsonify({"error": "Metin boş olamaz"}), 400

    try:
        rails = int(key)
    except:
        rails = 2

    try:
        encrypted = railfence_encrypt(text, rails)
        decrypted = railfence_decrypt(encrypted, rails)
    except Exception as e:
        return jsonify({"error": f"Şifreleme hatası: {str(e)}"}), 400

    return jsonify({"encrypted": encrypted, "decrypted": decrypted})

