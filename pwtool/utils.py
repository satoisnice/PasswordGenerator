def is_valid_char(c):
    return c.isprintable() and c not in "\n\r\t\x0b\x0c"

# len("\n") == 1