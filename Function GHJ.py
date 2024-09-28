import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Function J: J(s) = SHAKE256(s, 8 * 32)
def J(s: bytes) -> bytes:
    shake256 = hashlib.shake_256()
    shake256.update(s)
    return shake256.digest(32)  # Output 32 bytes

# Function H: H(s) = SHA3-256(s)
def H(s: bytes) -> bytes:
    sha3_256 = hashlib.sha3_256()
    sha3_256.update(s)
    return sha3_256.digest()  # 32 bytes

# Function G: G(c) = SHA3-512(c), then split into two 32-byte outputs (a, b)
def G(c: bytes) -> (bytes, bytes):
    sha3_512 = hashlib.sha3_512()
    sha3_512.update(c)
    digest = sha3_512.digest()  # 64 bytes total
    a = digest[:32]  # First 32 bytes
    b = digest[32:]  # Last 32 bytes
    return a, b

# Example usage:

# Test input
data = "I love crypto".encode()  # Convert string to bytes

# Call H function
h_result = H(data)
print(f"H(data): {h_result.hex()}")

# Call J function
j_result = J(data)
print(f"J(data): {j_result.hex()}")

# Call G function
a, b = G(data)
print(f"G(data): a = {a.hex()}, b = {b.hex()}")