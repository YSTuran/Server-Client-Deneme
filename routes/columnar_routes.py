from flask import Blueprint, render_template, request, jsonify
from cipher.columnar import columnar_encrypt, columnar_decrypt

columnar_bp = Blueprint("columnar_bp", __name__)

SERVER_XOR_KEY = 123

def xor_text(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)


@columnar_bp.route("/columnar", methods=["GET"])
def page():
    return render_template("columnar.html")

@columnar_bp.route("/columnar/send", methods=["POST"])
def columnar_send():
    data = request.get_json()
    xor_text_from_client = data.get("text", "").strip()
    key = data.get("key", "").strip()

    if not xor_text_from_client or not key:
        return jsonify({"error": "Metin ve anahtar boş olamaz"}), 400

    try:
        original_text = xor_text(xor_text_from_client, SERVER_XOR_KEY)

        encrypted = columnar_encrypt(original_text, key)
        decrypted = columnar_decrypt(encrypted, key)
        decrypted_xor = xor_text(decrypted, SERVER_XOR_KEY)

    except Exception as e:
        return jsonify({"error": f"Şifreleme hatası: {str(e)}"}), 400

    return jsonify({
        "encrypted": encrypted,
        "decrypted": decrypted_xor
    })
