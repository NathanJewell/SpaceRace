#external dependencies
import pygame
from pygame.locals import *
from pygame import gfxdraw
import math
import time
import drawshapes as goodgfx
import gameUtils as utils
import random

#internal dependencies
from Station import *
from Player import *


class MapHandler:

    def __init__(self):
        generateMap = False
        self.lastelapsed = 0
        self.objects = []
        self.players = []
        self.dt = 1000	#units generate every one second

        #setting up system
        self.players.append(Player((128,128,128), (255, 0, 0), "neutral"))
        self.players.append(Player((0, 255, 0), (255, 255, 255), "player1"))
        #self.objects.append(Station(4, self.players[0], (100, 200)))
        #self.objects.append(Station(10, self.players[0], (200, 300)))
        #self.objects.append(Station(1000, self.players[1], (300, 500)))

        self.player = self.players[1]

        self.selection = []

        self.generate(1024, 768, 10)

    def generate(self, sizex, sizey, numstations):  #generating a simple random map

        maxRate = 100
        minRate = 10
        for x in range(numstations):
            rate = random.randint(minRate, maxRate)
            player = self.players[random.randint(0, len(self.players))-1]
            station = Station(rate, player, (0, 0)) #position doesn't matter yet we'll be trial and erroring it soon
            conflict = True
            while conflict:
                station.position = (random.randint(0, sizex), random.randint(0, sizey))
                conflict = False
                for s in self.objects:
                    #failure conditions
                    if utils.inCircle(s.position, station.size * 2, station.position):
                        conflict = True
                        break
                    elif utils.inCircle(station.position, s.size *2, s.position):
                        conflict = True
                        break
            self.objects.append(station)


    def selectPoints(self, points, mouse=False):
        for o in self.objects:
            for p in points:
                if utils.inCircle(p, o.size, o.position):
                    if not mouse and o.owner == self.player:
                        o.selected = not o.selected
                        self.selection.append(o)
                    elif mouse:
                        o.mouseSelect = True

    def selectRect(self, rect, mouse=False):
        if not mouse:
            print("ehree")
            print(rect)
        for o in self.objects:
            if utils.inRect(rect, o.position) and o.owner == self.player:
                if not mouse:
                    print("asdfasldkf")
                    print(rect)
                if not mouse:
                    o.selected = True
                    self.selection.append(o)
                elif mouse:
                    o.mouseSelect = True

    def selectHoverPoint(self, pos):
        self.selectPoints([pos], True)

    def selectHoverRect(self, rect):
        self.selectRect(rect, True)

    def deselectAll(self):
        for o in self.objects:
            o.selected = False

        self.selection.clear()

    def selectAll(self):
        for o in self.objects:
            if o.owner == self.player:
                o.selected = True
                self.selection.append(o)

    def update(self, elapsed):
        self.selection.clear()
        if(elapsed-self.lastelapsed >= self.dt): #if it is a dt or greater
            self.lastelapsed = elapsed + (elapsed-self.lastelapsed-1000)
            for o in self.objects:
                o.generate()

    def draw(self, screen, font, mousePos):
        for o in self.objects:
            o.draw(screen, font)

            if o.selected or o.mouseSelect:
                goodgfx.circle(screen, o.owner.selectcolor, o.position, o.size + 10, 5)
                if not o.mouseSelect:
                    pygame.gfxdraw.line(screen, o.position[0], o.position[1], mousePos[0], mousePos[1], o.owner.selectcolor)

                o.mouseSelect = False
