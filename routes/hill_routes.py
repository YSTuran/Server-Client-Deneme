import base64
from flask import Blueprint, render_template, request, jsonify
from cipher.hill import hill_encrypt, hill_decrypt

hill_bp = Blueprint("hill_bp", __name__)
SERVER_XOR_KEY = 123

def xor_text(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)

@hill_bp.route("/hill", methods=["GET"])
def page():
    return render_template("hill.html")

@hill_bp.route("/hill/send", methods=["POST"])
def hill_send():
    data = request.get_json()
    encoded_xor_text = data.get("text", "").strip()
    matrix_str = data.get("matrix", "").strip()

    try:
        raw_xor_bytes = base64.b64decode(encoded_xor_text)
        raw_xor_text = raw_xor_bytes.decode('utf-8')
        original_text = xor_text(raw_xor_text, SERVER_XOR_KEY)
        
        original_text = original_text.upper().replace(" ", "")
        key = [int(x) for x in matrix_str.split(",")]

        encrypted = hill_encrypt(original_text, key)
        decrypted = hill_decrypt(encrypted, key)

        return jsonify({
            "encrypted": encrypted,
            "decrypted": decrypted
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400