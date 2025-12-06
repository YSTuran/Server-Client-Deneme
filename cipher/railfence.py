def rail_encrypt(text, rails=3):
    text = text.replace(" ", "*")

    rail = [""] * rails
    direction = 1
    row = 0

    for c in text:
        rail[row] += c
        row += direction

        if row == rails - 1 or row == 0:
            direction *= -1

    return "".join(rail)


def rail_decrypt(text, rails=3):
    pattern = [0] * len(text)
    direction = 1
    row = 0

    for i in range(len(text)):
        pattern[i] = row
        row += direction
        if row == rails - 1 or row == 0:
            direction *= -1

    rail_lengths = [pattern.count(r) for r in range(rails)]
    rails_str = []
    index = 0

    for length in rail_lengths:
        rails_str.append(text[index:index+length])
        index += length

    pos = [0] * rails
    result = ""

    for r in pattern:
        result += rails_str[r][pos[r]]
        pos[r] += 1

    return result.replace("*", " ")
