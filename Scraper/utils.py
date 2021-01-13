from base64 import b64decode, b64encode

def _decode(secret_string, reverse=True):
    secret_bytes = (secret_string[::-1].encode('utf-8')
                    if reverse
                    else secret_string.encode('utf-8'))

    return b64decode(secret_bytes).decode('utf-8')

def _encode(plain_text, reverse):
    encoded_bytes = plain_text.encode('utf-8')

    if reverse:
        return b64encode(encoded_bytes).decode('utf-8')[::-1]
    return b64encode(encoded_bytes).decode('utf-8')
