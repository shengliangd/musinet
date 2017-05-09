#!/usr/bin/python3

from sys import argv
from .xmlpkl import xml2pkl

if __name__ == '__main__':
    if len(argv) != 3:
        print("Usage: %s infile outfile" % argv[0])
        exit(-1)
    xml2pkl(argv[1], argv[2])
