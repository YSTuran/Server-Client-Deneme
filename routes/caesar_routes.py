from flask import Blueprint, render_template, request, jsonify
from cipher.caesar import caesar_encrypt, caesar_decrypt

caesar_bp = Blueprint("caesar_bp", __name__)
SERVER_XOR_KEY = 123

def xor_text(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)


@caesar_bp.route("/caesar", methods=["GET"])
def page():
    return render_template("caesar.html")


@caesar_bp.route("/caesar/send", methods=["POST"])
def caesar_send():
    data = request.get_json()
    client_xor_text = data.get("text", "")
    shift = int(data.get("shift", 0))

    original_text = xor_text(client_xor_text, SERVER_XOR_KEY)
    encrypted = caesar_encrypt(original_text, shift)
    decrypted = caesar_decrypt(encrypted, shift)
    decrypted_client_safe = xor_text(decrypted, SERVER_XOR_KEY)

    return jsonify({
        "encrypted": encrypted,
        "decrypted": decrypted_client_safe
    })
