#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
simple story
"""
import sys
import getopt
import re
import cairo
from kicad_sch2pic import draw_line, draw_comp


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
    page_height = 1000
    page_width = 1000
    print("Target : %s" % start_path)
    t = False
    with open(start_path) as infile:
        for line in infile:
            if re.match("EESchema Schematic File Version[\s\d\w]*", line):
                print(line)
            if re.match("EESchema Schematic File Version 2\s*", line):
                t = True
            if re.match("\$Descr\s+[\s\d\w]*", line):
                page = re.split("\s", line)
                page_width = int(page[2])
                page_height = int(page[3])
                print("Page format %s : %i x %i" % (page[1], page_width, page_height))
    if not t:
        print("Don't find correct EESchematic File Version")
        sys.exit(0)
    t = False
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
    t = False
    libcomp = ""
    namecomp = ""
    with open(lib_path) as infile:
        for line in infile:
            if re.match("ENDDEF", line):
                t = False
                library_component[namecomp] = libcomp
                libcomp = ""
            if re.match("DEF[\s\d\w]*", line):
                t = True
                namecomp = re.split("\s+", line)[1]
            if t:
                libcomp = libcomp + line

    print(library_component.keys())

    outfile = cairo.ImageSurface(cairo.FORMAT_ARGB32, page_width, page_height)
    ctx = cairo.Context(outfile)
    # Рисуем страницу
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, page_width, page_height)
    ctx.fill()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)  # TODO: Пунктир без закруглений

    with open(start_path) as infile:
        ctx.set_source_rgb(0, float(143)/255, 0)
        ctx.set_line_width(8)
        t = False
        for line in infile:
            # Search and draw Wires
            if t:
                l = re.split("\s+", line)
                draw_line(ctx, int(l[1]), int(l[2]), int(l[3]), int(l[4]))
                t = False
            if re.match("Wire Wire Line", line):
                t = True
        ctx.stroke()

    # with open(start_path) as infile:
    #     ctx.set_line_width(12)
    #     ctx.set_line_cap(cairo.LINE_CAP_ROUND)  # TODO: Пунктир без закруглений
    #     ctx.set_source_rgb(float(150)/255, 0, 0)
    #     comp_t = False
    #     comp_name = ""
    #     comp_x = 0
    #     comp_y = 0
    #     for line in infile:
    #         if comp_t:
    #             if re.match("L\s+[\w\d]*\s+[\w\d\s]*", line):
    #                 comp_name = re.split("\s+", line)[1]
    #                 print(comp_name)
    #             if re.match("P\s+[\w\d]*\s+[\w\d\s]*", line):
    #                 comp_x = int(re.split("\s+", line)[1])
    #                 comp_y = int(re.split("\s+", line)[2])
    #         if re.match("\$Comp", line):
    #             comp_t = True
    #         # Search component
    #         if re.match("\$EndComp", line):
    #             comp_t = False
    #             draw_comp(ctx, library_component[comp_name], comp_x, comp_y)
    #             comp_name = ""
    #             comp_x = 0
    #             comp_y = 0

    # FIXME: Тест работы отрисовщика компонент
    ctx.set_line_width(12)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(float(150)/255, 0, 0)
    draw_comp(ctx, library_component["M_CC"], 10200, 1000)
    print(library_component["M_CC"])

    ctx.set_source_rgb(0, 1, 0)
    ctx.set_line_width(8)
    draw_line(ctx, 2500, 1000, 2500, 5000)
    draw_line(ctx, 2500, 0, 2500, 4000)
    ctx.stroke()
    # ctx.set_source_rgb(0, 132/255, 132/255)
    # ctx.select_font_face("sans",
    #                      cairo.FONT_SLANT_NORMAL,
    #                      cairo.FONT_WEIGHT_NORMAL)
    # ctx.set_font_size(60)

    # ctx.move_to(500, 500)
    # ctx.show_text("ATU_Contact_Tr")

    outfile.write_to_png("example_sheet.png")

if __name__ == "__main__":
    main()
