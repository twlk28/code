import matplotlib.pyplot as plot
import numpy as np
from PIL import Image


def grayimage(path):
    # convert('L') 转为灰度图
    # 这样每个像素点就只有一个灰度数据
    img = Image.open(path).convert('L')
    return img


def image_fft(image):
    # 对图像做二维 fft
    a = np.fft.fft2(image)
    return a


def decompress_image(data):
    # 做一个逆 fft2 还原数据
    img = np.fft.ifft2(data)
    return img


def save_image(data, path):
    # 把图片还原并保存到文件中
    # fft 变换的结果是一个 [复数]
    # np.uint8 转换的时候，只会转换复数的实部，丢弃复数的虚部
    img = Image.fromarray(np.uint8(data))
    img.save(path)


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
    matrix = np.zeros_like(data)
    w2 = 512 / 2
    r = w2 * (1 - ratio)
    for i, row in enumerate(data):
        for j, n in enumerate(row):
            if (abs(i - w2) < r) or (abs(j - w2) < r):
                matrix[i, j] = 0
            else:
                matrix[i, j] = n
    return matrix


def preview(data):
    """
    调用 matplotlib 把图像画出来预览
    """
    m, n = 3, 3
    for i in range(m * n):
        # 从 1 到 9 选择画在第 n 个子图
        plot.subplot(m, n, i + 1)
        # 这里可以设置不同的过滤等级（压缩等级）
        ratio = (i + 1) / 10
        img = filter_image(data, ratio)
        b = decompress_image(img)
        plot_data = np.uint8(b)
        # 画图
        plot.imshow(plot_data, cmap=plot.cm.gray)
        plot.grid(False)
        plot.xticks([])
        plot.yticks([])
    # show 是让图像窗口持续停留
    plot.show()


def main():
    ipath = 'lena.png'
    opath = 'lena2.png'
    img = grayimage(ipath)
    data = image_fft(img)
    data_lossy = filter_image(data, 0.2)
    img_lossy = decompress_image(data_lossy)
    save_image(img_lossy, opath)
    #
    preview(data)
    pass


if __name__ == '__main__':
    main()
