#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
simple story
"""
import sys
import getopt
import re


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
    # FIXME: Для теста поместим сюда жесткую ссылку
    start_path = "/home/valber/forge/unitbiotech/grow2_0.sch"
    lib_path = start_path[:-4]+"-cache.lib"
    print("Target : %s" % start_path)
    t = False
    with open(start_path) as infile:
        for line in infile:
            if re.match("EESchema Schematic File Version[\s\d\w]*", line):
                print(line)
            if re.match("EESchema Schematic File Version 2\s*", line):
                t = True

    if not t:
        print("Don't find correct EESchematic File Version")
        sys.exit(0)

    with open(lib_path) as infile:
        for line in infile:
            if re.match("EESchema-LIBRARY Version 2[\s\d\w]*", line):
                print(line)
            if re.match("EESchema-LIBRARY Version 2.3\s*", line):
                t = True
            if re.match("EESchema-LIBRARY Version 2.2\s*", line):
                t = True
            # FIXME: Хреново нужно умнее вычленять версию. С учетом
            # того что в некоторых версиях они после версии дату пишут.

    library_component = {}      # название : текст компонента

if __name__ == "__main__":
    main()
