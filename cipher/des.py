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

PC1 = [
    57,49,41,33,25,17,9,
    1,58,50,42,34,26,18,
    10,2,59,51,43,35,27,
    19,11,3,60,52,44,36,
    63,55,47,39,31,23,15,
    7,62,54,46,38,30,22,
    14,6,61,53,45,37,29,
    21,13,5,28,20,12,4
]

PC2 = [
    14,17,11,24,1,5,
    3,28,15,6,21,10,
    23,19,12,4,26,8,
    16,7,27,20,13,2,
    41,52,31,37,47,55,
    30,40,51,45,33,48,
    44,49,39,56,34,53,
    46,42,50,36,29,32
]

SHIFT_SCHEDULE = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

SBOX = [
    [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
     [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
     [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
     [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
    [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
     [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
     [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
     [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
    [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
     [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
     [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
     [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
    [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
     [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
     [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
     [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
    [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
     [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
     [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
     [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
    [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
     [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
     [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
     [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
    [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
     [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
     [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
     [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
    [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
     [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
     [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
     [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
]

def _bytes_to_bits(byte_seq):
    bits = []
    for b in byte_seq:
        for i in range(8):
            bits.append((b >> (7 - i)) & 1)
    return bits

def _bits_to_bytes(bits):
    if len(bits) % 8 != 0:
        raise ValueError("bits length must be multiple of 8")
    out = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | (bits[i + j] & 1)
        out.append(byte)
    return bytes(out)

def _permute(bits, table):
    return [bits[i - 1] for i in table]

def _xor(a, b):
    return [x ^ y for x, y in zip(a, b)]

def _left_rotate(bits, n):
    return bits[n:] + bits[:n]

def _set_odd_parity_byte(b):
    top7 = b & 0xFE 
    ones = bin(top7).count("1")
    parity = 1 if ones % 2 == 0 else 0
    return top7 | parity

def _ensure_key_parity(byte_list):
    if len(byte_list) != 8:
        raise ValueError("Key must be 8 bytes for parity enforcement")
    return [_set_odd_parity_byte(b & 0xFF) for b in byte_list]

def _normalize_key(key):
    if isinstance(key, str):
        kb = [ord(c) & 0xFF for c in key]
    else:
        kb = list(key)

    if len(kb) == 7:
        xor_val = 0
        for b in kb:
            xor_val ^= (b & 0xFE)
        eighth_top7 = xor_val & 0xFE
        kb.append(eighth_top7)
    elif len(kb) == 8:
        pass
    else:
        raise ValueError("Key must be 7 or 8 bytes/chars")

    return _ensure_key_parity(kb)

def _generate_subkeys(key_bytes):
    key_bits = _bytes_to_bits(key_bytes)
    key56 = _permute(key_bits, PC1) 
    C = key56[:28]
    D = key56[28:]
    subkeys = []
    for shift in SHIFT_SCHEDULE:
        C = _left_rotate(C, shift)
        D = _left_rotate(D, shift)
        CD = C + D
        subkeys.append(_permute(CD, PC2))
    return subkeys

def _f_func(R, K):
    expanded = _permute(R, E)
    x = _xor(expanded, K)
    out = []
    for i in range(8):
        block6 = x[i*6:(i+1)*6]
        row = (block6[0] << 1) | block6[5]
        col = (block6[1] << 3) | (block6[2] << 2) | (block6[3] << 1) | block6[4]
        val = SBOX[i][row][col] 

        for j in range(4):
            out.append((val >> (3 - j)) & 1)
    return _permute(out, P)

def _des_block_process(block_bits, subkeys, encrypt=True):
    bits = _permute(block_bits, IP)
    L = bits[:32]
    R = bits[32:]
    keys = subkeys if encrypt else list(reversed(subkeys))
    for k in keys:
        newL = R
        newR = _xor(L, _f_func(R, k))
        L, R = newL, newR
    preout = R + L
    return _permute(preout, IP_INV)

def des_encrypt(plaintext, key):

    if isinstance(plaintext, str):
        pt_bytes = plaintext.encode('latin-1')
    else:
        pt_bytes = bytes(plaintext)

    if len(pt_bytes) != 8:
        raise ValueError("Plaintext must be exactly 8 bytes/chars")

    key_bytes = _normalize_key(key)

    subkeys = _generate_subkeys(key_bytes)

    block_bits = _bytes_to_bits(pt_bytes)
    out_bits = _des_block_process(block_bits, subkeys, encrypt=True)
    out_bytes = _bits_to_bytes(out_bits)
    return out_bytes.hex()

def des_decrypt(cipher_hex, key):
    if not isinstance(cipher_hex, str) or len(cipher_hex) != 16:
        raise ValueError("cipher_hex must be 16 hex characters (8 bytes)")

    try:
        cipher_bytes = bytes.fromhex(cipher_hex)
    except Exception as e:
        raise ValueError("cipher_hex is not valid hex") from e

    if len(cipher_bytes) != 8:
        raise ValueError("cipher_hex must represent exactly 8 bytes")

    key_bytes = _normalize_key(key)
    subkeys = _generate_subkeys(key_bytes)
    block_bits = _bytes_to_bits(cipher_bytes)
    out_bits = _des_block_process(block_bits, subkeys, encrypt=False)
    out_bytes = _bits_to_bytes(out_bits)
    return out_bytes.decode('latin-1')


