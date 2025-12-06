# 2 Round'luk Des Algoritması

IP = [58,50,42,34,26,18,10,2,
      60,52,44,36,28,20,12,4,
      62,54,46,38,30,22,14,6,
      64,56,48,40,32,24,16,8,
      57,49,41,33,25,17,9,1,
      59,51,43,35,27,19,11,3,
      61,53,45,37,29,21,13,5,
      63,55,47,39,31,23,15,7]

IP_INV = [40,8,48,16,56,24,64,32,
          39,7,47,15,55,23,63,31,
          38,6,46,14,54,22,62,30,
          37,5,45,13,53,21,61,29,
          36,4,44,12,52,20,60,28,
          35,3,43,11,51,19,59,27,
          34,2,42,10,50,18,58,26,
          33,1,41,9,49,17,57,25]

E = [32,1,2,3,4,5,
     4,5,6,7,8,9,
     8,9,10,11,12,13,
     12,13,14,15,16,17,
     16,17,18,19,20,21,
     20,21,22,23,24,25,
     24,25,26,27,28,29,
     28,29,30,31,32,1]

P = [16,7,20,21,29,12,28,17,
     1,15,23,26,5,18,31,10,
     2,8,24,14,32,27,3,9,
     19,13,30,6,22,11,4,25]


SBOX = [
[[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
 [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
 [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
 [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
[[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
 [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
 [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
 [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]]
]

def _str_to_bits(s):

    bits = []
    for c in s:
        byte = ord(c) & 0xFF
        b = bin(byte)[2:].rjust(8, "0")
        bits.extend(int(x) for x in b)
    return bits

def _bits_to_bytes(bits):
    out = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        out.append(int("".join(str(x) for x in byte), 2))
    return out

def _bytes_to_bits(bytes_list):
    bits = []
    for b in bytes_list:
        bits.extend(int(x) for x in bin(b)[2:].rjust(8, "0"))
    return bits

def _bits_to_hexstr(bits):
    b = _bits_to_bytes(bits)
    return "".join("{:02x}".format(x) for x in b)

def _hexstr_to_bits(hexstr):
    if len(hexstr) % 2 != 0:
        raise ValueError("Hex string uzunluğu çift olmalı")
    bytes_list = []
    for i in range(0, len(hexstr), 2):
        bytes_list.append(int(hexstr[i:i+2], 16))
    return _bytes_to_bits(bytes_list)

def permute(block, table):
    return [block[i-1] for i in table]

def xor(a,b):
    return [i^j for i,j in zip(a,b)]

def f(right, subkey):

    right_exp = permute(right, E)  
    temp = xor(right_exp, subkey)  
    output = []

    for i in range(0, len(temp), 6):
        block = temp[i:i+6]
        row = block[0]*2 + block[5]
        col = block[1]*8 + block[2]*4 + block[3]*2 + block[4]*1
        sbox = SBOX[(i//6) % len(SBOX)] 
        s = sbox[row][col]
        bin_s = bin(s)[2:].rjust(4, "0")
        output.extend(int(x) for x in bin_s)
    output = permute(output, P)
    return output

def des_block_bits(block_bits, key_bits, encrypt=True):

    block = permute(block_bits, IP)
    L, R = block[:32], block[32:]
    subkeys = [key_bits[:48], key_bits[8:56]]
    if not encrypt:
        subkeys = subkeys[::-1]
    for subkey in subkeys:
        temp = R
        R = xor(L, f(R, subkey))
        L = temp
    combined = R + L
    return permute(combined, IP_INV)

def des_encrypt(plaintext, key):

    if len(plaintext) != 8 or len(key) != 7:
        raise ValueError("Plaintext 8 karakter ve key 7 karakter olmalı")
    block_bits = _str_to_bits(plaintext)
    key_bits = _str_to_bits(key)  # 7 byte -> 56 bit
    out_bits = des_block_bits(block_bits, key_bits, encrypt=True)
    return _bits_to_hexstr(out_bits)

def des_decrypt(cipher_hex, key):

    if len(key) != 7:
        raise ValueError("Key 7 karakter olmalı")
    block_bits = _hexstr_to_bits(cipher_hex)
    key_bits = _str_to_bits(key)
    out_bits = des_block_bits(block_bits, key_bits, encrypt=False)
    out_bytes = _bits_to_bytes(out_bits)
    return "".join(chr(b) for b in out_bytes)
