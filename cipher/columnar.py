def columnar_encrypt(text, key):
    text = text.replace(" ", "*")
    key_order = sorted(range(len(key)), key=lambda k: key[k])

    rows = []
    row = ""
    for c in text:
        row += c
        if len(row) == len(key):
            rows.append(row)
            row = ""

    if row:
        row += "*" * (len(key) - len(row))
        rows.append(row)

    result = ""
    for i in key_order:
        for r in rows:
            result += r[i]

    return result


def columnar_decrypt(text, key):
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    n_cols = len(key)
    n_rows = len(text) // n_cols

    grid = [[""] * n_cols for _ in range(n_rows)]

    index = 0
    for k_i in key_order:
        for r in range(n_rows):
            grid[r][k_i] = text[index]
            index += 1

    result = "".join("".join(row) for row in grid)
    return result.replace("*", " ")
