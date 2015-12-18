#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
simple story
"""
import sys
import getopt


def main():
    start_path = "."
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:", ["help", "target"])
    except getopt.GetoptError as e:
        print(e.msg)
        sys.exit(1)
    for op, arg in opts:
        if op in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)

        if op in ("-t", "--target"):
            start_path = arg
    print("Main %s" % start_path)

    with open(start_path) as infile:
        for line in infile:
            print(line)


if __name__ == "__main__":
    main()
