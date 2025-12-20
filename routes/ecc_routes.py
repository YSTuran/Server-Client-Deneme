from flask import Blueprint, render_template, request, jsonify
from cipher.ecc import ecc_encrypt, ecc_decrypt

ecc_bp = Blueprint("ecc_bp", __name__)

@ecc_bp.route("/ecc", methods=["GET"])
def page():
    return render_template("ecc.html")


@ecc_bp.route("/ecc/send", methods=["POST"])
def ecc_send():
    data = request.get_json()

    try:
        xor_text = data["xor_text"].encode("latin1")

        encrypted = ecc_encrypt(xor_text)

        decrypted = ecc_decrypt(
            encrypted["ciphertext"],
            encrypted["iv"],
            encrypted["ephemeral_pub"]
        )

        return jsonify({
            "encrypted": encrypted["ciphertext"],
            "decrypted": decrypted
        })

    except Exception as e:
        return jsonify({"error": f"ECC hatası: {str(e)}"}), 400
