from utils import *


class EncodingTable(object):
    maxAddress = 2 ** 16
    initIndex = 2 ** 8

    def __init__(self):
        self.table = {}
        self._i = EncodingTable.initIndex

    def add(self, key):
        self.table[key] = self._i
        self._i += 1

    def get(self, key):
        if len(key) == 1:
            return key[0]
        else:
            return self.table.get(key)

    def reset(self):
        self.table = {}
        self._i = EncodingTable.initIndex

    def isfull(self):
        return self._i == EncodingTable.maxAddress


class EncodingOutput(object):
    def __init__(self):
        self.data = []
        pass

    # number → 2bytes data
    def append(self, coding_number):
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


def _encode(src):
    table = EncodingTable()
    output = EncodingOutput()
    prev, curr = b'', b''
    i, length = 0, len(src)
    while i < length:
        curr = bytes([src[i]])
        record = prev + curr
        if table.get(record) is None:
            table.add(record)
            output.append(table.get(prev))
            if table.isfull():
                table.reset()
            prev = curr
        else:
            prev += curr
        i += 1
    if len(prev) > 0:
        prev_coding = table.get(prev)
        output.append(prev_coding)
    return output.data
    pass


def encode(input_path, output_path):
    source = bytes_from_path(input_path)
    data = _encode(source)
    write_to_path(output_path, data)
