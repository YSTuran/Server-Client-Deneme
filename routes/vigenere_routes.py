from flask import Blueprint, render_template, request, jsonify
from cipher.vigenere import vigenere_encrypt, vigenere_decrypt

vigenere_bp = Blueprint("vigenere_bp", __name__)

@vigenere_bp.route("/vigenere")
def page():
    return render_template("vigenere.html")

@vigenere_bp.route("/vigenere/send", methods=["POST"])
def send():
    data = request.json
    text = data.get("text")
    key = data.get("key")
    mode = data.get("mode")

    if mode == "encrypt":
        result = vigenere_encrypt(text, key)
    else:
        result = vigenere_decrypt(text, key)

    return jsonify({"result": result})
