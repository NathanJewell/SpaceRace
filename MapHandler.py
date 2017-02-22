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
from Swarm import *



class MapHandler:

    def __init__(self):
        generateMap = False
        self.lastelapsed = 0
        self.objects = []
        self.swarms = []
        self.players = []
        self.tick = 1000	#units generate every one second

        #setting up system
        self.players.append(Player((128,128,128), (255, 0, 0), "neutral"))
        self.players.append(Player((0, 255, 0), (255, 255, 255), "player1"))

        self.player = self.players[1]

        self.selection = []
        self.attackratio = .5

        self.generate(1024, 768, 10)

        self.elapsed = 0
        self.dt = 0

        self.transparentScreen = pygame.Surface((1024, 768), pygame.SRCALPHA) #this should be moved to swarm handler

        mothership = pygame.image.load("mothership.png")
        cruiser = pygame.image.load("cruiser.png")
        scrapper = pygame.image.load("scrapper.png")
        fighter = pygame.image.load("fighter.png")
        self.swarmGraphic = [mothership, cruiser, scrapper, fighter]

    def generate(self, sizex, sizey, numstations):  #generating a simple random map
        maxRate = 120
        minRate = 20
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

    def doAttack(self, mousePos):
        target = None
        for o in self.objects:
            if utils.inCircle(mousePos, o.size, o.position):
                    target = o
        if target:
            for o in self.selection:
                if target != o:
                    self.swarms.append(Swarm(int(o.contents * self.attackratio), o, target, self.swarmGraphic))

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
        for o in self.objects:
            if utils.inRect(rect, o.position) and o.owner == self.player:
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
        self.dt = elapsed-self.elapsed
        self.elapsed = elapsed
        for o in self.objects:
            o.update(self.dt)

        for s in self.swarms:
            s.update(self.dt)
            if len(s.ships) == 0:
                self.swarms.remove(s)


    def draw(self, screen, font, mousePos, elapsed):
        self.transparentScreen.fill((0, 0, 0, 0))

        for o in self.objects:
            o.draw(screen, font)

            if o.selected or o.mouseSelect:
                #goodgfx.circle(screen, o.owner.selectcolor, o.position, o.size + 10, 5)
                pygame.draw.circle(screen, o.owner.selectcolor, o.position, o.size+10)
                if not o.mouseSelect:
                    pygame.gfxdraw.line(screen, o.position[0], o.position[1], mousePos[0], mousePos[1], o.owner.selectcolor)


                o.mouseSelect = False

        for s in self.swarms:
            s.draw(self.transparentScreen)

        screen.blit(self.transparentScreen, (0, 0))
