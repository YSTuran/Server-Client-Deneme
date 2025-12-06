SBOX = [
0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

INV_SBOX = [0]*256
for i,v in enumerate(SBOX):
    INV_SBOX[v] = i

RCON = [
0x00,
0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36
]

def _bytes_to_matrix(b: bytes):
    if len(b) != 16:
        raise ValueError("Block must be 16 bytes")
    return [[b[row + 4*col] for col in range(4)] for row in range(4)]

def _matrix_to_bytes(state):
    out = bytearray(16)
    for r in range(4):
        for c in range(4):
            out[r + 4*c] = state[r][c]
    return bytes(out)

def _xor_bytes(a,b):
    return bytes(x^y for x,y in zip(a,b))

def _xtime(a):
    return ((a << 1) & 0xFF) ^ (0x1B if (a & 0x80) else 0)

def _mul(a,b):
    res = 0
    for i in range(8):
        if b & 1:
            res ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return res

def _sub_bytes(state):
    for r in range(4):
        for c in range(4):
            state[r][c] = SBOX[state[r][c]]

def _inv_sub_bytes(state):
    for r in range(4):
        for c in range(4):
            state[r][c] = INV_SBOX[state[r][c]]

def _shift_rows(state):
    for r in range(1,4):
        state[r] = state[r][r:] + state[r][:r]

def _inv_shift_rows(state):
    for r in range(1,4):
        state[r] = state[r][-r:] + state[r][:-r]

def _mix_single_column(col):
    a0,a1,a2,a3 = col
    return [
        _mul(a0,2) ^ _mul(a1,3) ^ a2 ^ a3,
        a0 ^ _mul(a1,2) ^ _mul(a2,3) ^ a3,
        a0 ^ a1 ^ _mul(a2,2) ^ _mul(a3,3),
        _mul(a0,3) ^ a1 ^ a2 ^ _mul(a3,2)
    ]

def _mix_columns(state):
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        nc = _mix_single_column(col)
        for r in range(4):
            state[r][c] = nc[r]

def _inv_mix_single_column(col):
    a0,a1,a2,a3 = col
    return [
        _mul(a0,0x0e) ^ _mul(a1,0x0b) ^ _mul(a2,0x0d) ^ _mul(a3,0x09),
        _mul(a0,0x09) ^ _mul(a1,0x0e) ^ _mul(a2,0x0b) ^ _mul(a3,0x0d),
        _mul(a0,0x0d) ^ _mul(a1,0x09) ^ _mul(a2,0x0e) ^ _mul(a3,0x0b),
        _mul(a0,0x0b) ^ _mul(a1,0x0d) ^ _mul(a2,0x09) ^ _mul(a3,0x0e)
    ]

def _inv_mix_columns(state):
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        nc = _inv_mix_single_column(col)
        for r in range(4):
            state[r][c] = nc[r]

def _add_round_key(state, round_key):
    rk = _bytes_to_matrix(round_key)
    for r in range(4):
        for c in range(4):
            state[r][c] ^= rk[r][c]

def _rot_word(word4):
    return word4[1:] + word4[:1]

def _sub_word(word4):
    return [SBOX[b] for b in word4]

def _expand_key(key16):
    if len(key16) != 16:
        raise ValueError("Key must be 16 bytes for AES-128")
    key_words = [list(key16[i:i+4]) for i in range(0,16,4)]
    for i in range(4, 44):
        temp = key_words[i-1].copy()
        if i % 4 == 0:
            temp = _sub_word(_rot_word(temp))
            temp[0] ^= RCON[i//4]
        word = [ (key_words[i-4][j] ^ temp[j]) & 0xFF for j in range(4) ]
        key_words.append(word)
    round_keys = []
    for r in range(11):
        rk = []
        for w in key_words[4*r:4*r+4]:
            rk.extend(w)
        round_keys.append(bytes(rk))
    return round_keys

def encrypt_block(plaintext16, key16):
    if isinstance(plaintext16, str):
        pt = plaintext16.encode('latin-1')
    else:
        pt = bytes(plaintext16)
    if isinstance(key16, str):
        key = key16.encode('latin-1')
    else:
        key = bytes(key16)

    if len(pt) != 16 or len(key) != 16:
        raise ValueError("Plaintext and key must be 16 bytes/chars")

    round_keys = _expand_key(key)
    state = _bytes_to_matrix(pt)

    _add_round_key(state, round_keys[0])

    for rnd in range(1,10):
        _sub_bytes(state)
        _shift_rows(state)
        _mix_columns(state)
        _add_round_key(state, round_keys[rnd])

    _sub_bytes(state)
    _shift_rows(state)
    _add_round_key(state, round_keys[10])

    out = _matrix_to_bytes(state)
    return out.hex()

def decrypt_block(cipher_hex, key16):

    if not isinstance(cipher_hex, str) or len(cipher_hex) != 32:
        raise ValueError("cipher_hex must be 32 hex characters (16 bytes)")
    try:
        ct = bytes.fromhex(cipher_hex)
    except Exception:
        raise ValueError("cipher_hex is not valid hex")

    if isinstance(key16, str):
        key = key16.encode('latin-1')
    else:
        key = bytes(key16)
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes/chars")

    round_keys = _expand_key(key)
    state = _bytes_to_matrix(ct)

    _add_round_key(state, round_keys[10])
    _inv_shift_rows(state)
    _inv_sub_bytes(state)

    for rnd in range(9,0,-1):
        _add_round_key(state, round_keys[rnd])
        _inv_mix_columns(state)
        _inv_shift_rows(state)
        _inv_sub_bytes(state)

    _add_round_key(state, round_keys[0])

    pt_bytes = _matrix_to_bytes(state)
    return pt_bytes.decode('latin-1')

def aes_encrypt(plaintext, key):
    return encrypt_block(plaintext, key)

def aes_decrypt(cipher_hex, key):
    return decrypt_block(cipher_hex, key)
