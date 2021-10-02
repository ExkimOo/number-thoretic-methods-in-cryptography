def ascii_to_num(s):
    numeric_string = ""

    for i in range(len(s)):
        ascii_symbol = str(ord(s[i])).zfill(3)
        numeric_string += ascii_symbol

    return numeric_string


def num_to_ascii(numeric_string):
    s = ""

    for i in range(0, len(numeric_string), 3):
        s += chr(int(numeric_string[i:i+3]))

    return s