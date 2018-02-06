from utils import log

class LookAhead():
    def __init__(self, size=4):
        self.bit_size = size
        self.size = 2**size
        self.data = [0 for _ in range(self.size)]
        self.stream = None
        self.index = 0

    def fill(self, stream):
        self.stream = stream
        for _ in range(self.size):
            self.consume()
        pass

    def consume(self):
        n = next(self.stream, None)
        if n is None:
            self.data[self.index] = None
        else:
            self.data[self.index] = ord(n)
        self.index = (self.index + 1) % self.size
        pass

    def take1(self):
        i = (self.index) % self.size
        v = self.data[i]
        return v
        pass

    pass

class SearchBuffer():
    def __init__(self, size=12):
        self.bit_size = size
        self.size = 2**size
        self.data = []
        self.bit_count = 0
        self.index = 0
        self.done = False

    def clear(self):
        self.data = []
        self.bit_count = 0
        self.index = 0
        self.done = False

    def _append(self, bytes):
        for b in bytes:
            if self.bit_count < self.size:
                self.bit_count += 1
                self.data.append(b)
            else:
                self.data = self.data[1:]
                self.data.append(b)
        pass

    def _append_1byte(self, b):
        if self.bit_count < self.size:
            self.bit_count += 1
            self.data.append(b)
        else:
            self.data = self.data[1:]
            self.data.append(b)

    def _search(self, sub_bytes):
        found = bytes(self.data).find(sub_bytes)
        return found

    def consume(self, lookahead):
        bs, data, last_index = [], [], -1
        b = lookahead.take1()
        while b is not None:
            # log('next:({})'.format(hex(b)))
            bs.append(b)
            if len(bs) > lookahead.size:
                bs.pop()
                data = bytes(bs)
                break
            found_index = self._search(bytes(bs))
            if found_index == -1:
                bs.pop()
                if len(bs) == 0:
                    data = bytes([b])
                    lookahead.consume()
                    break
                else:
                    data = bytes(bs)
                    break
            else:
                last_index = found_index
                lookahead.consume()
                b = lookahead.take1()
                if b is None:
                    self.done = True
                    data = bytes(bs)
                    break
                else:
                    continue

        self._append(data)
        if len(data) < 3:
            return data
        else:
            return (last_index, len(data))
        pass

    def bytes_from_range(self, r):
        start, length = r
        a = self.data[start: start+length]
        b = bytes(a)
        return b
    pass