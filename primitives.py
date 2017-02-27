import pyglet
import math

def circle(x, y, resolution, radius, color, batch, group=None):
    interval = 2*math.pi/resolution
    points = []
    for i in range(resolution):
        angle = interval * i
        angle2 = interval * (i+1)
        points  += int(radius * math.cos(angle))+x, int(radius * math.sin(angle)) + y
        points += int(radius * math.cos(angle2))+x, int(radius * math.sin(angle2)) + y
        points += x, y

    return batch.add(len(points)//2, pyglet.gl.GL_TRIANGLES, group, ('v2i', points), ('c3B', (color*(len(points)//2))))

def line(x1, y1, x2, y2, color, batch, group=None):
    batch.add(2, pyglet.gl.GL_LINES, group, ('v2i', (x1, y1, x2, y2)), ('c3B', (color*(2))))

def rect(TLx, TLy, BRx, BRy, color, batch, group=None):
    batch.add(4, pyglet.gl.GL_QUADS, group, ('v2i', (TLx, TLy, TLx, BRy, BRx, BRy, BRx, TLy)), ('c4f', (color*(4))))
