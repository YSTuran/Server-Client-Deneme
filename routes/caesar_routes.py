from flask import Blueprint, render_template, request, jsonify
from cipher.caesar import caesar_encrypt, caesar_decrypt

caesar_bp = Blueprint("caesar_bp", __name__)

@caesar_bp.route("/caesar")
def page():
    return render_template("caesar.html")

@caesar_bp.route("/caesar/send", methods=["POST"])
def send():
    data = request.json
    text = data.get("text")
    shift = data.get("shift", 3)
    mode = data.get("mode", "encrypt")

    if mode == "encrypt":
        result = caesar_encrypt(text, shift)
    else:
        result = caesar_decrypt(text, shift)

    return jsonify({"result": result})
