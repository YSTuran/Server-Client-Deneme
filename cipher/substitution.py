import string

alphabet = string.ascii_uppercase

def substitution_encrypt(text, key):
    table = {alphabet[i]: key[i].upper() for i in range(26)}

    result = ""
    for c in text:
        if c == " ":
            result += "*"
        elif c.isalpha():
            result += table[c.upper()]
        else:
            result += c
    return result


def substitution_decrypt(text, key):
    reverse_table = {key[i].upper(): alphabet[i] for i in range(26)}

    result = ""
    for c in text:
        if c == "*":
            result += " "
        elif c.isalpha():
            result += reverse_table[c.upper()]
        else:
            result += c
    return result
