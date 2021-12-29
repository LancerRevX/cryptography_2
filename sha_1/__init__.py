from bitarray import bitarray
from bitarray.util import int2ba, ba2int
from numpy import uint32
from dataclasses import dataclass
from struct import pack, unpack


@dataclass
class Buffer:
    a: uint32
    b: uint32
    c: uint32
    d: uint32
    e: uint32


def cyclic_shift_left(value: uint32, shift: uint32) -> uint32:
    return value << shift | value >> uint32(32) - shift


def sha1(message: str) -> str:
    message_bits = bitarray()
    message_bits.frombytes(message.encode('utf-8'))
    initial_length = len(message_bits)
    message_bits.append(1)
    while len(message_bits) % 512 != 448:
        message_bits.append(0)
    message_bits.extend(int2ba(initial_length, 64))

    buffer = [uint32(0x67452301),
              uint32(0xEFCDAB89),
              uint32(0x98BADCFE),
              uint32(0x10325476),
              uint32(0xC3D2E1F0)]

    for i in range(len(message_bits) // 512):
        a, b, c, d, e = buffer

        block = message_bits[i*512:i*512+512]
        block = [uint32(ba2int(block[j * 32:j * 32 + 32])) for j in range(16)]

        # block = [block[x * 32:x * 32 + 32] for x in range(16)]
        # block = [uint32(int.from_bytes(word.tobytes(), 'little')) for word in block]
        w = [uint32(0)] * 80
        for t in range(80):
            if t <= 15:
                w[t] = block[t]
            else:
                w[t] = cyclic_shift_left(w[t - 3] ^ w[t - 8] ^ w[t - 14] ^ w[t - 16], uint32(1))

            if 0 <= t <= 19:
                f = b & c | ~b & d
                k = uint32(0x5A827999)
            elif 20 <= t <= 39:
                f = b ^ c ^ d
                k = uint32(0x6ED9EBA1)
            elif 40 <= t <= 59:
                f = b & c | b & d | c & d
                k = uint32(0x8F1BBCDC)
            else:
                f = b ^ c ^ d
                k = uint32(0xCA62C1D6)
            result = cyclic_shift_left(a, uint32(5)) + f + e + k + w[t]
            a, b, c, d, e = result, a, cyclic_shift_left(b, uint32(30)), c, d

        buffer[0] += a
        buffer[1] += b
        buffer[2] += c
        buffer[3] += d
        buffer[4] += e

    return f'{buffer[0]:08x}{buffer[1]:08x}{buffer[2]:08x}{buffer[3]:08x}{buffer[4]:08x}'


import struct


class SHA1Hash:
    """
    Class to contain the entire pipeline for SHA1 Hashing Algorithm
    >>> SHA1Hash(bytes('Allan', 'utf-8')).final_hash()
    '872af2d8ac3d8695387e7c804bf0e02c18df9e6e'
    """

    def __init__(self, data):
        """
        Inititates the variables data and h. h is a list of 5 8-digit Hexadecimal
        numbers corresponding to
        (1732584193, 4023233417, 2562383102, 271733878, 3285377520)
        respectively. We will start with this as a message digest. 0x is how you write
        Hexadecimal numbers in Python
        """
        self.data = data
        self.h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    @staticmethod
    def rotate(n, b):
        """
        Static method to be used inside other methods. Left rotates n by b.
        >>> SHA1Hash('').rotate(12,2)
        48
        """
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    def padding(self):
        """
        Pads the input message with zeros so that padded_data has 64 bytes or 512 bits
        """
        padding = b"\x80" + b"\x00" * (63 - (len(self.data) + 8) % 64)
        padded_data = self.data + padding + struct.pack(">Q", 8 * len(self.data))
        return padded_data

    def split_blocks(self):
        """
        Returns a list of bytestrings each of length 64
        """
        return [
            self.padded_data[i : i + 64] for i in range(0, len(self.padded_data), 64)
        ]

    # @staticmethod
    def expand_block(self, block):
        """
        Takes a bytestring-block of length 64, unpacks it to a list of integers and
        returns a list of 80 integers after some bit operations
        """
        w = list(struct.unpack(">16L", block)) + [0] * 64
        for i in range(16, 80):
            w[i] = self.rotate((w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]), 1)
        return w

    def final_hash(self):
        """
        Calls all the other methods to process the input. Pads the data, then splits
        into blocks and then does a series of operations for each block (including
        expansion).
        For each block, the variable h that was initialized is copied to a,b,c,d,e
        and these 5 variables a,b,c,d,e undergo several changes. After all the blocks
        are processed, these 5 variables are pairwise added to h ie a to h[0], b to h[1]
        and so on.  This h becomes our final hash which is returned.
        """
        self.padded_data = self.padding()
        self.blocks = self.split_blocks()
        for block in self.blocks:
            expanded_block = self.expand_block(block)
            a, b, c, d, e = self.h
            for i in range(0, 80):
                if 0 <= i < 20:
                    f = (b & c) | ((~b) & d)
                    k = 0x5A827999
                elif 20 <= i < 40:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif 40 <= i < 60:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8F1BBCDC
                elif 60 <= i < 80:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6
                a, b, c, d, e = (
                    self.rotate(a, 5) + f + e + k + expanded_block[i] & 0xFFFFFFFF,
                    a,
                    self.rotate(b, 30),
                    c,
                    d,
                )
            self.h = (
                self.h[0] + a & 0xFFFFFFFF,
                self.h[1] + b & 0xFFFFFFFF,
                self.h[2] + c & 0xFFFFFFFF,
                self.h[3] + d & 0xFFFFFFFF,
                self.h[4] + e & 0xFFFFFFFF,
            )
        return "%08x%08x%08x%08x%08x" % tuple(self.h)

