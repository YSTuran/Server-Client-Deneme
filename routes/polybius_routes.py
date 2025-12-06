from flask import Blueprint, render_template, request, jsonify
from cipher.polybius import polybius_encrypt, polybius_decrypt

polybius_bp = Blueprint("polybius_bp", __name__)

@polybius_bp.route("/polybius", methods=["GET"])
def page():
    return render_template("polybius.html")

@polybius_bp.route("/polybius/send", methods=["POST"])
def polybius_send():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Metin boş olamaz"}), 400

    try:
        encrypted = polybius_encrypt(text)
        decrypted = polybius_decrypt(encrypted)
    except Exception as e:
        return jsonify({"error": f"Şifreleme hatası: {str(e)}"}), 400

    return jsonify({"encrypted": encrypted, "decrypted": decrypted})
