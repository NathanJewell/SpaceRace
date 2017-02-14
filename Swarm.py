#external dependencies
import pygame
from pygame.locals import *
from pygame import gfxdraw
import math
import time
import drawshapes as goodgfx
import gameUtils as utils
import random

class Swarm:


    def __init__(self, amount, origin, destination): #amount in transit, objects that are origin and destination

        #game params
        self.size = amount
        self.speed = 10 #pixels per second
        self.origin = origin
        self.destination = destination
        self.slope = utils.slope(origin.position, destination.position)
        self.length = utils.distance(origin.position, destination.position)
        self.center = origin.position
        self.ships = []
        #flocking params
        self.sightAngle = 270
        self.sightRadius = 50

        self.transparentScreen = pygame.Surface((1024, 768), pygame.SRCALPHA) #this should be moved to swarm handler

        self.spawn()

    def spawn(self):
        self.motherships = self.size//1000
        self.cruisers = (self.size % 1000 ) // 100
        self.fighters  = self.size % 100
        print(self.size)
        print(self.motherships)
        print(self.cruisers)
        print(self.fighters)

        def randPos(pos, dist):
            return (pos[0] + random.randint(-dist, dist), pos[1] + random.randint(-dist, dist))

        for m in range(self.motherships):
            self.ships.append(Ship(10, self.origin.owner.color, randPos(self.origin.position, 100)))
        for c in range(self.cruisers):
            self.ships.append(Ship(5, self.origin.owner.color, randPos(self.origin.position, 100)))
        for f in range(self.fighters):
            self.ships.append(Ship(2, self.origin.owner.color, randPos(self.origin.position, 100)))

    def update(self, dt): #time change in milliseconds
        dt/=1000
        dpx = self.speed*dt*-1
        dpy = self.speed*dt*self.slope*-1

        for s in self.ships:
            s.addPosition((dpx, dpy))


    def draw(self, screen):
        self.transparentScreen.fill((0, 0, 0, 0))
        for s in self.ships:
            s.draw(self.transparentScreen)
        screen.blit(self.transparentScreen, (0, 0))



class Ship:
    def __init__(self, size, color, position):
        self.size = size
        self.color = color + (100,) #inserting transparency value
        self.position = position
        self.intposition = (int(position[0]), int(position[1]))

    def addPosition(self, delta):
        self.position = (self.position[0] + delta[0], self.position[1] + delta[1])

    def draw(self, screen):
        self.intposition = (int(self.position[0]), int(self.position[1]))
        pygame.draw.circle(screen, self.color, self.intposition, self.size)
