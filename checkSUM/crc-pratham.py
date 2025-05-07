def xor(a, b):
    """Perform bitwise XOR operation between two binary strings."""
    result = "".join('0' if i == j else '1' for i, j in zip(a, b))
    return result.lstrip('0')  # Remove leading zeros

def divide(data, generator):
    """Perform binary division (modulo-2) to compute CRC checksum."""
    dividend = data + '0' * (len(generator) - 1)  # Append zero bits
    divisor = generator
    
    while len(dividend) >= len(divisor):
        dividend = xor(dividend[:len(divisor)], divisor) + dividend[len(divisor):]
    
    return dividend  # Remainder is the CRC checksum

def encode(data, generator):
    """Encode data by appending CRC checksum."""
    checksum = divide(data, generator)
    return data + checksum  # Append checksum to data

def decode(received_data, generator):
    """Check for errors by performing division on received data."""
    remainder = divide(received_data, generator)
    
    if '1' in remainder:
        return "Error detected! Received data is corrupted."
    else:
        return "No error detected. Received data is correct."

# Example Usage
data = "11010011101100"  # Input binary data
polynomial = "1011"  # Generator polynomial

# Encoding Step
encoded_data = encode(data, polynomial)
print(f"Original Data: {data}")
print(f"Generator Polynomial: {polynomial}")
print(f"Encoded Data (Data + CRC): {encoded_data}")

# Decoding Step (Simulating correct reception)
print(decode(encoded_data, polynomial))

# Simulating an error in transmission
corrupted_data = encoded_data[:5] + ('1' if encoded_data[5] == '0' else '0') + encoded_data[6:]
print(f"Corrupted Data: {corrupted_data}")
print(decode(corrupted_data, polynomial))