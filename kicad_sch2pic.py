#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Draw simple
#
# ATU_Contact_Tr
#
DEF ATU_Contact_Tr K 0 40 Y Y 1 F N
F0 "K" -370 -120 60 H V C CNN
F1 "ATU_Contact_Tr" 500 -100 60 H V C CNN
F2 "" 0 0 60 H V C CNN
F3 "" 0 0 60 H V C CNN
DRAW
A 0 -150 50 -1799 -1 0 1 0 N -50 -150 50 -150
P 3 0 1 0  -150 -100  150 0  150 0 N
P 3 0 1 0  -150 -25  -150 0  -150 0 N
P 3 0 1 5  0 -140  0 -150  0 -150 N
P 3 0 1 5  0 -130  0 -110  0 -110 N
P 3 0 1 5  0 -100  0 -80  0 -80 N
P 3 0 1 5  0 -70  0 -50  0 -50 N
P 4 0 1 0  50 -150  -50 -150  -50 -150  -50 -150 N
X ~ 1 -450 0 300 R 50 50 1 1 P
X ~ 2 450 0 300 L 50 50 1 1 P
ENDDRAW
ENDDEF
"""
import math
import cairo
import re

WIDTH, HEIGHT = 2000, 1000
svg = cairo.SVGSurface("example2.svg", WIDTH, HEIGHT)
ctx = cairo.Context(svg)


def draw_line(ctx, x1, y1, x2, y2, x0=0, y0=0):
    """Отрисовка линии компонента
    draw_line(ctx, x1, y1, x2, y2, x0=0, y0=0)
    ctx - полотно cairo.Context
    x1, y1 координаты первой точки
    x0, y0 кординаты центра относительной системы координат
    """
    mtx = ctx.get_matrix()
    ctx.translate(x0, y0)
    if (x0 != 0) or (y0 != 0):
        ctx.scale(1, -1)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.set_matrix(mtx)
    return


def draw_pin(ctx, x, y, length, orient, font_data, x0=0, y0=0):
    """Отрисовка вывода компнента
    """
    lab = font_data[0]
    num = font_data[1]
    lab_size = font_data[2]
    num_size = font_data[3]

    if orient == 'R' or orient == 'U':
        x_lab = length
        y_lab = 0.0
        x_num = 0.0 + length/2
        y_num = 0.0
    else:                      # L and D
        length = -length
        x_lab = length
        y_lab = 0.0
        x_num = 0.0 + length/2
        y_num = 0.0
    # TODO: доделать поддержку верт пинов
    mtx = ctx.get_matrix()
    ctx.translate(x, y)
    if orient == 'U':
        ctx.rotate(math.pi/2)
    if orient == 'D':
        ctx.rotate(math.pi/2)

    ctx.move_to(0, 0)
    ctx.line_to(length, 0)
    ctx.stroke()
    fnt_clr = ctx.get_font_options()
    fnt_mtx = ctx.get_font_matrix()
    clr_mtx = ctx.get_source()
    ctx.select_font_face("sans",
                         cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_NORMAL)
    ctx.scale(1, -1)            # Оставить здесь
    if num != '~':
        ctx.set_font_size(num_size)
        sz = ctx.text_extents(num)  # Text Rectangle
        # dif = (sz[1] + sz[3])
        ctx.move_to(x_num - sz[2]/2, y_num - abs(sz[1]))
        ctx.show_text(num)
    if lab != '~' and font_data[4]:
        ctx.set_source_rgb(0, 132/float(255), 132/float(255))
        ctx.set_font_size(lab_size)
        sz = ctx.text_extents(lab)  # Text Rectangle
        if orient == 'R' or orient == 'U':
            ctx.move_to(x_lab + sz[2]*0.4, y_lab + abs(sz[3])/2)
        else:
            ctx.move_to(x_lab - sz[2]*1.4, y_lab + abs(sz[3])/2)
        ctx.show_text(lab)
        ctx.set_font_matrix(fnt_mtx)
        ctx.set_font_options(fnt_clr)
        ctx.set_source(clr_mtx)

    ctx.set_matrix(mtx)
    return


def draw_arc(ctx, xc, yc, r, start_angle, stop_angle, x0=0, y0=0):
    """Рисуем арку
    draw_arc(ctx, xc, yc, r, start_angle, stop_angle, sx, sy, x0=0, y0=0)
    xc,yc - координаты центра арки
    r - радиус
    start_angle - стартовый угл(0 на трех часах + против часовой)
    В кисад углы заданы в 0,1 градуса т.е. 1800 - это pi
    sx,sy - FIXME:  альтернативное задание арки
    x0,y0 - центр относительной системы координат

    Нарисовать арку по двум углам можнодвумя способами
    в KiCAD это неопределенность разрешена тем что арку больше 180 не нарисуеш
    в Cairo тем что арка ВСЕГДА рисуется по часовой
    """
    mtx = ctx.get_matrix()
    ctx.translate(xc, yc)
    ctx.scale(1, -1)
    str_a = -start_angle/float(10)
    stp_a = -stop_angle/float(10)
    if (abs(str_a - stp_a) > 180) or (str_a > stp_a):
        str_a, stp_a = stp_a, str_a
    s0 = math.pi/180 * str_a
    e0 = math.pi/180 * stp_a
    xs = r*math.cos(s0)
    ys = r*math.sin(s0)
    ctx.move_to(xs, ys)
    ctx.arc(0, 0, r, s0, e0)
    ctx.set_matrix(mtx)


def draw_comp(ctx, text, component_matrix, x0=0, y0=0):
    """Draw Component from lib
    Хорошо что позиции текста указываются в sch в
    абсолютных координатах
    """
    # ctx.save()
    # ctx.set_line_width(12)
    # ctx.set_line_cap(cairo.LINE_CAP_ROUND)  # TODO: Пунктир без закруглений
    # ctx.set_source_rgb(float(150)/255, 0, 0)
    mtx = ctx.get_matrix()
    ctx.translate(x0, y0)
    ctx.scale(1, -1)
    label_flag = True
    for line in re.split('\n', text):
        if re.match("DEF\s+[\w\d]*\s+[\w\d\s]*", line):
            data = re.split("\s+", line)
            if data[-4] == 'N':  # Invisible pin label
                label_flag = False

    for line in re.split('\n', text):
        if re.match("A\s+[\w\d]*\s+[\w\d\s]*", line):
            data = re.split("\s+", line)
            xc = int(data[1])
            yc = int(data[2])
            r = int(data[3])
            draw_arc(ctx, xc, yc, r, int(data[4]), int(data[5]), x0, y0)
            if data[-5] == 'F':
                ctx.fill()
            else:
                ctx.stroke()
        if re.match("P\s+[\w\d]*\s+[\w\d\s]*", line):
            data = re.split("\s+", line)
            x1 = int(data[5])
            y1 = int(data[6])
            ctx.move_to(x1, y1)
            for i in range(int(data[1])-1):
                num = (i+1)*2+5
                x2 = int(data[num])
                y2 = int(data[num+1])
                ctx.line_to(x2, y2)
            # TODO: Thickness option
            if data[-1] == 'F':
                ctx.fill()
            else:
                ctx.stroke()

        if re.match("X\s+[\w\d\s]*", line):
            data = re.split("\s+", line)
            x = int(data[3])
            y = int(data[4])
            length = int(data[5])
            symbol = data[6]
            textdata = [data[1], data[2], int(data[8]), int(data[7]), label_flag]
            if data[-2] != 'W':  # Invisible pin
                draw_pin(ctx, x, y, length, symbol, textdata)
            # print("Textdata: %s" % str(textdata))
            # TODO: Draw pin ma,e and number
        if re.match("C\s+[\w\d]*\s+[\w\d\s]*", line):
            data = re.split("\s+", line)

            xc = int(data[1])
            yc = int(data[2])
            r = int(data[3])
            ctx.move_to(xc + r*math.cos(0), yc + r*math.sin(0))
            ctx.arc(xc, yc, r, 0, 2*math.pi)
            if data[-1] == 'F':
                ctx.fill()
            else:
                ctx.stroke()

        if re.match("S\s+[\w\d\s]*", line):
            data = re.split("\s+", line)
            x1 = int(data[1])
            y1 = int(data[2])
            x2 = int(data[3])
            y2 = int(data[4])
            # Rectangle(x1,y2 point, xlength, ylength)
            ctx.rectangle(x1, y1, x2-x1, y2-y1)
            if data[-1] == 'F':
                ctx.fill()
            else:
                ctx.stroke()

    ctx.set_matrix(mtx)

# svg = cairo.SVGSurface("example2.svg", WIDTH, HEIGHT)
# ctx = cairo.Context(svg)

# ctx.set_line_width(8)
# ctx.set_line_cap(cairo.LINE_CAP_ROUND)  # TODO: Пунктир без закруглений
# ctx.set_source_rgb(150/255, 0, 0)

# # Придумавшего этот формат надо посадить на кол
# # A 0 -150 50 -1799 -1 0 1 0 N -50 -150 50 -150
# draw_arc(ctx, 0, -150, 50, 0, -2, 0, 0)

# # Применение покраски на только что отрисованные детали
# # ctx.set_source_rgb(0.5, 0.0, 0.5)  # Solid color
# ctx.stroke()

# ctx.set_source_rgb(0, 132/255, 132/255)
# ctx.select_font_face("sans",
#                      cairo.FONT_SLANT_NORMAL,
#                      cairo.FONT_WEIGHT_NORMAL)
# ctx.set_font_size(60)
# svg.finish()
