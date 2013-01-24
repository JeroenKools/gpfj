'''
Created on 24 jan. 2013

@author: Junuxx
'''

import math
import random
import colorsys

def gradient(startHue, endHue, startSaturation, endSaturation, steps):
    hstepsize = (endHue - startHue) / (steps - 1)
    sstepsize = (float(endSaturation) - startSaturation) / (steps - 1)
    hue = [startHue + i * hstepsize for i in range(steps + 1)]
    saturation = [startSaturation + i * sstepsize for i in range(steps + 1)]
    colors = [colorsys.hsv_to_rgb(h, s, 1) for (h, s) in zip(hue, saturation)]
    colors = ["#%02x%02x%02x" % (int(255 * c[0]), int(255 * c[1]), int(255 * c[2])) for c in colors]
    return colors

def star(x, y, innerRadius, outerRadius, th0=0, arms=5, noise=0):
    coords = []
    noise = max(0, noise)
    N = lambda x = 0: random.randint(-noise, noise)

    for i in range(arms):
        th1 = 2.*math.pi * i / arms + th0
        th2 = 2.*math.pi * (i + .5) / arms + th0

        coords += [x + math.sin(th1) * innerRadius + N(),
                   y + math.cos(th1) * innerRadius + N(),
                   x + math.sin(th2) * outerRadius + N(),
                   y + math.cos(th2) * outerRadius + N()]
    return coords

def kaboom(x, y, levels, canvas, root):
    """Paints an animated explosion on a tkinter canvas"""
    colors = gradient(0, 1. / 7, 1, 1, 5)
    basename = random.randint(0, 1000000)
    th0 = math.pi * random.random()

    for i in range(levels):
        coords = star(x, y, 15 - 2 * i, 30 - i * 2, th0, 7, 6 - i)
        name = "star%i_part%i" % (basename, i)
        canvas.create_polygon(coords, outline=None, fill=colors[i], state="hidden", tags=name)

    reveal(basename, levels - 1, canvas, root)

def reveal(basename, i, canvas, root):
    if i >= 0:
        canvas.itemconfig("star%i_part%i" % (basename, i), state="normal")
        root.after(40, lambda: reveal(basename, i - 1, canvas, root))
    else:
        hide(basename, i, canvas, root)

def hide(basename, i, canvas, root):
    if i < 5:
        canvas.delete("star%i_part%i" % (basename, i))
        root.after(60, lambda: hide(basename, i + 1, canvas, root))