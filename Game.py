#external dependencies
import pyglet
import pygame
import math
import time
import gameUtils as utils
import random
import accelerate

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
        self.screen.on_mouse_motion = self.on_mouse_motion
        self.screen.on_key_press = self.on_key_press
        self.screen.on_key_release = self.on_key_release
        self.screen.on_mouse_press = self.on_mouse_press
        self.screen.on_mouse_release = self.on_mouse_release
        self.screen.on_mouse_drag = self.on_mouse_drag
        self.end = False


        self.selection = None
        self.clickQueue = []
        self.mouseDown = False
        self.mouseDownPos = (0, 0)
        self.mouseUpPos = (0, 0)
        self.mousePos = (0, 0)
        self.dragging = False
        self.shifting = False

    def setup(self):
        self.mapHandler = MapHandler()
        self.guiBatch = pyglet.graphics.Batch()

    def start(self):
        self.setup()
        self.targetFPS = 480;
        self.targetFrametimeMs = int(1000/self.targetFPS)
        t = time.time() * 1000
        self.lastelapsed = 0
        self.elapsed = 0
        self.framestart = 0
        self.frametime = 1
        pyglet.clock.schedule(self.on_update);  #setting update max frames to 120
        p = profiler.Profile(signatures=False)
        p.enable()
        pyglet.app.run()
        p.disable()
        p.print_stats()
        profiler.plot(p)



    def on_draw(self):
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        self.screen.clear()
        self.guiBatch = pyglet.graphics.Batch()
        self.mapHandler.draw(self.mousePos, self.elapsed)

        #drawing selection box
        if self.selection:
            #use muted or highlighted version of user color for selection
            primitives.rect(self.selection[0][0], self.selection[0][1], self.selection[1][0], self.selection[1][1], (200, 0, 200, 128), self.guiBatch, pyglet.graphics.OrderedGroup(3))
            #pygame.draw.rect(self.transparentScreen, (200, 200, 200, 128), (posx, posy, -1*width, -1*height))

        print(pyglet.clock.get_fps())
        #fpstext.draw()

        self.guiBatch.draw()

    def on_update(self, dt):

        self.mapHandler.update(dt*1000)
        if self.selection:
            self.mapHandler.selectHoverRect(self.selection)
        if len(self.clickQueue) > 0:
            self.mapHandler.selectPoints(self.clickQueue)
            self.clickQueue.clear()
        self.mapHandler.selectHoverPoint(self.mousePos)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mousePos = (x, y)
        if self.mouseDown:
            self.dragging = True
        if self.mouseDown and self.shifting:
            self.selection = (self.mouseDownPos, self.mousePos) #selection is updated

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.mousePos = (x, y)
        if self.mouseDown:
            self.dragging = True
        if self.mouseDown and self.shifting:
            self.selection = (self.mouseDownPos, self.mousePos) #selection is updated

    def on_mouse_press(self, x, y, button, modifiers):

        self.mousePos = (x, y)
        if button == pyglet.window.mouse.LEFT:
            self.mouseDown = True;
            self.mouseDownPos = self.mousePos
            if self.shifting:
                self.clickQueue.append(self.mousePos)
            else:
                self.mapHandler.doAttack(self.mousePos)
                self.mapHandler.deselectAll()

    def on_mouse_release(self, x, y, button, modifiers):

        self.mousePos = (x, y)
        if  button == pyglet.window.mouse.LEFT:
            self.mouseDown = False;
            self.mouseUpPos = self.mousePos
            if self.dragging and self.shifting:
                self.mapHandler.selectRect(self.selection)
                self.selection = None
                self.dragging = False
            if not self.shifting:
                self.clickQueue.clear()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.LSHIFT:
            self.shifting = True

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.LSHIFT:
            self.shifting = False


        #def on_mouse_draw(x, y, button, modifiers):
