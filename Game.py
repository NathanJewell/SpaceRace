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
from MapHandler import *
from Station import *
from Player import *

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768), DOUBLEBUF)
        self.transparentScreen = pygame.Surface((1024, 768), pygame.SRCALPHA)
        self.end = False


        self.selection = None
        self.clickQueue = []
        self.mouseDown = False
        self.mouseDownPos = None
        self.mouseUpPos = None
        self.mousePos = None
        self.dragging = False
        self.shifting = False

    def setup(self):
        self.gamefont = pygame.font.SysFont("monospace", 15)

        self.mapHandler = MapHandler()

    def start(self):
        self.setup()
        targetFPS = 120;
        targetFrametimeMs = int(1000/targetFPS)
        t = time.time() * 1000
        lastelapsed = 0

        while not self.end:	#main game loop

            framestart = time.time() * 1000
            elapsed = int((framestart-t)) #elapsed time in ms

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        self.shifting = True

                elif event.type == KEYUP:
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        self.shifting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousePos = event.pos
                    if event.button == 1:
                        self.mouseDown = True;
                        self.mouseDownPos = self.mousePos
                        if self.shifting:
                            self.clickQueue.append(self.mousePos)
                        else:
                            self.mapHandler.deselectAll()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mousePos = event.pos
                    if event.button == 1:
                        self.mouseDown = False;
                        self.mouseUpPos = self.mousePos
                        if self.dragging and self.shifting:
                            self.mapHandler.selectRect(self.selection)
                            self.selection = None
                            self.dragging = False
                        if not self.shifting:
                            self.clickQueue.clear()
                elif event.type == pygame.MOUSEMOTION:
                    self.mousePos = event.pos
                    if self.mouseDown:
                        self.dragging = True
                    if self.mouseDown and self.shifting:
                        self.selection = (self.mouseDownPos, self.mousePos) #selection is updated
                if event.type == pygame.QUIT:
                    self.end = True

            self.screen.fill((0, 0, 0))
            self.transparentScreen.fill((0, 0, 0, 0))
            #updating

            #end = self.inputHandler.update()
            self.mapHandler.update(elapsed)
            if self.selection:
                self.mapHandler.selectHoverRect(self.selection)
            if len(self.clickQueue) > 0:
                self.mapHandler.selectPoints(self.clickQueue)
                self.clickQueue.clear()
            self.mapHandler.selectHoverPoint(self.mousePos)
            #drawing
            self.mapHandler.draw(self.screen, self.gamefont, self.mousePos)


            if self.selection:
                #use muted or highlighted version of user color for selection
                width = self.selection[0][0] - self.selection[1][0]
                height = self.selection[0][1] - self.selection[1][1]
                posx = self.selection[0][0]
                posy = self.selection[0][1]
                pygame.draw.rect(self.transparentScreen, (200, 200, 200, 128), (posx, posy, -1*width, -1*height))

            for p in self.clickQueue:
                pygame.draw.circle(self.screen, (200, 200, 200), p, 5)
            #self.inputHandler.draw(self.screen)

            self.screen.blit(self.transparentScreen, (0, 0))
            pygame.display.flip() #flip buffer

            #controlling fps by waiting for max fps
            frametime = time.time() * 1000 -framestart
            waittime = int(targetFrametimeMs - frametime)
            if waittime > 0:
                pygame.time.wait(waittime)
