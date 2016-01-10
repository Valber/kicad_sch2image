#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
simple story
"""
import sys
import getopt
import re
import cairo
import math
from kicad_sch2pic import draw_line, draw_comp, draw_field, draw_label


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
    # Рисуем страницу необязательно но на прозрачный альфа канал смотреть неудобно
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, page_width, page_height)
    ctx.fill()

    with open(start_path) as infile:
        ctx.set_source_rgb(0, float(143)/255, 0)
        ctx.set_line_width(8)
        t = False
        shet_t = False

        text_flag = False
        data_string = ""
        
        for line in infile:
            # Search and draw Wires
            if t:
                l = re.split("\s+", line)
                draw_line(ctx, int(l[1]), int(l[2]), int(l[3]), int(l[4]))
                ctx.stroke()
                t = False
            if re.match("Wire Wire Line", line):
                t = True

            # Draw Connection
            if re.match("Connection ~[\w\s\d]*", line):
                data = re.split("\s+", line)
                xc = int(data[-3])
                yc = int(data[-2])
                r = 20              # FIXME: Magic number
                ctx.move_to(xc, yc)
                ctx.arc(xc, yc, r, 0, 2*math.pi)
                ctx.fill()

            # Draw Text Labels GLabels HLabels Notes
            if text_flag:
                draw_label(ctx, line[:-1], data_string)
                text_flag = False
            if re.match("Text [\w\s\d]*", line):
                text_flag = True
                data_string = re.split("\s+", line)
                # Text GLabel 2750 750  0    60   Input ~ 0

            # Draw Sheet
            if shet_t:
                if re.match("S\s+[\d\w\s]*", line):
                    data = re.split("\s+", line)
                    print(data)
                    ctx.save()
                    ctx.set_source_rgb(float(147)/255, 0, float(147)/255)
                    x1 = int(data[1])
                    y1 = int(data[2])
                    x2 = int(data[3])
                    y2 = int(data[4])
                    ctx.rectangle(x1, y1, x2, y2)
                    ctx.stroke()
                    ctx.restore()
                    shet_t = False
            if re.match("\$Sheet", line):
                shet_t = True

    with open(start_path) as infile:
        ctx.set_line_width(12)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)  # TODO: Пунктир без закруглений
        ctx.set_source_rgb(float(150)/255, 0, 0)
        comp_t = False
        comp_matrix_disappear = True
        comp_name = ""
        comp_x = 0
        comp_y = 0
        field_pool = []
        comp_mtx = ['1', '0', '0', '-1']

        for line in infile:
            if comp_t:
                # Надобность двух нижних строчек вызывает сомнение
                if comp_matrix_disappear:
                    comp_mtx = ['1', '0', '0', '-1']
                if re.match("L\s+[\w\d]*\s+[\w\d\s]*", line):  # Search Search Comp
                    comp_name = re.split("\s+", line)[1]
                    # print(line)
                if re.match("P\s+[\w\d]*\s+[\w\d\s]*", line):  # Search Comp Position
                    comp_x = int(re.split("\s+", line)[1])
                    comp_y = int(re.split("\s+", line)[2])
                    # Get transformation matrix
                if re.match('\s+[-10]+\s+[-10]+\s+[-10]+\s+[-10]+\s+', line):
                    data = re.split("\s+", line)
                    # print("Transform matrix: %s" % str(data[1:-1]))
                    comp_mtx = data[1:-1]
                    comp_matrix_disappear = False
                if re.match("F\s+[\w\d\s]*", line):  # Draw Field
                    data = re.split("\s+", line)
                    field_pool.append(data)

            if re.match("\$Comp", line):
                comp_t = True
            # Search component
            if re.match("\$EndComp", line):  # Draw Comp
                comp_t = False
                draw_comp(ctx, library_component[comp_name], comp_mtx, comp_x, comp_y)
                for i in field_pool:
                    if i[2] != '""' and i[7] != '0001':
                        draw_field(ctx, i, comp_mtx, comp_x, comp_y)

                field_pool = []
                comp_name = ""
                comp_x = 0
                comp_y = 0


    # FIXME: Тест работы отрисовщика компонент
    # ctx.set_line_width(12)
    # ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    # ctx.set_source_rgb(float(150)/255, 0, 0)
    # draw_comp(ctx, library_component["M_CC"], 10200, 1000)
    # print(library_component["M_CC"])

    ctx.set_source_rgb(0, 1, 0)
    ctx.set_line_width(8)
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
