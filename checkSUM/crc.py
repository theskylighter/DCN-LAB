def xor(a, b):
    """Performs XOR between two binary strings."""
    result = []
    for i in range(1, len(b)):  # Ignore first bit (leading 1 is always removed)
        result.append('1' if a[i] != b[i] else '0')
    return ''.join(result)


def mod2div(dividend, divisor):
    """Performs Mod-2 division (binary division using XOR)."""
    pick = len(divisor)
    tmp = dividend[:pick]  # Take initial part of the dividend

    while pick < len(dividend):
        if tmp[0] == '1':  # Perform XOR if the first bit is 1
            tmp = xor(tmp, divisor) + dividend[pick]
        else:  # If first bit is 0, XOR with all 0s
            tmp = xor(tmp, '0' * pick) + dividend[pick]

        pick += 1

    # Last step of XOR
    if tmp[0] == '1':
        tmp = xor(tmp, divisor)
    else:
        tmp = xor(tmp, '0' * pick)

    return tmp  # Remainder


def encode_crc(data, generator):
    """Encodes data by appending CRC checksum."""
    n = len(generator) - 1
    augmented_data = data + '0' * n  # Append n zeros
    remainder = mod2div(augmented_data, generator)
    return data + remainder  # Encoded frame


def decode_crc(received_data, generator):
    """Checks if received data has an error using CRC verification."""
    remainder = mod2div(received_data, generator)
    return remainder == '0' * (len(generator) - 1)  # If remainder is all 0s, no error


# Example Usage
if __name__ == "__main__":
    data = "11010011101100"  # Example binary data
    generator = "1101"  # Example generator polynomial (x^3 + x + 1)

    print(f"Original Data: {data}")
    encoded_data = encode_crc(data, generator)
    print(f"Encoded Data with CRC: {encoded_data}")

    # Simulate corruption
    corrupted_data = encoded_data[:5] + ('1' if encoded_data[5] == '0' else '0') + encoded_data[6:]

    # Checking received message
    if decode_crc(encoded_data, generator):
        print("No Error Detected (Valid Transmission)")
    else:
        print("Error Detected in Transmission!")

    if decode_crc(corrupted_data, generator):
        print("No Error Detected (Valid Transmission)")
    else:
        print("Error Detected in Corrupted Data!")

