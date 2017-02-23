#external dependencies
import pygame
from pygame.locals import *
from pygame import gfxdraw
import math
import time
import drawshapes as goodgfx
import gameUtils as utils
import random
import numpy
class Swarm:


    def __init__(self, amount, origin, destination, graphics): #amount in transit, objects that are origin and destination

        #game params
        self.size = amount
        self.speed = 50 #pixels per second
        self.origin = origin
        self.destination = destination
        self.slope = utils.normDiff(origin.position, destination.position)
        #self.angle = math.atan(self.slope)
        self.length = utils.distance(origin.position, destination.position)
        self.center = origin.position
        #self.ships = []
        self.ships = []


        self.origin.contents -= amount
        self.graphics = graphics
        self.spawn()

    def spawn(self):
        self.motherships = self.size//1000
        self.cruisers = (self.size % 1000 ) // 100
        self.scrappers = (self.size % 100) // 10
        self.fighters  = self.size % 10

        def randPos(pos, dist):
            return (pos[0] + random.randint(-dist, dist), pos[1] + random.randint(-dist, dist))

        for m in range(self.motherships):
            self.ships.append(Ship(25, 1000, self.origin.owner.color, randPos(self.origin.position, 100), self.destination.position, self.graphics[0]))
        for c in range(self.cruisers):
            self.ships.append(Ship(10, 100, self.origin.owner.color, randPos(self.origin.position, 100), self.destination.position, self.graphics[1]))
        for s in range(self.scrappers):
            self.ships.append(Ship(5, 10, self.origin.owner.color, randPos(self.origin.position, 100), self.destination.position, self.graphics[2]))
        for f in range(self.fighters):
            self.ships.append(Ship(2, 1, self.origin.owner.color, randPos(self.origin.position, 100), self.destination.position, self.graphics[3]))


    def update(self, dt): #time change in milliseconds
        dt/=1000
        dt *= self.speed

        for s in self.ships:
            if utils.inCircle(s.position, self.destination.size + s.size*1.41, self.destination.position):
                if self.destination.owner == self.origin.owner:
                    self.destination.recieve(s.amount)
                else:
                    self.destination.defend(s.amount)
                s.kill()
            s.update(dt)

        if self.destination.contents <= 0:
            self.destination.owner = self.origin.owner
            self.destination.contents = abs(self.destination.contents)

    def draw(self, screen):
        self.ships.draw(screen)




class Ship(pyglet.sprite.Sprite):
    def __init__(self, size, amount, color, position, destination, tex):
        pygame.sprite.Sprite.__init__(self)

        self.image = tex
        self.rect = self.image.get_rect()
        self.size = size

        self.halfsize = self.size//2
        self.amount = amount
        self.color = color + (100,) #inserting transparency value
        self.position = [position[0], position[1]]
        self.intposition = [int(position[0]), int(position[1])]
        self.slope = utils.normDiff(self.position, destination)
        print(math.atan(self.slope[1]/self.slope[0]))
        a = utils.rot_center(self.image, self.rect, numpy.sign(self.slope[0])*math.atan(self.slope[0]/self.slope[1])/math.pi*180)
        self.image = a[0]
        self.rect = a[1]
        #self.image = pygame.transform.rotate(self.image, math.atan(self.slope[1]/self.slope[0]))

    def update(self, dt):
        self.position[0] -= dt*self.slope[0]
        self.position[1] -= dt*self.slope[1]
        self.intposition = [int(a) for a in self.position] #middle
        BR = [self.intposition[0] + self.halfsize, self.intposition[1]+self.halfsize]
        TL = [self.intposition[0] - self.halfsize, self.intposition[1]-self.halfsize]
        self.rect = [TL, BR]

    """def draw(self, screen):
        self.intposition = [int(a) for a in self.position] #middle
        BR = [self.intposition[0] + self.halfsize, self.intposition[1]+self.halfsize]
        TL = [self.intposition[0] - self.halfsize, self.intposition[1]-self.halfsize]

        screen.blit(self.sprite, [TL, BR])


        #goodgfx.circle(screen, self.color, self.intposition, self.size, 2)
        #pygame.draw.circle(screen, self.color, self.intposition, self.size)"""
