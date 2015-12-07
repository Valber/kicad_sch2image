#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import cairo

WIDTH, HEIGHT = 1000, 1000


def cms(x, y):
    return ((x+float(WIDTH)/2)/WIDTH, (-y+float(HEIGHT)/2)/HEIGHT)


def draw_line(ctx, x1, y1, x2, y2):
    x, y = cms(x1, y1)
    ctx.move_to(x, y)
    x, y = cms(x2, y2)
    ctx.line_to(x, y)
    return


def draw_point(ctx, x0, y0):
    draw_line(ctx, x0-10, y0, x0+10, y0)
    draw_line(ctx, x0, y0-10, x0, y0+10)
    return


def draw_arc(ctx, x0, y0, r, start_angle, stop_angle, sx, sy):
    maxlen = max(float(WIDTH), float(HEIGHT))
    x, y = cms(x0, y0)
    r0 = r/maxlen
    s0 = math.pi/2 * (start_angle)
    e0 = math.pi/2 * (stop_angle)
    print(s0, e0)
    sx = x0 + r*math.cos(s0)
    sy = y0 + r*math.sin(s0)
    xs, ys = cms(sx, sy)    
    ctx.move_to(xs, ys)
    ctx.arc(x, y, r0, s0, e0)


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


surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)


ctx.scale(WIDTH, HEIGHT)        # Normalizing the canvas


# pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
# pat.add_color_stop_rgba(1, 0.7, 0, 0, 0.5) # First stop, 50% opacity
# pat.add_color_stop_rgba(0, 0.9, 0.7, 0.2, 1) # Last stop, 100% opacity

# ctx.rectangle(0, 0, 1, 1)      # Rectangle(x0, y0, x1, y1)
# # ctx.set_source (pat)
# # ctx.fill ()

# ctx.translate(0.1, 0.1)  # Changing the current transformation matrix

# ctx.move_to(0, 0)
# ctx.arc(0.2, 0.1, 0.1, -math.pi/2, 0)  # Arc(cx, cy, radius, start_angle, stop_angle)
# ctx.line_to(0.5, 0.1)                  # Line to (x,y)
# ctx.curve_to(0.5, 0.2, 0.5, 0.4, 0.2, 0.8)  # Curve(x1, y1, x2, y2, x3, y3)
# ctx.close_path()


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

# draw_arc(ctx, -150, 50, 50, 0, 1)
# ctx.move_to(0.75, 0.5)
# ctx.arc(0.5, 0.5, 0.25, 0, math.pi/2)

# ctx.scale(WIDTH, HEIGHT)



ctx.set_source_rgb(0.3, 0.2, 0.5)  # Solid color
ctx.set_line_width(0.02)
ctx.stroke()

# draw_point(ctx, -50, -150)
# draw_point(ctx, 0,-150)

#draw_arc(ctx, 0, -150, 50, 0, 0.5)


# Применение покраски на только что отрисованные детали
ctx.set_source_rgb(0.5, 0.0, 0.5)  # Solid color
ctx.set_line_width(0.02)
ctx.stroke()

surface.write_to_png("example.png")  # Output to PNG
# Draw simple
# A 0 -150 50 -1799 -1 0 1 0 N -50 -150 50 -150
# P 3 0 1 0  -150 -100  150 0  150 0 N
# P 3 0 1 0  -150 -25  -150 0  -150 0 N
# P 3 0 1 5  0 -140  0 -150  0 -150 N
# P 3 0 1 5  0 -130  0 -110  0 -110 N
# P 3 0 1 5  0 -100  0 -80  0 -80 N
# P 3 0 1 5  0 -70  0 -50  0 -50 N
# P 4 0 1 0  50 -150  -50 -150  -50 -150  -50 -150 N
# X ~ 1 -450 0 300 R 50 50 1 1 P
# X ~ 2 450 0 300 L 50 50 1 1 P
