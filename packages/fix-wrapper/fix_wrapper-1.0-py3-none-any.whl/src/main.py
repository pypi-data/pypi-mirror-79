"""This file is main entrance of the project
    use argparse to get input arguments"""
import argparse
from wrapper import *


def parse_op(options):
    """"process argparse options"""
    file_path = os.path.abspath(options.file)
    if not os.path.isfile(file_path):
        print("Can't find file, please try again")
        sys.exit()
    out_dir = os.path.abspath(options.out_dir)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    wrap = Wrapper(file_path, out_dir)
    wrap.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True,
                        help="drag log file here/input file path")
    parser.add_argument("-o", "--out_dir", default="../output",
                        help="output dir")
    options = parser.parse_args()
    parse_op(options)
