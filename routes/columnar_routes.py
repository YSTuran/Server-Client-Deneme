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
    text = data.get("text", "").strip()
    key = data.get("key", "").strip()

    if not text or not key:
        return jsonify({"error": "Metin ve anahtar boş olamaz"}), 400

    try:
        encrypted = columnar_encrypt(text, key)
        decrypted = columnar_decrypt(encrypted, key)

    except Exception as e:
        return jsonify({"error": f"Şifreleme hatası: {str(e)}"}), 400

    return jsonify({
        "encrypted": encrypted,
        "decrypted": decrypted
    })
