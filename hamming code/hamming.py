def get_parity_positions_for_encoding(data_bits):
    """Calculate the number of parity bits required for encoding"""
    r = 0
    while (2 ** r) < (len(data_bits) + r + 1):
        r += 1
    return r

def get_parity_positions_for_error_detection(received_code):
    """Calculate the number of parity bits in the received code"""
    r = 0
    while (2 ** r) <= len(received_code):  # Fixed condition
        r += 1
    return r - 1  # Adjust because we stop at r where 2^r > len(received_code)

def insert_parity_bits(data_bits):
    """Insert parity bits at positions 1, 2, 4, 8, ..."""
    r = get_parity_positions_for_encoding(data_bits)
    hamming_code = []
    j = 0  # To track parity positions
    k = 0  # To track data positions

    for i in range(1, len(data_bits) + r + 1):
        if i == 2 ** j:  # Parity bit position
            hamming_code.append(0)  # Placeholder
            j += 1
        else:
            hamming_code.append(int(data_bits[k]))
            k += 1
    return hamming_code, r

def calculate_parity_bits(hamming_code, r):
    """Calculate and set parity bits in the Hamming code"""
    n = len(hamming_code)
    for i in range(r):
        parity_pos = 2 ** i
        parity_value = 0
        for j in range(1, n + 1):
            if j & parity_pos:  # Check if the bit position is included
                parity_value ^= hamming_code[j - 1]
        hamming_code[parity_pos - 1] = parity_value  # Set parity bit
    return hamming_code

def encode_hamming(data_bits):
    """Generate Hamming code for given data bits"""
    hamming_code, r = insert_parity_bits(data_bits)
    hamming_code = calculate_parity_bits(hamming_code, r)
    return hamming_code

def detect_and_correct_error(received_code):
    """Detect and correct a single-bit error in received Hamming code"""
    n = len(received_code)
    r = get_parity_positions_for_error_detection(received_code)  # Corrected r calculation
    error_position = 0

    for i in range(r):
        parity_pos = 2 ** i
        parity_value = 0
        for j in range(1, n + 1):
            if j & parity_pos:
                parity_value ^= received_code[j - 1]
        if parity_value != 0:
            error_position += parity_pos

    if error_position:
        print(f"Error detected at position: {error_position}")
        received_code[error_position - 1] ^= 1  # Correct error
        print("Corrected Hamming Code:", received_code)
    else:
        print("No error detected.")

    return received_code

# Example usage
data_bits = "1011"
print("Original Data Bits:", data_bits)

hamming_code = encode_hamming(data_bits)
print("Encoded Hamming Code:", hamming_code)

# Introduce an error (e.g., flip bit at position 3)
received_code = hamming_code[:]
received_code[2] ^= 1  # Flipping bit at position 3
print("Received Code with Error:", received_code)

# Detect and correct error
corrected_code = detect_and_correct_error(received_code)