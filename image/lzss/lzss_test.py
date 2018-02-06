import os

if __name__ == '__main__':
    cmd1 = 'python3 lzss.py assets/a.bmp'
    os.system(cmd1)
    cmd2 = 'python3 lzss.py assets/a.lzss assets/a.lzss.bmp'
    os.system(cmd2)