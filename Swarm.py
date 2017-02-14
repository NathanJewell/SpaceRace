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
        self.speed = 50 #pixels per second
        self.origin = origin
        self.destination = destination
        self.slope = utils.normDiff(origin.position, destination.position)
        #self.angle = math.atan(self.slope)
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
            self.ships.append(Ship(10, 1000, self.origin.owner.color, randPos(self.origin.position, 100), self.destination.position))
        for c in range(self.cruisers):
            self.ships.append(Ship(5, 100, self.origin.owner.color, randPos(self.origin.position, 100), self.destination.position))
        for f in range(self.fighters):
            self.ships.append(Ship(2, 1, self.origin.owner.color, randPos(self.origin.position, 100), self.destination.position))


    def update(self, dt): #time change in milliseconds
        dt/=1000
        dt *= self.speed

        for s in self.ships:
            if inCircle(s.position, self.destination.position, self.destination.size + s.size):
                destination.attack(s.amount)
                self.ships.remove(s)
            s.update(dt)



    def draw(self, screen):
        self.transparentScreen.fill((0, 0, 0, 0))
        for s in self.ships:
            s.draw(self.transparentScreen)
        screen.blit(self.transparentScreen, (0, 0))



class Ship:
    def __init__(self, size, amount, color, position, destination):
        self.size = size
        self.amount = amount
        self.color = color + (100,) #inserting transparency value
        self.position = position
        self.intposition = (int(position[0]), int(position[1]))
        self.slope = utils.normDiff(self.position, destination)


    def addPosition(self, delta):
        self.position = (self.position[0] + delta[0], self.position[1] + delta[1])

    def update(self, dt):
        dpx = dt*self.slope[0]*-1
        dpy = dt*self.slope[1]*-1
        self.addPosition((dpx, dpy))

    def draw(self, screen):
        self.intposition = (int(self.position[0]), int(self.position[1]))
        pygame.draw.circle(screen, self.color, self.intposition, self.size)