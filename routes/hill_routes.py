from flask import Blueprint, render_template, request, jsonify
from cipher.hill import hill_encrypt, hill_decrypt
import base64

hill_bp = Blueprint("hill_bp", __name__)

# 🔒 Sunucuya özel gizli XOR anahtarı
SERVER_XOR_KEY = 123


# =====================
# XOR + Base64 KATMANI
# =====================

def xor_encrypt(text: str) -> str:
    raw = text.encode("utf-8")
    xored = bytes(b ^ SERVER_XOR_KEY for b in raw)
    return base64.b64encode(xored).decode("utf-8")


def xor_decrypt(text: str) -> str:
    raw = base64.b64decode(text)
    original = bytes(b ^ SERVER_XOR_KEY for b in raw)
    return original.decode("utf-8")

@hill_bp.route("/hill", methods=["GET"])
def page():
    return render_template("hill.html")

@hill_bp.route("/hill/send", methods=["POST"])
def hill_send():
    data = request.get_json() or {}

    plain_text = data.get("text", "").strip()
    matrix_str = data.get("matrix", "").strip()

    if not plain_text or not matrix_str:
        return jsonify({"error": "Metin ve matris boş olamaz"}), 400

    try:
        plain_text = plain_text.upper().replace(" ", "")

        key = [int(x) for x in matrix_str.split(",")]

        hill_encrypted = hill_encrypt(plain_text, key)

        encrypted_out = xor_encrypt(hill_encrypted)

        hill_cipher = xor_decrypt(encrypted_out)
        decrypted_out = hill_decrypt(hill_cipher, key)

    except Exception as e:
        return jsonify({"error": f"Hill hatası: {str(e)}"}), 400

    return jsonify({
        "encrypted": encrypted_out,
        "decrypted": decrypted_out
    })
