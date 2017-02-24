#external dependencies
import pyglet
import pygame
import math
import time
import gameUtils as utils
import random

#internal dependencies
from MapHandler import *
from Station import *
from Player import *

import accelerate
from accelerate import profiler

class Game:

    def __init__(self):
        self.screen = pyglet.window.Window(800, 800)
        self.screen.on_draw = self.on_draw
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
        self.mapHandler = MapHandler()

    def start(self):
        self.setup()
        self.targetFPS = 480;
        self.targetFrametimeMs = int(1000/targetFPS)
        t = time.time() * 1000
        self.lastelapsed = 0
        pyglet.clock.schedule_interval(self.on_update, 1/120.0);  #setting update max frames to 120
        pyglet.app.run()



    def on_draw():
        self.mapHandler.draw(self.mousePos, elapsed)

        self.p.disable()
        #drawing selection box
        if self.selection:
            #use muted or highlighted version of user color for selection
            width = self.selection[0][0] - self.selection[1][0]
            height = self.selection[0][1] - self.selection[1][1]
            posx = self.selection[0][0]
            posy = self.selection[0][1]
            pygame.draw.rect(self.transparentScreen, (200, 200, 200, 128), (posx, posy, -1*width, -1*height))

        fpstext = pyglet.text.Label(text=framerateText, x=self.position[0], y=self.position[1]+self.size, batch=batch) #self.owner.color
        fpstext.draw()

    def on_update():
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
                            self.mapHandler.doAttack(self.mousePos)
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
                    self.p.print_stats()
                    self.end = True

            self.screen.fill((0, 0, 0))
            self.transparentScreen.fill((0, 0, 0, 0))
            #updating

            self.mapHandler.update(elapsed)
            if self.selection:
                self.mapHandler.selectHoverRect(self.selection)
            if len(self.clickQueue) > 0:
                self.mapHandler.selectPoints(self.clickQueue)
                self.clickQueue.clear()
            self.mapHandler.selectHoverPoint(self.mousePos)




            #drawing


            #controlling fps by waiting for any extra time to pass
            frametime = time.time() * 1000 -framestart
            #font.render(str(self.contents), 1, self.owner.invcolor);
            waittime = int(targetFrametimeMs - frametime)
            framerateText = self.gamefont.render(str(1000/frametime), 1, (255, 255, 255));



            if waittime > 0:
                pygame.time.wait(waittime)
