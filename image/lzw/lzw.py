import sys
import os
from utils import *

class EncodingTable(object):
    def __init__(self):
        self.table = {}
        self._total = 256

    def add(self, key):
        self.table[key] = self._total
        self._total += 1

    def get(self, key):
        if len(key) == 1:
            return key[0]
        else:
            return self.table.get(key)


class DecodingTable(object):
    kValueIncreasment = -1

    def __init__(self):
        self.table = {}
        self._total = 256

    def set(self, key, value=kValueIncreasment):
        if value == DecodingTable.kValueIncreasment:
            self.table[key] = self._total
            self._total += 1
        else:
            self.table[key] = value
            self._total += 1

    def get(self, item):
        if item < 256:
            return chr(item)
        else:
            return self.table.get(item)


class EncodingOutput(object):
    def __init__(self):
        self.data = []
        pass

    # number → 2bytes data
    def append(self, coding_number):
        # if coding_number > 0xffff:
        # log(coding_number)
        # pass

        if coding_number < 256:
            self.data.append(0x00)
            self.data.append(coding_number)
        else:
            self.data.append((coding_number >> 8))
            self.data.append((coding_number & 0x00FF))
        pass

    def write(self, path):
        with open(path, 'wb') as f:
            f.write(bytes(self.data))


class DecodingInput(object):
    def __init__(self, raw):
        length = len(raw)
        self.data = []
        for j in range(0, length, 2):
            self.data.append(int.from_bytes(raw[j: j + 2], 'big'))
        self.length = int(length / 2)
        self.i = 0

    def next(self):
        if self.i < self.length:
            self.i += 1
            return self.data[self.i - 1]
        return None


def _encode(src):
    table = EncodingTable()
    output = EncodingOutput()
    prev, curr = b'', b''
    i, length = 0, len(src)
    while i < length:
        curr = bytes([src[i]])
        record = prev + curr
        if table.get(record) is None:
            prev_coding = table.get(prev)
            output.append(prev_coding)
            table.add(record)
            prev = curr
        else:
            prev += curr
        i += 1
    if len(prev) > 0:
        prev_coding = table.get(prev)
        output.append(prev_coding)
    return output.data
    pass


def append_result(result, item):
    a = [ord(e) for e in item]
    result += a


def _decode(coding):
    table = DecodingTable()
    input = DecodingInput(coding)
    result = []

    # 初始态
    prev, curr = '', ''

    # 读入第一个字符
    curr_code = input.next()
    curr = table.get(curr_code)
    append_result(result, curr)
    prev_code = curr_code

    # 读入下一个字符
    curr_code = input.next()
    while curr_code is not None:
        curr = table.get(curr_code)
        if curr is not None:
            append_result(result, curr)
            prev = table.get(prev_code)
            curr = table.get(curr_code)[0]
            table.set(table._total, prev + curr)
            pass
        else:
            prev = table.get(prev_code)
            curr = table.get(prev_code)[0]
            table.set(curr_code, prev + curr)
            append_result(result, prev + curr)
            pass
        prev_code = curr_code
        curr_code = input.next()

    return result
    pass


def bytes_from_path(path):
    s = []
    with open(path, 'rb') as f:
        s = f.read()
    return s


def write_to_path(path, raw):
    with open(path, 'wb') as f:
        f.write(bytes(raw))


def rename(path, suffix='rename'):
    a = path.split('.')
    a[-1] = suffix
    b = '.'.join(a)
    return b


def encode(input_path, output_path):
    source = bytes_from_path(input_path)
    data = _encode(source)
    write_to_path(output_path, data)


def decode(input_path, output_path):
    source = bytes_from_path(input_path)
    data = _decode(source)
    write_to_path(output_path, data)


def cli():
    args = sys.argv[1:]
    coding = True if len(args) == 1 else False
    if coding:
        input_path = args[0]
        output_path = rename(input_path, 'lzw')
        encode(input_path, output_path)
    else:
        input_path = args[0]
        output_path = args[1]
        decode(input_path, output_path)


if __name__ == '__main__':
    cli()
