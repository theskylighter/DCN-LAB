def calculate_parity_bits(data):
    """ Calculate the 3 parity bits (P1, P2, P3) for 4-bit data """
    P1 = data[0] ^ data[1] ^ data[3]  # Covers positions 1, 3, 5, 7
    P2 = data[0] ^ data[2] ^ data[3]  # Covers positions 2, 3, 6, 7
    P3 = data[1] ^ data[2] ^ data[3]  # Covers positions 4, 5, 6, 7
    return [P1, P2, data[0], P3, data[1], data[2], data[3]]

def introduce_error(encoded_data, error_position):
    """ Introduce an error at a specific position (1-based index) """
    if error_position > 0:
        encoded_data[error_position - 1] ^= 1  # Flip the bit
    return encoded_data

def detect_and_correct_error(received_data):
    """ Detect and correct a single-bit error """
    P1 = received_data[0] ^ received_data[2] ^ received_data[4] ^ received_data[6]
    P2 = received_data[1] ^ received_data[2] ^ received_data[5] ^ received_data[6]
    P3 = received_data[3] ^ received_data[4] ^ received_data[5] ^ received_data[6]

    error_position = (P3 * 4) + (P2 * 2) + (P1 * 1)  # Convert binary to decimal

    if error_position != 0:
        print(f"Error detected at position: {error_position}")
        received_data[error_position - 1] ^= 1  # Flip the incorrect bit
        print("Corrected Data:", received_data)
    else:
        print("No error detected.")
    
    return received_data

# Example Run:
data_bits = [1, 0, 1, 1]  # 4-bit data
encoded_data = calculate_parity_bits(data_bits)
print("Encoded Data:", encoded_data)

# Simulating an error at position 4
# Using [:] creates a copy of encoded_data to avoid modifying the original list
received_data = introduce_error(encoded_data[:], 4)
print("Received Data (with error):", received_data)

# Error detection and correction
corrected_data = detect_and_correct_error(received_data)
