"""
Project functions file.
"""


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


def _byte_encode():
    pass


def _byte_decode():
    pass


def _compress():
    pass


def _decompress():
    pass


def _sample_ntt():
    pass
