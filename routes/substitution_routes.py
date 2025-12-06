from flask import Blueprint, render_template, request, jsonify
from cipher.substitution import substitution_encrypt, substitution_decrypt

substitution_bp = Blueprint("substitution_bp", __name__)

@substitution_bp.route("/substitution")
def page():
    return render_template("substitution.html")

@substitution_bp.route("/substitution/send", methods=["POST"])
def send():
    data = request.json
    text = data.get("text")
    key = data.get("key")
    mode = data.get("mode")

    if mode == "encrypt":
        result = substitution_encrypt(text, key)
    else:
        result = substitution_decrypt(text, key)

    return jsonify({"result": result})
