import base64
from flask import Blueprint, render_template, request, jsonify
from cipher.vigenere import vigenere_encrypt, vigenere_decrypt

vigenere_bp = Blueprint("vigenere_bp", __name__)
SERVER_XOR_KEY = 123

def xor_text(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)

@vigenere_bp.route("/vigenere", methods=["GET"])
def page():
    return render_template("vigenere.html")

@vigenere_bp.route("/vigenere/send", methods=["POST"])
def vigenere_send():
    data = request.get_json()
    encoded_xor_text = data.get("text", "")
    key = data.get("key", "")

    if not encoded_xor_text or not key:
        return jsonify({"error": "Metin ve anahtar boş olamaz"}), 400

    try:
        xor_text_bytes = base64.b64decode(encoded_xor_text)
        xor_text_from_client = xor_text_bytes.decode('utf-8')
        original_text = xor_text(xor_text_from_client, SERVER_XOR_KEY)

        encrypted = vigenere_encrypt(original_text, key)
        decrypted_plain = vigenere_decrypt(encrypted, key) 

        decrypted_xor = xor_text(decrypted_plain, SERVER_XOR_KEY)
        decrypted_safe_packet = base64.b64encode(decrypted_xor.encode()).decode()

        from app import socketio
        socketio.emit("display_on_server", {
            "method": "Vigenere Cipher",
            "text": encoded_xor_text,
            "encrypted": encrypted
        })

        return jsonify({
            "encrypted": encrypted,
            "decrypted": decrypted_safe_packet
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500