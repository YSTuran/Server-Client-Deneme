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

        key = [int(x) for x in matrix_str.split(",")]

        encrypted_final = hill_encrypt(original_text, key)
        decrypted_plain = hill_decrypt(encrypted_final, key)

        decrypted_xor = xor_text(decrypted_plain, SERVER_XOR_KEY)
        decrypted_safe_packet = base64.b64encode(decrypted_xor.encode()).decode()

        from app import socketio
        socketio.emit("display_on_server", {
            "method": "Hill",
            "text": encoded_xor_text,
            "encrypted": encrypted_final
        })

        return jsonify({
            "encrypted": encrypted_final,
            "decrypted": decrypted_safe_packet
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400