from flask import Blueprint, render_template, request, jsonify
from cipher.hill import hill_encrypt, hill_decrypt

hill_bp = Blueprint("hill_bp", __name__)

@hill_bp.route("/hill", methods=["GET"])
def page():
    return render_template("hill.html")

@hill_bp.route("/hill/send", methods=["POST"])
def hill_send():
    data = request.get_json()
    text = data.get("text", "").strip()
    matrix_str = data.get("matrix", "").strip()

    if not text or not matrix_str:
        return jsonify({"error": "Metin ve matriks boş olamaz"}), 400

    try:
        matrix_values = [int(x) for x in matrix_str.split(",")]
        encrypted = hill_encrypt(text, matrix_values)
        decrypted = hill_decrypt(encrypted, matrix_values)
    except Exception as e:
        return jsonify({"error": f"Matriste hata: {str(e)}"}), 400

    return jsonify({"encrypted": encrypted, "decrypted": decrypted})
