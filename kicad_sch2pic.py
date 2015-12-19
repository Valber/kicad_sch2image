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


def cms(x, y, x0=0, y0=0):
    """Преобразование координат
    Внутри sch файла находится отрисовка в абсолютных координатах
    Внутри lib файла компоненты отрисовываются в относительных координатах
    """
    if (x0 != 0) or (y0 != 0):
        return ((x+x0), (-y+y0))
    else:
        return ((x+x0), (y+y0))


def draw_line(ctx, x1, y1, x2, y2, x0=0, y0=0):
    """Отрисовка линии
    draw_line(ctx, x1, y1, x2, y2, x0=0, y0=0)
    ctx - полотно cairo.Context
    x1, y1 координаты первой точки
    x0, y0 кординаты центра относительной системы координат
    """
    x, y = cms(x1, y1, x0, y0)
    ctx.move_to(x, y)
    x, y = cms(x2, y2, x0, y0)
    ctx.line_to(x, y)
    return


def draw_pin(ctx, x, y, length, orient, x0=0, y0=0):
    """Отрисовка вывода компнента
    """
    if orient == 'L':
        xe = x - length
        ye = y
    else:
        xe = x + length
        ye = y
    draw_line(ctx, x, y, xe, ye, x0, y0)
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
    """
    x, y = cms(xc, yc, x0, y0)
    s0 = math.pi/1800 * (start_angle) + math.pi/2
    e0 = math.pi/1800 * (stop_angle) + math.pi/2
    xs = x + r*math.cos(s0)
    ys = y + r*math.sin(s0)
    ctx.move_to(xs, ys)
    ctx.arc(x, y, r, s0, e0)


def draw_comp(ctx, text, x0=0, y0=0):
    """Draw Component from lib
    Хорошо что позиции текста указываются в sch в
    абсолютных координатах
    """
    # ctx.save()
    # ctx.set_line_width(12)
    # ctx.set_line_cap(cairo.LINE_CAP_ROUND)  # TODO: Пунктир без закруглений
    # ctx.set_source_rgb(float(150)/255, 0, 0)

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
            x, y = cms(x1, y1, x0, y0)
            ctx.move_to(x, y)
            for i in range(int(data[1])-1):
                num = (i+1)*2+5
                x2 = int(data[num])
                y2 = int(data[num+1])
                x, y = cms(x2, y2, x0, y0)
                ctx.line_to(x, y)
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
            draw_pin(ctx, x, y, length, symbol, x0, y0)
            # TODO: Draw pin ma,e and number
            ctx.stroke()
        if re.match("C\s+[\w\d]*\s+[\w\d\s]*", line):
            data = re.split("\s+", line)

            xc = int(data[1])
            yc = int(data[2])
            r = int(data[3])
            x, y = cms(xc, yc, x0, y0)
            ctx.move_to(x + r*math.cos(0), y + r*math.sin(0))
            ctx.arc(x, y, r, 0, 2*math.pi)
            if data[-1] == 'F':
                ctx.fill()
            else:
                ctx.stroke()

        if re.match("S\s+[\w\d\s]*", line):
            data = re.split("\s+", line)
            x1, y1 = cms(int(data[1]), int(data[2]), x0, y0)
            x2, y2 = cms(int(data[3]), int(data[4]), x0, y0)
            # Rectangle(x1,y2 point, xlength, ylength)
            ctx.rectangle(x1, y1, x2-x1, y2-y1)
            if data[-1] == 'F':
                ctx.fill()
            else:
                ctx.stroke()

    #ctx.restore()


# svg = cairo.SVGSurface("example2.svg", WIDTH, HEIGHT)
# ctx = cairo.Context(svg)

# ctx.set_line_width(8)
# ctx.set_line_cap(cairo.LINE_CAP_ROUND)  # TODO: Пунктир без закруглений
# ctx.set_source_rgb(150/255, 0, 0)

# draw_line(ctx, -150, -100, 150, 0)
# draw_line(ctx, -150, -25, -150, 0)
# draw_line(ctx, 0, -140,  0, -150)
# draw_line(ctx, 0, -130,  0, -110)
# draw_line(ctx, 0, -100,  0, -80)
# draw_line(ctx, 0, -70,  0, -50)
# draw_line(ctx, 50, -150,  -50, -150)

# draw_pin(ctx, -450, 0, 300, 'R')
# draw_pin(ctx, 450, 0, 300, 'L')

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


# x, y = cms(500/2, -100)
# ctx.move_to(x, y)
# ctx.show_text("ATU_Contact_Tr")

# x, y = cms(-370, -100)
# ctx.move_to(x, y)
# ctx.show_text("K")



# svg.finish()
