from flask import Blueprint, render_template, request, jsonify
from cipher.polybius import polybius_encrypt, polybius_decrypt

polybius_bp = Blueprint("polybius_bp", __name__)

@polybius_bp.route("/polybius")
def page():
    return render_template("polybius.html")

@polybius_bp.route("/polybius/send", methods=["POST"])
def send():
    data = request.json
    text = data.get("text")
    mode = data.get("mode")

    if mode == "encrypt":
        result = polybius_encrypt(text)
    else:
        result = polybius_decrypt(text)

    return jsonify({"result": result})
