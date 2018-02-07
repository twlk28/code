import matplotlib.pyplot as plot
import numpy as np
from PIL import Image


def image_fft(image):
    # 对图像做二维 fft
    a = np.fft.fft2(image)
    return a


def decompress_image(data):
    # 做一个逆 fft2 还原数据
    img = np.fft.ifft2(data)
    return img


def filter_image(data, ratio=1):
    """
    ratio 是压缩率, 范围是 0 - 1
    1 表示完全不压缩

    本函数会对 fft 变换后的数据进行过滤
    经过二维 fft 变换后，得到的数据是一个系数矩阵
    其中，高频数据在中心, 低频在四个角
    高频数据可以丢弃（设置为 0 就算是丢弃了）
    """

    # 造一个空数组并复制数据
    w2 = len(data) / 2
    r = w2 * (1 - ratio)
    matrix = np.zeros_like(data)
    for i, row in enumerate(data):
        for j, n in enumerate(row):
            if (abs(i - w2) < r) or (abs(j - w2) < r):
                matrix[i, j] = 0
            else:
                matrix[i, j] = n
    return matrix


def thunkify(img, thunk_size=8):
    s, w, h = [], img.width, img.height
    x, y = 0, 0
    while y < h:
        x = 0
        while x < w:
            rect = (x, y, x + thunk_size, y + thunk_size)
            image = img.crop(rect)
            s.append((rect, image))
            x += thunk_size
        y += thunk_size
    return s


def compose_thunks(thunks, width, height):
    img_empty = Image.new('RGB', (width, height))
    for rect, image in thunks:
        img_empty.paste(image, rect)
    return img_empty


def compress_thunk(img, ratio=1):
    # 对图片每个通道应用fft转换
    r1, g1, b1 = img.split()
    channels = []
    for i, data in enumerate([r1, g1, b1]):
        a = image_fft(data)
        b = filter_image(a, ratio)
        c = decompress_image(b)
        d = Image.fromarray(np.uint8(c))
        channels.append(d)
    img2 = Image.merge('RGB', channels)
    return img2


def compress_image(img, ratio=1):
    # 图像进行 8x8 分块
    thunks = thunkify(img, thunk_size=8)
    # 对每个分块图片压缩
    thunks_lossy = [(rect, compress_thunk(image, ratio)) for rect, image in thunks]
    # 压缩后的分块合成大图
    img_lossy = compose_thunks(thunks_lossy, img.width, img.height)
    return img_lossy


def preview(img):
    m, n = 3, 3
    for i in range(m * n):
        plot.subplot(m, n, i + 1)
        ratio = (i + 1) / 9
        img_lossy = compress_image(img, ratio)
        plot.imshow(img_lossy)
        plot.grid(False)
        plot.xticks([])
        plot.yticks([])
    plot.show()


def main():
    ipath = 'lena.png'
    opath = 'lena2.png'
    image = Image.open(ipath)
    image_lossy = compress_image(image, 0.2)
    image_lossy.save(opath)
    #
    preview(image)
    pass


if __name__ == '__main__':
    main()
