import base64
from flask import Blueprint, render_template, request, jsonify
from cipher.substitution import substitution_encrypt, substitution_decrypt

substitution_bp = Blueprint("substitution_bp", __name__)
SERVER_XOR_KEY = 123

def xor_text(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)

@substitution_bp.route("/substitution", methods=["GET"])
def page():
    return render_template("substitution.html")

@substitution_bp.route("/substitution/send", methods=["POST"])
def substitution_send():
    data = request.get_json()
    encoded_xor_text = data.get("text", "").strip()
    key = data.get("key", "").strip()

    if not encoded_xor_text or len(key) != 26:
        return jsonify({"error": "Metin boş olamaz ve anahtar 26 karakter olmalı"}), 400

    try:
        xor_text_bytes = base64.b64decode(encoded_xor_text)
        xor_text_from_client = xor_text_bytes.decode('utf-8')
        original_text = xor_text(xor_text_from_client, SERVER_XOR_KEY)

        encrypted = substitution_encrypt(original_text, key)
        decrypted_plain = substitution_decrypt(encrypted, key)

        decrypted_xor = xor_text(decrypted_plain, SERVER_XOR_KEY)
        decrypted_safe_packet = base64.b64encode(decrypted_xor.encode()).decode()

        from app import socketio
        socketio.emit("display_on_server", {
            "method": "Substitution",
            "text": encoded_xor_text,
            "encrypted": encrypted
        })

        return jsonify({
            "encrypted": encrypted,
            "decrypted": decrypted_safe_packet
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500