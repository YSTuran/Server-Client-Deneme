def columnar_encrypt(text, key):
    n_cols = len(key)
    key_order = sorted(range(n_cols), key=lambda k: key[k])
    
    padding_len = (n_cols - (len(text) % n_cols)) % n_cols
    text += chr(0) * padding_len

    rows = [text[i:i + n_cols] for i in range(0, len(text), n_cols)]
    
    result = ""
    for col in key_order:
        for row in rows:
            result += row[col]
    return result

def columnar_decrypt(text, key):
    n_cols = len(key)
    n_rows = len(text) // n_cols
    key_order = sorted(range(n_cols), key=lambda k: key[k])
    
    grid = [[""] * n_cols for _ in range(n_rows)]
    
    idx = 0
    for col in key_order:
        for row in range(n_rows):
            grid[row][col] = text[idx]
            idx += 1
            
    result = "".join("".join(r) for r in grid)
    return result.replace(chr(0), "")