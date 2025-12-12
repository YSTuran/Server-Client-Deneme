from flask import Blueprint, render_template, request, jsonify
from cipher.railfence import railfence_encrypt, railfence_decrypt

railfence_bp = Blueprint("railfence_bp", __name__)

SERVER_XOR_KEY = 123

def xor_text(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)

@railfence_bp.route("/railfence", methods=["GET"])
def page():
    return render_template("railfence.html")

@railfence_bp.route("/railfence/send", methods=["POST"])
def railfence_send():
    data = request.get_json()

    xor_text_from_client = data.get("text", "")
    key = data.get("key", 2)

    if not xor_text_from_client:
        return jsonify({"error": "Metin boş olamaz"}), 400

    try:
        rails = int(key)
    except:
        rails = 2

    try:
        original_text = xor_text(xor_text_from_client, SERVER_XOR_KEY)

        encrypted = railfence_encrypt(original_text, rails)
        decrypted = railfence_decrypt(encrypted, rails)

        decrypted_xor = xor_text(decrypted, SERVER_XOR_KEY)

    except Exception as e:
        return jsonify({"error": f"Şifreleme hatası: {str(e)}"}), 400

    return jsonify({
        "encrypted": encrypted,
        "decrypted": decrypted_xor
    })
