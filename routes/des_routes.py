from flask import Blueprint, render_template, request, jsonify
from cipher.des import des_encrypt, des_decrypt

des_bp = Blueprint("des_bp", __name__)

@des_bp.route("/des", methods=["GET"])
def page():
    return render_template("des.html")

@des_bp.route("/des/send", methods=["POST"])
def des_send():
    data = request.get_json() or {}
    text = data.get("text", "")
    key = data.get("key", "")

    if len(text) != 8 or len(key) != 7:
        return jsonify({"error":"Metin 8 karakter ve anahtar 7 karakter olmalı"}), 400

    try:
        encrypted = des_encrypt(text, key) 
        decrypted = des_decrypt(encrypted, key)
    except Exception as e:
        return jsonify({"error": f"DES hatası: {str(e)}"}), 400

    return jsonify({"encrypted": encrypted, "decrypted": decrypted})