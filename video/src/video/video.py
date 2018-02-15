from struct import pack, unpack


class Davi(object):
    d = {
        'identifier': ('4s', 0, 4),
        'version': ('4s', 4, 8),
        'frames': ('B', 8, 9),
        'width': ('H', 9, 11),
        'height': ('H', 11, 13),
    }

    def __init__(self):
        self.meta = {}
        self.diff = []
        self.vblock = []
        self._setup_meta()
        self.width = 0
        self.heigth = 0
        self.frames = 0
        pass

    @classmethod
    def from_bytes(cls, data):
        this = cls()
        # meta
        i = 0
        for k, info in Davi.d.items():
            fmt, start, end = info
            if fmt[-1] == 's':
                this.meta[k] = unpack(fmt, data[start:end])[0].decode('ascii')[0]
            else:
                this.meta[k] = unpack(fmt, data[start:end])[0]
            i += (end - start)
        this.width = this.meta['width']
        this.heigth = this.meta['height']
        this.frames = this.meta['frames']

        # diff
        n = 0
        while n < this.meta['frames']:
            diff_item = {}
            size = unpack('I', data[i:i + 4])[0]
            diff_item['size'] = size
            diff_item['data'] = data[i + 4: i + 4 + size]
            i += (4 + size)
            n += 1
            this.diff.append(diff_item)

        # vblock
        size_of_data = len(data)
        size_of_pair = 4
        numbers_of_pair = int(this.meta['width'] / 8) * int(this.meta['height'] / 8)
        while i < size_of_data:
            vblock_item = []
            j = 0
            while j < numbers_of_pair:
                jj = j * size_of_pair
                pair = {
                    'x': unpack('H', data[i + jj: i + jj + 2])[0],
                    'y': unpack('H', data[i + jj + 2: i + jj + 4])[0],
                }
                j += 1
                vblock_item.append(pair)
            i += numbers_of_pair * size_of_pair
            this.vblock.append(vblock_item)
        return this

    def _setup_meta(self):
        self.meta['identifier'] = 'davi'
        self.meta['version'] = '1.0\n'
        pass

    def write_meta(self, frames, width, height):
        self.meta['frames'] = frames
        self.meta['width'] = width
        self.meta['height'] = height
        self.width = width
        self.heigth = height
        self.frames = frames

    def write_diff(self, diff_bytes):
        item = {
            'size': len(diff_bytes),
            'data': diff_bytes,
        }
        self.diff.append(item)
        pass

    def write_vblock(self, vblock_json):
        self.vblock.append(vblock_json)
        pass

    def save(self, savepath):
        data = bytearray()

        # process meta
        for k, info in Davi.d.items():
            fmt, _, __ = info
            if fmt[-1] == 's':
                data += pack(fmt, self.meta[k].encode('ascii'))
            else:
                data += pack(fmt, self.meta[k])

        # process diff
        for o in self.diff:
            data += pack('I', o['size'])
            data += o['data']

        # process vblock
        for b in self.vblock:
            for pair in b:
                x, y = pair.values()
                data += pack('H', x)
                data += pack('H', y)

        # write out
        with open(savepath, 'wb') as f:
            f.write(data)
        pass
