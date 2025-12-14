from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key().decode()
    public_key = key.publickey().export_key().decode()
    return public_key, private_key


def rsa_encrypt(text, public_key_str):
    public_key = RSA.import_key(public_key_str)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_bytes = cipher.encrypt(text.encode("utf-8"))
    return base64.b64encode(encrypted_bytes).decode()


def rsa_decrypt(cipher_text, private_key_str):
    private_key = RSA.import_key(private_key_str)
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_bytes = cipher.decrypt(base64.b64decode(cipher_text))
    return decrypted_bytes.decode("utf-8")
