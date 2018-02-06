import sys

from lib import LookAhead, SearchBuffer
from utils import *


class LZSS():
    def __init__(self, lookahead_size=4):
        self.lookahead = LookAhead(lookahead_size)
        self.searching = SearchBuffer(16 - lookahead_size)
        pass

    def _encode(self, stream):
        # reset self.props if need.
        bits = []
        self.lookahead.fill(stream)
        while not self.searching.done:
            found = self.searching.consume(self.lookahead)
            if type(found) is tuple:
                bits += self.bits_from_tuple(found)
            else:
                bits += self.bits_from_bytes(found)
        data = self.bytes_from_bits(bits)
        return data

    def encode(self, input_path, output_path):
        self.searching.clear()
        f = open(input_path, 'rb')
        r = self._encode(LZSS.streamable(f))
        f.close()
        LZSS.write(r, output_path)
        pass

    def _decode(self, stream):
        kLeadingByte = 0
        kLeadingTuple = 1
        out, i, leadingType = [], 0, kLeadingByte
        bits = []
        range_start, range_len = 0, 0
        bit = next(stream, None)
        while bit is not None:
            if i == 0:
                leadingType = bit
                bit = next(stream, None)
                i += 1
                continue
            if leadingType == kLeadingByte:
                if i < 8:
                    bits.append(bit)
                    bit = next(stream, None)
                    i += 1
                    continue
                else:
                    bits.append(bit)
                    byte = LZSS.val_from_bits(bits)
                    self.searching._append_1byte(byte)
                    # log('add({})'.format(byte), i)
                    out.append(byte)
                    bit = next(stream, None)
                    i = 0
                    bits = []
                    continue
            else:
                if i < 9:
                    bits.append(bit)
                    bit = next(stream, None)
                    i += 1
                elif i == 9:  # skip
                    bit = next(stream, None)
                    i += 1
                elif i < self.searching.bit_size + 1:
                    bits.append(bit)
                    bit = next(stream, None)
                    i += 1
                elif i == self.searching.bit_size + 1:
                    bits.append(bit)
                    range_start = LZSS.val_from_bits(bits)
                    bit = next(stream, None)
                    i += 1
                    bits = []
                elif i < 17:
                    bits.append(bit)
                    bit = next(stream, None)
                    i += 1
                elif i == 17:
                    bits.append(bit)
                    range_len = LZSS.val_from_bits(bits) + 1
                    r = (range_start, range_len)
                    data = self.searching.bytes_from_range(r)
                    self.searching._append(data)
                    # log('add({})'.format(data), i)
                    out += list(data)
                    bit = next(stream, None)
                    i = 0
                    bits = []
                pass
            pass
        data = bytes(out)
        return data

    def decode(self, input_path, output_path):
        self.searching.clear()
        f = open(input_path, 'rb')
        r = self._decode(LZSS.bitsable(f))
        f.close()
        LZSS.write(r, output_path)
        pass

    def bits_from_bytes(self, bs):
        a = []
        leading = 0
        for b in bs:
            bits = [(b >> i) & 1 for i in reversed(range(8))]
            a += ([leading] + bits)
        return a

    def bits_from_tuple(self, tp):
        leading = 1
        b1, b2 = tp
        b2 = b2 - 1  # 长度编码 = 值-1; 比如4位, 长度范围 1-16 对应编码 0-15
        size1 = 16 - self.lookahead.bit_size
        size2 = self.lookahead.bit_size
        b1_bits = [(b1 >> i) & 1 for i in reversed(range(size1))]
        b2_bits = [(b2 >> i) & 1 for i in reversed(range(size2))]
        a = [leading] + b1_bits[0:8] + [leading] + b1_bits[8:size1] + b2_bits
        return a

    def bytes_from_bits(self, bits):
        data = []
        v = 0
        i = 7
        for b in bits:
            if i > 0:
                v = ((b << i) | v)
                i -= 1
            else:
                v = ((b << i) | v)
                data.append(v)
                v = 0
                i = 7

        # 最后一位不满8bit的情况
        if i != 7:
            data.append(v)
        return bytes(data)

    @staticmethod
    def streamable(file):
        while True:
            data = file.read(1)
            if not data:
                break
            yield data

    @staticmethod
    def bitsable(file):
        bytes = (b for b in file.read())
        for b in bytes:
            for i in reversed(range(8)):
                yield ((b >> i) & 1)

    @staticmethod
    def write(bytes, path):
        with open(path, 'wb') as f:
            f.write(bytes)
        pass

    @staticmethod
    def byte_from_bit8(bit8):
        v = 0
        for i in range(8):
            v |= (bit8[i] << (7 - i))
        return v

    @staticmethod
    def val_from_bits(bits):
        v = 0
        length = len(bits)
        for i in range(length):
            v |= (bits[i] << (length - 1 - i))
        return v

    pass


def cli():
    lzss = LZSS()
    args = sys.argv[1:]
    coding = True if len(args) == 1 else False
    if coding:
        input_path = args[0]
        output_path = rename(input_path, 'lzss')
        lzss.encode(input_path, output_path)
    else:
        input_path = args[0]
        output_path = args[1]
        lzss.decode(input_path, output_path)


if __name__ == '__main__':
    cli()
