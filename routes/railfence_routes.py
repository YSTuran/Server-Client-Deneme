from flask import Blueprint, render_template, request, jsonify
from cipher.railfence import rail_encrypt, rail_decrypt

railfence_bp = Blueprint("railfence_bp", __name__)

@railfence_bp.route("/railfence")
def page():
    return render_template("railfence.html")

@railfence_bp.route("/railfence/send", methods=["POST"])
def send():
    data = request.json
    text = data.get("text")
    rails = int(data.get("rails"))
    mode = data.get("mode")

    if mode == "encrypt":
        result = rail_encrypt(text)
    else:
        result = rail_decrypt(text)

    return jsonify({"result": result})
