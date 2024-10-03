"""
Project functions file.
"""
import math
from Crypto.Hash import SHAKE128

Q_VAL = 3329


def _bits_to_bytes(bit_array: list[int]) -> list[bytes]:

    if not all(x in [0, 1] for x in bit_array):
        raise ValueError("Each bit in array need to be 0 or 1")

    if len(bit_array) % 8 != 0 or len(bit_array) == 0:
        raise ValueError("Received array of bits needs to be a multiple of 8")

    bytes_array = []

    # chunk into arrays of 8 bits
    chunked = [bit_array[i:i+8] for i in range(0, len(bit_array), 8)]

    for array in chunked:
        curr = 0

        for i, val in enumerate(array):
            # least significant on the left, little endian
            curr += val*(2 ** i)

        # casting to whatever endian should not matter as we are using only one byte
        bytes_array.append(curr.to_bytes(1, "little"))

    return bytes_array


def _bytes_to_bits(byte_array: list[bytes]) -> list[int]:

    if not all(isinstance(x, bytes) for x in byte_array) or len(byte_array) == 0:
        raise ValueError("Requires an array of bytes.")

    bit_array = []
    for byte in byte_array:
        value = int.from_bytes(byte, "little")
        bit_values = [int(x) for x in f"{value:08b}"[::-1]]
        bit_array.extend(bit_values)

    return bit_array


def _byte_encode(int_array: list[int], d: int) -> list[bytes]:

    if len(int_array) != 256:
        raise ValueError(
            f"Provided array contained {len(int_array)} integers. Required length is 256")

    if not all(isinstance(x, int) for x in int_array):
        raise ValueError("int_array values must be integers")

    if (not d or not isinstance(d, int) or d > 12 or d < 1):
        raise ValueError(
            "Parameter d has to be integer between 1 and 12")

    m = 2**d if d < 12 else 3329    # The q param == 3329

    # check that provided int_array values are modulo of m
    if any(x >= m for x in int_array):
        raise ValueError(
            f"int_array contains an element exceeding the max value {m-1} for current d value {d}")

    bit_array = [0]*(len(int_array)*d)

    for i, val in enumerate(int_array):
        a = val
        for j in range(d):
            bit_array[i*d+j] = a % 2
            a = (a-bit_array[i*d+j]) // 2

    return _bits_to_bytes(bit_array)


def _byte_decode(bytes_array: list[bytes], d: int) -> list[int]:

    if not all(isinstance(x, bytes) for x in bytes_array):
        raise ValueError("bytes_array values must be bytes")

    if (not d or not isinstance(d, int) or d > 12 or d < 1):
        raise ValueError(
            "Parameter d has to be integer between 1 and 12")

    bit_array = _bytes_to_bits(bytes_array)

   # chunk into arrays of d bits
    chunked = [bit_array[i:i+d] for i in range(0, len(bit_array), d)]
    int_array = []
    for joo in chunked:
        curr = 0
        for i, val in enumerate(joo):
            curr += val*(2**i)
        int_array.append(curr)

    return int_array


def _compress(int_array: list[int], d: int) -> list[int]:

    compressed = []

    modifier = 2**d / Q_VAL

    for value in int_array:
        temp = modifier*value
        temp = math.ceil(
            temp) if temp % 1 == 0.5 else round(temp)

        compressed.append(temp % (2**d))

    return compressed


def _decompress(int_array: list[int], d: int) -> list[int]:

    decompressed = []

    modifier = Q_VAL/(2**d)

    for value in int_array:
        new_value = modifier*value
        new_value = math.ceil(
            new_value) if new_value % 1 == 0.5 else round(new_value)

        decompressed.append(new_value)

    return decompressed


def _sample_ntt(b):

    # Verify that the seed is exactly 32 bytes
    if len(b) != 32:
        raise ValueError("Received an improper length, the seed must be exactly 32 bytes.")
    
    # input parameter b is a 32-byte seed
    ctx = SHAKE128.new()
    ctx = ctx.update(b)
    j = 0
    a = []
    while j < 256:
        c = ctx.read(3)
        d1 = c[0] + 256 * (c[1] % 16)
        d2 = (c[1] // 16) + 16 * c[2]
        if d1 < Q_VAL:
            a.append(d1)
            j+=1
        if d2 < Q_VAL and j < 256:
            a.append(d2)
            j+=1
        
    return a
