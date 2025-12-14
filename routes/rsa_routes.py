from flask import Blueprint, render_template, request, jsonify
from cipher.rsa import generate_keys, rsa_encrypt, rsa_decrypt

rsa_bp = Blueprint("rsa_bp", __name__)

PUBLIC_KEY, PRIVATE_KEY = generate_keys()

@rsa_bp.route("/rsa", methods=["GET"])
def page():
    return render_template("rsa.html")

@rsa_bp.route("/rsa/send", methods=["POST"])
def rsa_send():
    data = request.get_json()
    text = data.get("text", "")
    mode = data.get("mode", "encrypt")

    if not text:
        return jsonify({"error": "Metin boş olamaz"}), 400

    try:
        if mode == "decrypt":
            decrypted = rsa_decrypt(text, PRIVATE_KEY)
            return jsonify({"decrypted": decrypted})
        else:
            encrypted = rsa_encrypt(text, PUBLIC_KEY)
            return jsonify({"encrypted": encrypted})

    except Exception as e:
        return jsonify({"error": f"RSA hatası: {str(e)}"}), 400

@rsa_bp.route("/rsa/key", methods=["GET"])
def rsa_key():
    return jsonify({"public_key": PUBLIC_KEY})
