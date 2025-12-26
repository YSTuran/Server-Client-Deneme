import base64
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
    encoded_xor_text = data.get("text", "").strip()
    key = data.get("key", "").strip()

    if not encoded_xor_text or not key:
        return jsonify({"error": "Metin ve anahtar boş olamaz"}), 400

    try:
        xor_text_bytes = base64.b64decode(encoded_xor_text)
        xor_text_from_client = xor_text_bytes.decode('utf-8')
        original_text = xor_text(xor_text_from_client, SERVER_XOR_KEY)

        encrypted = columnar_encrypt(original_text, key)
        decrypted_plain = columnar_decrypt(encrypted, key)

        decrypted_xor = xor_text(decrypted_plain, SERVER_XOR_KEY)
        decrypted_safe_packet = base64.b64encode(decrypted_xor.encode()).decode()

        from app import socketio
        socketio.emit("display_on_server", {
            "method": "Columnar Transposition",
            "text": encoded_xor_text,
            "encrypted": encrypted
        })

        return jsonify({
            "encrypted": encrypted,
            "decrypted": decrypted_safe_packet
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500