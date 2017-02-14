import math
import pygame.gfxdraw
import Vector

def inCircle(pos, radius, p): #is point p=(x,y) within circle with r=radius(x,y) and position=pos
    r2 = radius*radius
    dist = ((pos[0]-p[0])**2 + (pos[1]-p[1])**2)
    if dist <= r2:
        return True
    return False

def inRect(r, p): #rectangle defined by four integers (x1,y1,x2,y2)
    if not p or not r:
        return False
    width = r[0][0] - r[1][0]
    height = r[0][1] - r[1][1]
    posx = r[1][0] + width
    posy = r[1][1] + height

    TLCorner = (r[0][0], r[0][1])
    BRCorner = (posx - width, posy - height)


    if p[0] > TLCorner[0] and p[0] < BRCorner[0] and p[1] > TLCorner[0] and p[1] < BRCorner[1]:
        return True
    return False

def aaLine(screen, X0, X1, thickness, color):
    X1 = (X1[0]-X0[1], X1[1]-X0[1])
    diff = ((X0[0]-X1[0]), (X0[1]-X1[1]))
    center = (diff[0]/2, diff[1]/2)
    length = math.sqrt(diff[0]**2 + diff[1]**2)
    angle = math.atan2(X0[1] - X1[1], X0[0] - X1[0])

    UL = (center[0] + (length / 2.) * math.cos(angle) - (thickness / 2.) * math.sin(angle),
      center[1] + (thickness / 2.) * math.cos(angle) + (length / 2.) * math.sin(angle))
    UR = (center[0] - (length / 2.) * math.cos(angle) - (thickness / 2.) * math.sin(angle),
          center[1] + (thickness / 2.) * math.cos(angle) - (length / 2.) * math.sin(angle))
    BL = (center[0] + (length / 2.) * math.cos(angle) + (thickness / 2.) * math.sin(angle),
          center[1] - (thickness / 2.) * math.cos(angle) + (length / 2.) * math.sin(angle))
    BR = (center[0] - (length / 2.) * math.cos(angle) + (thickness / 2.) * math.sin(angle),
          center[1] - (thickness / 2.) * math.cos(angle) - (length / 2.) * math.sin(angle))

    pygame.gfxdraw.aapolygon(screen, (UL, UR, BR, BL), color)
    pygame.gfxdraw.filled_polygon(screen, (UL, UR, BR, BL), color)


def distance(p1, p2):
    xdiff = p1[0] - p2[0]
    ydiff = p1[1] - p2[1]
    return math.sqrt(xdiff**2 + ydiff**2)

def slope(p1, p2):
    xdiff = p1[0] - p2[0]
    ydiff = p1[1] - p2[1]
    return ydiff/xdiff
