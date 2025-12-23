import base64
from flask import Blueprint, render_template, request, jsonify
from cipher.caesar import caesar_encrypt, caesar_decrypt

caesar_bp = Blueprint("caesar_bp", __name__)
SERVER_XOR_KEY = 123


def xor_text(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)


@caesar_bp.route("/caesar")
def page():
    return render_template("caesar.html")


@caesar_bp.route("/caesar/send", methods=["POST"])
def caesar_send():
    data = request.get_json()
    encoded = data.get("text")
    shift = int(data.get("shift"))

    raw_xor = base64.b64decode(encoded).decode()
    original = xor_text(raw_xor, SERVER_XOR_KEY)

    encrypted = caesar_encrypt(original, shift)
    decrypted = caesar_decrypt(encrypted, shift)

    return jsonify({
        "encrypted": encrypted,
        "decrypted": decrypted
    })
