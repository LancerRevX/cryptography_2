from bitarray import bitarray
from bitarray.util import int2ba, hex2ba, ba2int, ba2hex
from math import sin
from typing import Callable
from numpy import uint32, uint64, array
from dataclasses import dataclass
from struct import pack, unpack


@dataclass
class Buffer:
    a: uint32
    b: uint32
    c: uint32
    d: uint32


def md5(message: str) -> str:
    initial_message_bits = bitarray()
    initial_message_bits.frombytes(message.encode('utf-8'))
    message_bits = bitarray(initial_message_bits)

    message_bits.append(1)
    len_mod_512 = len(message_bits) % 512
    zeros_number = 448 - len(message_bits) % 512 if len_mod_512 <= 448 else 512 - len_mod_512 + 448
    message_bits.extend('0' * zeros_number)

    message_length = uint64(len(initial_message_bits))
    message_length_bits = bitarray(endian='big')
    message_length_bits.frombytes(pack('<Q', message_length))
    message_bits.extend(message_length_bits)

    buffer = Buffer(
        a=uint32(0x67452301),
        b=uint32(0xefcdab89),
        c=uint32(0x98badcfe),
        d=uint32(0x10325476))
    for i in range(0, len(message_bits), 512):
        aa = buffer.a
        bb = buffer.b
        cc = buffer.c
        dd = buffer.d
        process_block(message_bits[i:i+512], buffer)
        buffer.a += aa
        buffer.b += bb
        buffer.c += cc
        buffer.d += dd
    buffer.a = unpack("<I", pack(">I", buffer.a))[0]
    buffer.b = unpack("<I", pack(">I", buffer.b))[0]
    buffer.c = unpack("<I", pack(">I", buffer.c))[0]
    buffer.d = unpack("<I", pack(">I", buffer.d))[0]

    return f'{buffer.a:08x}{buffer.b:08x}{buffer.c:08x}{buffer.d:08x}'


T = array([int(2 ** 32 * abs(sin(i))) for i in range(1, 65)], uint32)
S = array([7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
           5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
           4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
           6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21], uint32)


def process_block(block_bits: bitarray, buffer: Buffer):
    def ff(x: uint32, y: uint32, z: uint32) -> uint32:
        return (x & y) | (~x & z)

    def fg(x: uint32, y: uint32, z: uint32) -> uint32:
        return (x & z) | (~z & y)

    def fh(x: uint32, y: uint32, z: uint32) -> uint32:
        return x ^ y ^ z

    def fi(x: uint32, y: uint32, z: uint32) -> uint32:
        return y ^ (~z | x)

    block = [block_bits[x * 32:x * 32 + 32] for x in range(16)]
    block = [uint32(int.from_bytes(word.tobytes(), 'little')) for word in block]

    for i in range(64):
        if 0 <= i <= 15:
            k = i
            f = ff
        elif 16 <= i <= 31:
            k = (i * 5 + 1) % 16
            f = fg
        elif 32 <= i <= 47:
            k = (i * 3 + 5) % 16
            f = fh
        else:
            k = (i * 7) % 16
            f = fi
        result = buffer.a + f(buffer.b, buffer.c, buffer.d) + block[k] + T[i]
        result = result << S[i] | result >> uint32(32) - S[i]
        result += buffer.b
        buffer.a = buffer.d
        buffer.d = buffer.c
        buffer.c = buffer.b
        buffer.b = result



