import base64
from flask import Blueprint, render_template, request, jsonify
from cipher.des import des_encrypt, des_decrypt
from cipher.rsa import rsa_encrypt, rsa_decrypt, generate_keys
from cipher.ecc import ecc_encrypt, ecc_decrypt, generate_ecc_keys

des_bp = Blueprint("des_bp", __name__, url_prefix="/des")

RSA_PUBLIC_KEY, RSA_PRIVATE_KEY = generate_keys()
ECC_PUBLIC_KEY, ECC_PRIVATE_KEY = generate_ecc_keys()
SERVER_XOR_KEY = 123

def xor_text(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)

@des_bp.route("/", methods=["GET"])
def page():
    return render_template("des.html")

@des_bp.route("/send", methods=["POST"])
def send():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body yok"}), 400

    encoded_xor_text = data.get("text", "")
    key = data.get("key", "")
    transport = data.get("transport", "none")

    try:
        raw_xor_bytes = base64.b64decode(encoded_xor_text)
        raw_xor_text = raw_xor_bytes.decode('utf-8')
        original_text = xor_text(raw_xor_text, SERVER_XOR_KEY)

        if len(original_text) != 8 or len(key) != 7:
            return jsonify({"error": "Metin 8, anahtar 7 karakter olmalı"}), 400

        encrypted = des_encrypt(original_text, key)
        decrypted = des_decrypt(encrypted, key)

        response = {
            "encrypted": encrypted,
            "decrypted": decrypted,
            "transport": transport
        }

        if transport == "rsa":
            rsa_cipher = rsa_encrypt(encrypted, RSA_PUBLIC_KEY)
            rsa_plain = rsa_decrypt(rsa_cipher, RSA_PRIVATE_KEY)
            response["transported"] = rsa_cipher
            response["transport_decrypted"] = rsa_plain
        elif transport == "ecc":
            ecc_payload = ecc_encrypt(encrypted.encode(), ECC_PUBLIC_KEY)
            ecc_plain = ecc_decrypt(ecc_payload, ECC_PRIVATE_KEY)
            response["transported"] = ecc_payload
            response["transport_decrypted"] = ecc_plain.decode()
        else:
            response["transported"] = "-"

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500