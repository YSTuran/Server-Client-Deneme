import base64
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
    encoded_xor_text = data.get("text", "").strip()
    key_val = data.get("key", 2)

    if not encoded_xor_text:
        return jsonify({"error": "Metin boş olamaz"}), 400

    try:
        rails = int(key_val)
        if rails < 2: rails = 2
    except:
        rails = 2

    try:
        xor_text_bytes = base64.b64decode(encoded_xor_text)
        xor_text_from_client = xor_text_bytes.decode('utf-8')
        original_text = xor_text(xor_text_from_client, SERVER_XOR_KEY)

        encrypted = railfence_encrypt(original_text, rails)
        decrypted_plain = railfence_decrypt(encrypted, rails)

        decrypted_xor = xor_text(decrypted_plain, SERVER_XOR_KEY)
        decrypted_safe_packet = base64.b64encode(decrypted_xor.encode()).decode()

        from app import socketio
        socketio.emit("display_on_server", {
            "method": "Rail Fence",
            "text": encoded_xor_text,
            "encrypted": encrypted
        })

        return jsonify({
            "encrypted": encrypted,
            "decrypted": decrypted_safe_packet
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500