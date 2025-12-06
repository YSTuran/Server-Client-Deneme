from flask import Blueprint, render_template, request, jsonify
from cipher.columnar import columnar_encrypt, columnar_decrypt

columnar_bp = Blueprint("columnar_bp", __name__)

@columnar_bp.route("/columnar")
def page():
    return render_template("columnar.html")

@columnar_bp.route("/columnar/send", methods=["POST"])
def send():
    data = request.json
    text = data.get("text")
    key = data.get("key")
    mode = data.get("mode")

    if mode == "encrypt":
        result = columnar_encrypt(text, key)
    else:
        result = columnar_decrypt(text, key)

    return jsonify({"result": result})
