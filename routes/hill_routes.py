from flask import Blueprint, render_template, request, jsonify
from cipher.hill import hill_encrypt, hill_decrypt

hill_bp = Blueprint("hill_bp", __name__)

@hill_bp.route("/hill")
def page():
    return render_template("hill.html")

@hill_bp.route("/hill/send", methods=["POST"])
def send():
    data = request.json
    text = data.get("text")
    key = data.get("key")
    mode = data.get("mode")

    if mode == "encrypt":
        result = hill_encrypt(text, key)
    else:
        result = hill_decrypt(text, key)

    return jsonify({"result": result})
