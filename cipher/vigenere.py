def extend_key(text, key):
    new_key = ""
    key_index = 0

    for c in text:
        if c == " ":
            new_key += "*"
        else:
            new_key += key[key_index % len(key)]
            key_index += 1

    return new_key


def char_shift(c, k, mode):
    if c == "*":
        return "*"

    base = ord('A')
    t = ord(c.upper()) - base
    k = ord(k.upper()) - base

    if mode == "encrypt":
        return chr((t + k) % 26 + base)
    else:
        return chr((t - k) % 26 + base)


def vigenere_encrypt(text, key):
    text = text.replace(" ", "*")
    ek = extend_key(text, key)

    return "".join(char_shift(text[i], ek[i], "encrypt") for i in range(len(text)))


def vigenere_decrypt(text, key):
    ek = extend_key(text, key)

    decrypted = "".join(char_shift(text[i], ek[i], "decrypt") for i in range(len(text)))
    return decrypted.replace("*", " ")
