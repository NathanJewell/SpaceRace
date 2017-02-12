# drawshapes.py
# written by Jeffrey Kleykamp

import math
import pygame

TAU = 2 * math.pi

def getpolygon(origin, radius, N, start=0, end=None):
    out = []
    x, y = origin
    Nf = float(N)
    if end is None:
        end = TAU
    for i in range(N):
        xp = x + radius * math.sin(end * i / Nf + start)
        yp = y - radius * math.cos(end * i / Nf + start)
        out.append((xp, yp))
    return out

def regpolygon(surf, color, origin, radius, width, N, start=0):
    if width == 0 or width >= radius:
        pl = getpolygon(origin, radius, N)
        r = pygame.draw.polygon(surf, color, pl)
        return r
    else:
        end = TAU * (N+1) / float(N)
        p1 = getpolygon(origin, radius, N+1, start=start, end=end)
        p2 = getpolygon(origin, radius-width, N+1, start=start, end=end)
        p2.reverse()
        p1.extend(p2)
        r = pygame.draw.polygon(surf, color, p1)
        return r

def circle(surf, color, origin, radius, width=0, N=64):
    regpolygon(surf, color, origin, radius, width, N, 0)

def arc(surf, color, origin, radius, start=0, end=None, width=0, N=64):
    if width == 0 or width >= radius * 0.5:
        p2 = [origin]
    else:
        p2 = getpolygon(origin, radius-width, N, start=start, end=end)
        p2.reverse()
    p1 = getpolygon(origin, radius, N, start=start, end=end)
    p1.extend(p2)
    r = pygame.draw.polygon(surf, color, p1)
    return r

def wedge(surf, color, origin, radius, start=0, end=None, width=0, N=64):
    if width == 0 or width >= radius * 0.5:
        return arc(surf, color, origin, radius, start=start, end=end, width=0, N=N)
    # does outside polygon
    p1 = [origin]
    p2 = getpolygon(origin, radius, N, start=start, end=end)
    p3 = [origin]
    p1.extend(p2)
    p1.extend(p3)

    # does inside polygon
    x, y = origin
    xp = x + width * math.sin(end * 0.5 + start)
    yp = y - width * math.cos(end * 0.5 + start)
    norigin = (xp,yp)
    p3 = [norigin]
    p2 = getpolygon(norigin, radius-2*width, N, start=start, end=end)
    p2.reverse()
    p1.extend(p3)
    p1.extend(p2)
    p1.extend(p3)

    # draws the full polygon
    r = pygame.draw.polygon(surf, color, p1)
    return r

def ellipse(surf, color, rect, width=0, N=64):
    # draws an ellipse that bounds the rect
    xradius = rect.width * 0.5
    yradius = rect.height * 0.5
    origin = rect.center

    return ellipse_radius(surf, color, origin, xradius, yradius, width=width, N=N)


def ellipse_radius(surf, color, origin, xradius, yradius, width=0, N=64):
    # draws an ellipse that has the two radii
    pl = []
    x, y = origin
    if width >= min(xradius, yradius):
        width = 0
    if width is 0:
        end = TAU
    else:
        end = TAU * (N+1) / float(N)
        N = N+1
    Nf = float(N)

    for i in range(N):
        xp = x + xradius * math.sin(end * i / Nf)
        yp = y - yradius * math.cos(end * i / Nf)
        pl.append((xp, yp))

    if width is not 0:
        xradius -= width
        yradius -= width
        for i in range(N):
            xp = x + xradius * math.sin(-end * i / Nf)
            yp = y - yradius * math.cos(-end * i / Nf)
            pl.append((xp, yp))

    r = pygame.draw.polygon(surf, color, pl)
    return r

if __name__ == '__main__':
    # test code
    import os

    # this code trys to incorporate aa lines but it's not as good as polygon alone
    # because it doesn't fill in the polygon. So I tried doing both...
    old = pygame.draw.polygon
    def idk(s,c,pl):
        pygame.draw.aalines(s,c,True,pl,False)
        old(s,c,pl)

    def switchxray():
        pygame.draw.polygon = lambda s,c,pl: pygame.draw.aalines(s,c,True,pl,False)
    def switchfull():
        pygame.draw.polygon = idk
    def switchori():
        pygame.draw.polygon = old
    def draw_3modes(i, j,dx,f):
        pos = (dx*i, j*dx)
        f(pos)
        i += 2
        switchfull()
        pos = (dx*i, j*dx)
        f(pos)
        i += 2
        switchxray()
        pos = (dx*i, j*dx)
        f(pos)
        i += 2
        switchori()


    def test():
        print("The first col uses the current draw function")
        print("The next col uses polygons")
        print("The next col uses polygons + aalines")
        print("The next col uses aalines only")
        print("Ideally aalines should fill leading to smooth shapes")
        input("Press enter to continue")

        width = 800
        height = 600
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        screen = pygame.display.set_mode((width,height))
        c = pygame.color.Color("blueviolet")
        radius = 75
        width = 25
        dx = radius + 10
        r = pygame.Rect(0,0,2*radius,2*radius)

        # draws a bunch of circles
        pygame.draw.circle(screen, c, (dx, dx), radius, width)
        f = lambda p: circle(screen, c, p, radius+20, width)
        draw_3modes(3,1,dx,f)

        # draws a bunch of arcs
        r.center = (dx, 3*dx)
        pygame.draw.arc(screen, c, r, math.pi/2, 3, width)
        f = lambda p: arc(screen, c, p, radius, 0, math.pi/2-3, width)
        draw_3modes(3,3,dx,f)

        # draws a bunch of circles nearly filled in
        pygame.draw.circle(screen, c, (dx, 4*dx), radius, radius - 5)
        f = lambda p: circle(screen, c, p, radius, radius - 5)
        draw_3modes(3,4,dx,f)

        # draws a bunch of ellipses
        r = pygame.Rect(0,0,1.5*radius,2*radius)
        r.center = (dx, 6*dx)
        pygame.draw.ellipse(screen, c, r, width)
        f = lambda p: ellipse_radius(screen, c, p, 3*radius/4.0, radius, width)
        draw_3modes(3,6,dx,f)

        pygame.display.flip()

        while True:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return
    test()
