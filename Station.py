#external dependencies
import pyglet
from pyglet import graphics
import math
import time
import primitives
import gameUtils as utils
import random

#internal dependencies


class Station:

    def __init__(self, rate, owner, position, batch):
        self.rate = rate  #generation speed per minute
        self.interval = int((60/rate)*1000) #time between adding one in ms
        self.size = int(3*math.sqrt(self.rate) + 10)
        self.position = position
        self.owner = owner #owner is a reference to a player
        self.contents = 0
        self.selected = False
        self.mouseSelect = False
        self.elapsed = 0

        self.verts = primitives.circle_verts(self.position[0], self.position[1], 30, self.size) #v2i for circle points
        self.color = []
        self.capture()
        batch.add(len(self.verts)//2, pyglet.gl.GL_TRIANGLES, pyglet.graphics.OrderedGroup(0), ('v2i', self.verts), ('c3b', self.color))

    def capture(self):
        self.color = (self.owner.color*(len(self.verts)//2))

    def defend(self, amount):   #defending is losing troops so same as sending troops
        self.contents -= amount

    def send(self, amount): #recieving contents from friendly
        self.contents -= amount

    def recieve(self, amount):
        self.contents += amount

    def update(self, dt):
        self.elapsed += dt
        if self.elapsed >= self.interval:
            self.elapsed -= self.interval
            self.contents += 1

    def draw(self, batch):
        #pygame.draw.circle(screen, self.owner.color, self.position, self.size)  #self.owner.color
        nametext = pyglet.text.Label(text=self.owner.name, x=self.position[0], y=self.position[1]+self.size, batch=batch, group=pyglet.graphics.OrderedGroup(1)) #self.owner.color
        contenttext = pyglet.text.Label(text=str(self.contents), x=self.position[0], y=self.position[1], batch=batch, group=pyglet.graphics.OrderedGroup(1))

        primitives.circle(self.position[0], self.position[1], 30, self.size, self.owner.color, batch, pyglet.graphics.OrderedGroup(0))


        nametext.draw()
        contenttext.draw()
