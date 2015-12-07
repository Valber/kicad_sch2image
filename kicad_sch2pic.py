#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Draw simple
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
"""
import math
import cairo

WIDTH, HEIGHT = 1000, 1000


def cms(x, y):
    return ((x+float(WIDTH)/2), (-y+float(HEIGHT)/2))


def draw_line(ctx, x1, y1, x2, y2):
    x, y = cms(x1, y1)
    ctx.move_to(x, y)
    x, y = cms(x2, y2)
    ctx.line_to(x, y)
    return


def draw_pin(ctx, x, y, length, orient):
    # maxlen = max(float(WIDTH), float(HEIGHT))
    if orient == 'L':
        xe = x - length
        ye = y
    else:
        xe = x + length
        ye = y
    draw_line(ctx, x, y, xe, ye)
    return


def draw_point(ctx, x0, y0):
    draw_line(ctx, x0-10, y0, x0+10, y0)
    draw_line(ctx, x0, y0-10, x0, y0+10)
    return


def draw_arc(ctx, x0, y0, r, start_angle, stop_angle, sx, sy):
    x, y = cms(x0, y0)
    s0 = math.pi/2 * (start_angle)
    e0 = math.pi/2 * (stop_angle)
    print(s0, e0)
    sx = x0 + r*math.cos(s0)
    sy = y0 + r*math.sin(s0)
    xs, ys = cms(sx, sy)
    ctx.move_to(xs, ys)
    ctx.arc(x, y, r, s0, e0)


svg = cairo.SVGSurface("example2.svg", WIDTH, HEIGHT)
ctx = cairo.Context(svg)

ctx.set_line_width(10)
ctx.set_source_rgb(150/255, 0, 0)

draw_line(ctx, -150, -100, 150, 0)
draw_line(ctx, -150, -25, -150, 0)
draw_line(ctx, 0, -140,  0, -150)
draw_line(ctx, 0, -130,  0, -110)
draw_line(ctx, 0, -100,  0, -80)
draw_line(ctx, 0, -70,  0, -50)
draw_line(ctx, 50, -150,  -50, -150)

draw_pin(ctx, -450, 0, 300, 'R')
draw_pin(ctx, 450, 0, 300, 'L')

# Придумавшего этот формат надо посадить на кол
# A 0 -150 50 -1799 -1 0 1 0 N -50 -150 50 -150
draw_arc(ctx, 0, -150, 50, 0, -2, 0, 0)

# Применение покраски на только что отрисованные детали
# ctx.set_source_rgb(0.5, 0.0, 0.5)  # Solid color
ctx.stroke()

svg.finish()
