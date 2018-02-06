import os

if __name__ == '__main__':
    cmd1 = 'python3 lzw.py assets/a.bmp'
    os.system(cmd1)
    cmd2 = 'python3 lzw.py assets/a.lzw assets/a.lzw.bmp'
    os.system(cmd2)
