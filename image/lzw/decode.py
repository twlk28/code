from utils import *


class DecodingTable(object):
    maxAddress = 2 ** 16
    initIndex = 2 ** 8

    def __init__(self):
        self.table = {}
        self._i = DecodingTable.initIndex

    def set(self, key, value):
        self.table[key] = value
        self._i += 1
        if self.isfull():
            self.reset()

    def get(self, item):
        if item < 256:
            return chr(item)
        else:
            return self.table.get(item)

    def reset(self):
        self.table = {}
        self._i = DecodingTable.initIndex

    def isfull(self):
        return self._i == DecodingTable.maxAddress


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
            table.set(table._i, prev + curr)
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


def decode(input_path, output_path):
    source = bytes_from_path(input_path)
    data = _decode(source)
    write_to_path(output_path, data)
