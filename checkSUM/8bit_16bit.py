def compute_checksum_8bit(data):
    """Computes 8-bit checksum using one's complement sum."""
    checksum = sum(data) & 0xFF  # Keep within 8-bit
    return ~checksum & 0xFF  # One's complement


def verify_checksum_8bit(data):
    """Verifies 8-bit checksum. Returns True if valid, False if corrupted."""
    checksum = compute_checksum_8bit(data)
    data.append(checksum)
    return compute_checksum_8bit(data) == 0xFF


def compute_checksum_16bit(data):
    """Computes 16-bit checksum using one's complement sum."""
    checksum = sum(data) & 0xFFFF  # Keep within 16-bit
    return ~checksum & 0xFFFF  # One's complement


def verify_checksum_16bit(data):
    """Verifies 16-bit checksum. Returns True if valid, False if corrupted."""
    checksum = compute_checksum_16bit(data)
    data.append(checksum)
    return compute_checksum_16bit(data) == 0xFFFF


# Demonstrate checksum
def demonstrate_checksum():
    # 8-bit Checksum Example
    data8 = [10, 20, 30, 40, 50]
    checksum8 = compute_checksum_8bit(data8)
    data8.append(checksum8)
    
    print(f"8-bit Checksum: {checksum8}")

    # Corrupt the data
    data8[2] ^= 0x01  # Flip one bit in the third byte

    if verify_checksum_8bit(data8):
        print("8-bit Checksum Verified: No Error")
    else:
        print("8-bit Checksum Verification Failed: Data Corrupted!")

    # 16-bit Checksum Example
    data16 = [1000, 2000, 3000, 4000, 5000]
    checksum16 = compute_checksum_16bit(data16)
    data16.append(checksum16)

    print(f"16-bit Checksum: {checksum16}")

    # Corrupt the data
    data16[1] ^= 0x0001  # Flip one bit in the second word

    if verify_checksum_16bit(data16):
        print("16-bit Checksum Verified: No Error")
    else:
        print("16-bit Checksum Verification Failed: Data Corrupted!")


if __name__ == "__main__":
    demonstrate_checksum()
