from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os, base64


def generate_ecc_keys():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    return public_key, private_key


def ecc_encrypt(data: bytes, receiver_public_key):
    ephemeral_private = ec.generate_private_key(ec.SECP256R1())
    shared_key = ephemeral_private.exchange(ec.ECDH(), receiver_public_key)

    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"ecc-transport"
    ).derive(shared_key)

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    pad_len = 16 - (len(data) % 16)
    padded = data + bytes([pad_len]) * pad_len

    ciphertext = encryptor.update(padded) + encryptor.finalize()

    ephemeral_pub_bytes = ephemeral_private.public_key().public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "iv": base64.b64encode(iv).decode(),
        "ephemeral_pub": base64.b64encode(ephemeral_pub_bytes).decode()
    }


def ecc_decrypt(payload: dict, receiver_private_key):
    ephemeral_pub = serialization.load_der_public_key(
        base64.b64decode(payload["ephemeral_pub"])
    )

    shared_key = receiver_private_key.exchange(ec.ECDH(), ephemeral_pub)

    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"ecc-transport"
    ).derive(shared_key)

    iv = base64.b64decode(payload["iv"])
    ciphertext = base64.b64decode(payload["ciphertext"])

    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded = decryptor.update(ciphertext) + decryptor.finalize()
    pad_len = padded[-1]

    return padded[:-pad_len]
