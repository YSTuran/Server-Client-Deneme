from flask import Blueprint, render_template, request, jsonify
from cipher.caesar import caesar_encrypt, caesar_decrypt

caesar_bp = Blueprint("caesar_bp", __name__)

@caesar_bp.route("/caesar", methods=["GET"])
def page():
    return render_template("caesar.html")

@caesar_bp.route("/caesar/send", methods=["POST"])
def caesar_send():
    data = request.get_json()
    text = data.get("text", "")
    try:
        shift = int(data.get("shift", 0))
    except:
        shift = 0

    encrypted = caesar_encrypt(text, shift)
    decrypted = caesar_decrypt(encrypted, shift)

    return jsonify({"encrypted": encrypted, "decrypted": decrypted})
