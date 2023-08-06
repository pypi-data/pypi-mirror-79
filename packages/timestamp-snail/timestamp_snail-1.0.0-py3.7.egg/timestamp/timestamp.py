import time
import datetime
import argparse
import sys


def strftime(timestamp, format_string='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format_string, time.localtime(timestamp))


# 解析命令行参数
def get_argparse():
    parser = argparse.ArgumentParser(description='convert timestamp into time')
    parser.add_argument('v', help='timestamp', type=int)
    
    return parser.parse_args()


def main():
    parser = get_argparse()
    _timestamp = parser.v
    if _timestamp:
        print(f'当前时间是: {strftime(_timestamp)}')
    

if __name__ == "__main__":
    main()
    