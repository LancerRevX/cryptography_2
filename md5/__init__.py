from bitarray import bitarray
from bitarray.util import int2ba, hex2ba
from math import sin


def message_to_bits(message: str) -> bitarray:
    message_bits = bitarray()
    bitarray.frombytes(message.encode('utf-8'))
    return message_bits


def bits_to_message(message_bits: bitarray) -> str:
    return message_bits.tobytes().decode('utf-8')


def md5(initial_message_bits: bitarray):
    message_bits = bitarray(initial_message_bits)
    message_bits.append(1)
    len_mod_512 = len(message_bits) % 512
    zeros_number = 448 - len(message_bits) % 512 if len_mod_512 <= 448 else 512 - len_mod_512 + 448
    message_bits.extend('0' * zeros_number)
    message_bits += int2ba(len(initial_message_bits), 64)
    A = hex2ba('01234567')
    B = hex2ba('89ABCDEF')
    C = hex2ba('FEDCBA98')
    D = hex2ba('76543210')
    T = [int(2**32 * abs(sin(i))) for i in range(1, 65)]