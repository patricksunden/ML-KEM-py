"""
Project functions file.
"""
import math
from Crypto.Hash import SHAKE128

Q_VAL = 3329

BITREV7_NTT_MODQ = [
    1,      1729,   2580,   3289,   2642,   630,    1897,   848,
    1062,   1919,   193,    797,    2786,   3260,   569,    1746,
    296,    2447,   1339,   1476,   3046,   56,     2240,   1333,
    1426,   2094,   535,    2882,   2393,   2879,   1974,   821,
    289,    331,    3253,   1756,   1197,   2304,   2277,   2055,
    650,    1977,   2513,   632,    2865,   33,     1320,   1915,
    2319,   1435,   807,    452,    1438,   2868,   1534,   2402,
    2647,   2617,   1481,   648,    2474,   3110,   1227,   910,
    17,     2761,   583,    2649,   1637,   723,    2288,   1100,
    1409,   2662,   3281,   233,    756,    2156,   3015,   3050,
    1703,   1651,   2789,   1789,   1847,   952,    1461,   2687,
    939,    2308,   2437,   2388,   733,    2337,   268,    641,
    1584,   2298,   2037,   3220,   375,    2549,   2090,   1645,
    1063,   319,    2773,   757,    2099,   561,    2466,   2594,
    2804,   1092,   403,    1026,   1143,   2150,   2775,   886,
    1722,   1212,   1874,   1029,   2110,   2935,   885,    2154 ]

BITREV7_NTT_MODQ_2 = [
    17,     -17,    2761,   -2761,  583,    -583,   2649,   -2649,
    1637,   -1637,  723,    -723,   2288,   -2288,  1100,   -1100,
    1409,   -1409,  2662,   -2662,  3281,   -3281,  233,    -233,
    756,    -756,   2156,   -2156,  3015,   -3015,  3050,   -3050,
    1703,   -1703,  1651,   -1651,  2789,   -2789,  1789,   -1789,
    1847,   -1847,  952,    -952,   1461,   -1461,  2687,   -2687,
    939,    -939,   2308,   -2308,  2437,   -2437,  2388,   -2388,
    733,    -733,   2337,   -2337,  268,    -268,   641,    -641,
    1584,   -1584,  2298,   -2298,  2037,   -2037,  3220,   -3220,
    375,    -375,   2549,   -2549,  2090,   -2090,  1645,   -1645,
    1063,   -1063,  319,    -319,   2773,   -2773,  757,    -757,
    2099,   -2099,  561,    -561,   2466,   -2466,  2594,   -2594,
    2804,   -2804,  1092,   -1092,  403,    -403,   1026,   -1026,
    1143,   -1143,  2150,   -2150,  2775,   -2775,  886,    -886,
    1722,   -1722,  1212,   -1212,  1874,   -1874,  1029,   -1029,
    2110,   -2110,  2935,   -2935,  885,    -885,   2154,   -2154 ]

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

# Computes NTT representation 𝑓 of the given polynomial 𝑓 ∈ 𝑅𝑞.
# The input of ntt is a set of 256 coefficients (array)
def ntt(f):

    if len(f) != 256:
        raise ValueError("Received an improper length, the seed must be exactly 256.")
    if not type(f) is list:
        raise TypeError("The input needs to be a list.")
    
    i = 1
    length = 128
    start = 0

    print(length)
    while length >= 2:
        for start in range(0, 256, length * 2):
            zeta = BITREV7_NTT_MODQ[i]
            i += 1
            for j in range(start, start + length):
                t = (zeta * f[j + length]) % Q_VAL
                f[j + length] = (f[j] - t) % Q_VAL
                f[j] = (f[j] + t) % Q_VAL
        length //= 2
    return f

# Computes ̂the polynomial 𝑓 ∈ 𝑅𝑞 that corresponds to the given NTT representation 𝑓 ∈ 𝑇𝑞.
# input (f) is an array
def inverse_ntt(f):

    if len(f) != 256:
        raise ValueError("Received an improper length, the array length must be exactly 256.")
    if not type(f) is list:
        raise TypeError("The input needs to be a list.")
    
    length = 2
    i = 127
    start = 0
    while length <= 128:
        for start in range(0, 256, length * 2):
            zeta = BITREV7_NTT_MODQ[i]
            i -= 1
            for j in range(start, start + length):
                t = f[j]
                f[j] = (t + f[j + length]) % Q_VAL
                f[j + length] = (zeta * (f[j + length] - t)) % Q_VAL
        length *= 2
    for entry in f:
        entry = (entry * 3303) % Q_VAL
    return f

# input is two arrays f, g

# "Computes the product (in the ring 𝑇𝑞) of two NTT representations."
def multiply_ntt(f, g):

    if len(f) != 256 and len(g) != 256:
        raise ValueError("The length of the input arrays need to be exactly 256.")
    
    if not type(f) is list or not type(g) is list:
        raise TypeError("The input needs to be a list.")
    # Have to initialize the list first
    h = [0] * 256

    for i in range(0, 128):
        tuple = base_case_multiply(f[2*i], f[2*i+1], g[2*i], g[2*i+1], BITREV7_NTT_MODQ_2[i])
        h[2*i] += tuple[0]
        h[2*i+1] = tuple [1]

        # output is an array, h
        # the output consists of the coefficients of the product of the inputs
    return h


# "Computes the product of two degree-one polynomials with respect to a quadratic modulus"
def base_case_multiply(a0, a1, b0, b1, gamma):

    if not(type(a0) or type(a1) or type(b0) or type(b1) or type(gamma)) is int:
        raise TypeError("The inputs need to be of type int")

    c0 = ((a0 * b0) + (a1 * b1 * gamma)) % Q_VAL
    c1 = ((a0 * b1) + (a1 * b0)) % Q_VAL
    return (c0, c1)
