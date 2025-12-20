from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os, base64

SERVER_PRIVATE_KEY = ec.generate_private_key(ec.SECP256R1())
SERVER_PUBLIC_KEY = SERVER_PRIVATE_KEY.public_key()

XOR_KEY = 123

def xor_bytes(data: bytes) -> bytes:
    return bytes(b ^ XOR_KEY for b in data)


def ecc_encrypt(xor_plain_bytes: bytes):
    eph_private = ec.generate_private_key(ec.SECP256R1())
    shared = eph_private.exchange(ec.ECDH(), SERVER_PUBLIC_KEY)

    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"ecc-demo",
    ).derive(shared)

    iv = os.urandom(16)

    cipher = Cipher(
        algorithms.AES(derived_key),
        modes.CFB(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(xor_plain_bytes) + encryptor.finalize()

    eph_public_bytes = eph_private.public_key().public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    return {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "iv": base64.b64encode(iv).decode(),
        "ephemeral_pub": base64.b64encode(eph_public_bytes).decode()
    }


def ecc_decrypt(ciphertext_b64, iv_b64, eph_pub_b64):
    ciphertext = base64.b64decode(ciphertext_b64)
    iv = base64.b64decode(iv_b64)
    eph_pub_bytes = base64.b64decode(eph_pub_b64)

    eph_public = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256R1(),
        eph_pub_bytes
    )

    shared = SERVER_PRIVATE_KEY.exchange(ec.ECDH(), eph_public)

    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"ecc-demo",
    ).derive(shared)

    cipher = Cipher(
        algorithms.AES(derived_key),
        modes.CFB(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    xor_plain = decryptor.update(ciphertext) + decryptor.finalize()

    plain = xor_bytes(xor_plain)
    return plain.decode("utf-8")
