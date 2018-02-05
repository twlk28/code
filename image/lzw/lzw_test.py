from lzw import *

if __name__ == '__main__':
    cmd1 = 'python3 lzw.py a.bmp'
    os.system(cmd1)
    cmd2 = 'python3 lzw.py a.lzw a.lzw.bmp'
    os.system(cmd2)
