import base64
from flask import Blueprint, render_template, request, jsonify
from cipher.polybius import polybius_encrypt, polybius_decrypt

polybius_bp = Blueprint("polybius_bp", __name__)
SERVER_XOR_KEY = 123

def xor_text(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)

@polybius_bp.route("/polybius", methods=["GET"])
def page():
    return render_template("polybius.html")

@polybius_bp.route("/polybius/send", methods=["POST"])
def polybius_send():
    data = request.get_json()
    encoded_xor_text = data.get("text", "").strip()

    if not encoded_xor_text:
        return jsonify({"error": "Metin boş olamaz"}), 400

    try:
        xor_text_bytes = base64.b64decode(encoded_xor_text)
        xor_text_from_client = xor_text_bytes.decode('utf-8')
        original_text = xor_text(xor_text_from_client, SERVER_XOR_KEY)

        encrypted = polybius_encrypt(original_text)
        decrypted = polybius_decrypt(encrypted)

        return jsonify({
            "encrypted": encrypted,
            "decrypted": decrypted
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500