grid = {
    "A":"11","B":"12","C":"13","D":"14","E":"15",
    "F":"21","G":"22","H":"23","I":"24","J":"24","K":"25",
    "L":"31","M":"32","N":"33","O":"34","P":"35",
    "Q":"41","R":"42","S":"43","T":"44","U":"45",
    "V":"51","W":"52","X":"53","Y":"54","Z":"55"
}

reverse = {v:k for k,v in grid.items()}

def polybius_encrypt(text):
    text = text.replace(" ", "*")
    return "".join(grid.get(c.upper(), c) for c in text)

def polybius_decrypt(text):
    result = ""
    i = 0
    while i < len(text):
        if text[i] == "*":
            result += " "
            i += 1
        else:
            code = text[i:i+2]
            i += 2
            result += reverse.get(code, "?")
    return result
