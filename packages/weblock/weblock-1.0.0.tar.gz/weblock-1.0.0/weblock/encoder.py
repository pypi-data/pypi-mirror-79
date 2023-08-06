from base64 import b64encode, b64decode

def encode_data(data: str, key: str) -> str:
    """Encode an HTML file with a key

    Args:
        data (str): HTML contents
        key (str): Key

    Returns:
        str: Encoded output
    """

    output = []
    for i, char in enumerate(data):
        # Get the i % 2len(key) value
        i2 = i % (2 * len(key))

        # Get the i3 value
        i3 = i2 if \
            (i2 < len(key)) else \
                (max((2 * len(key)) - i2, 0) - 1)

        # Get key element
        ki = ord(key[i3])
        
        # XOR
        output.append(chr(ord(char) ^ ki))
    
    # Base64 encode data
    return b64encode(("".join(output)).encode()).decode()


def decode_data(data, key):
    """Decode an HTML file with a key

    Args:
        data (str): HTML contents
        key (str): Key

    Returns:
        str: Decoded output
    """

    data = b64decode(data).decode()

    output = []
    for i, char in enumerate(data):
        # Get the i % 2len(key) value
        i2 = i % (2 * len(key))

        # Get the i3 value
        i3 = i2 if \
            (i2 < len(key)) else \
                (max((2 * len(key)) - i2, 0) - 1)

        # Get key element
        ki = ord(key[i3])
        
        # XOR
        output.append(chr(ord(char) ^ ki))
    
    # Base64 encode data
    return ("".join(output))