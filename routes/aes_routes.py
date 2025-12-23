from flask import Blueprint, render_template, request, jsonify
from cipher.aes import aes_encrypt, aes_decrypt
from cipher.rsa import rsa_encrypt, generate_keys
from cipher.ecc import ecc_encrypt, ecc_decrypt, generate_ecc_keys
import base64

aes_bp = Blueprint("aes_bp", __name__, url_prefix="/aes")

RSA_PUBLIC_KEY, RSA_PRIVATE_KEY = generate_keys()
ECC_PUBLIC_KEY, ECC_PRIVATE_KEY = generate_ecc_keys()


@aes_bp.route("/", methods=["GET"])
def page():
    return render_template("aes.html")

SERVER_XOR_KEY = 123

def xor_text(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)


@aes_bp.route("/send", methods=["POST"])
def send():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body yok"}), 400

    encoded_xor_text = data.get("text", "") # İstemciden gelen Base64+XOR'lu metin
    key = data.get("key", "")
    transport = data.get("transport", "none")

    try:
        raw_xor_bytes = base64.b64decode(encoded_xor_text)
        raw_xor_text = raw_xor_bytes.decode('utf-8')
        original_text = xor_text(raw_xor_text, SERVER_XOR_KEY)

        if len(original_text) != 16 or len(key) != 16:
            return jsonify({"error": f"Metin ve anahtar 16 karakter olmalı! (Gelen: {len(original_text)})"}), 400

        encrypted = aes_encrypt(original_text, key)
        decrypted = aes_decrypt(encrypted, key)

        response = {
            "encrypted": encrypted,
            "decrypted": decrypted,
            "transport": transport
        }

        if transport == "rsa":
            response["transported"] = rsa_encrypt(encrypted, RSA_PUBLIC_KEY)
        elif transport == "ecc":
            ecc_payload = ecc_encrypt(encrypted.encode("utf-8"), ECC_PUBLIC_KEY)
            ecc_plain = ecc_decrypt(ecc_payload, ECC_PRIVATE_KEY)
            response["transported"] = ecc_payload
            response["ecc_decrypted"] = ecc_plain.decode("utf-8")

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"İşlem hatası: {str(e)}"}), 500
