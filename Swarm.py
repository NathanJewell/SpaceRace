#external dependencies
import pyglet
import math
import time
import primitives
import gameUtils as utils
import random
import numpy
class Swarm:


    def __init__(self, amount, origin, destination, graphics, batch): #amount in transit, objects that are origin and destination

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
        self.spawn(batch)

    def spawn(self, batch):
        self.motherships = self.size//1000
        self.cruisers = (self.size % 1000 ) // 100
        self.scrappers = (self.size % 100) // 10
        self.fighters  = self.size % 10

        def randPos(pos, dist):
            return (pos[0] + random.randint(-dist, dist), pos[1] + random.randint(-dist, dist))

        for m in range(self.motherships):
            self.ships.append(Ship(25, 1000, self.origin.owner.color, randPos(self.origin.position, 100), self.destination.position, self.graphics[0], batch))
        for c in range(self.cruisers):
            self.ships.append(Ship(10, 100, self.origin.owner.color, randPos(self.origin.position, 100), self.destination.position, self.graphics[1], batch))
        for s in range(self.scrappers):
            self.ships.append(Ship(5, 10, self.origin.owner.color, randPos(self.origin.position, 100), self.destination.position, self.graphics[2], batch))
        for f in range(self.fighters):
            self.ships.append(Ship(2, 1, self.origin.owner.color, randPos(self.origin.position, 100), self.destination.position, self.graphics[3], batch))


    def update(self, dt): #time change in milliseconds
        dt/=1000
        dt *= self.speed

        for s in self.ships:
            if utils.inCircle(s.position, self.destination.size + s.size*1.41, self.destination.position):
                if self.destination.owner == self.origin.owner:
                    self.destination.recieve(s.amount)
                else:
                    self.destination.defend(s.amount)
                self.ships.remove(s)
            s.update(dt)

        if self.destination.contents <= 0:
            self.destination.owner = self.origin.owner
            self.destination.contents = abs(self.destination.contents)
            self.destination.capture()

    def draw(self, screen):
        pass


class Ship:
    def __init__(self, size, amount, color, position, destination, tex, batch):
        self.sprite = pyglet.sprite.Sprite(tex, position[0], position[1], subpixel=True, batch=batch)

        self.size = size
        #self.sprite.height = size
        #self.sprite.width = size

        self.halfsize = self.size//2
        self.amount = amount
        self.position = [position[0], position[1]]
        self.slope = utils.normDiff(self.position, destination)\

        quad = 0; """ |_3_|_0_|     3 = 180+theta 0=-theta
                      |---s---|
                      |_2_|_1_|     2 = 180-theta 1 = +theta"""
        theta = 0
        if -1*self.slope[1] > 0:       #theta is just the sign of theta to be added and quad is wether or not 180 is there
            if -1*self.slope[0] > 0:
                quad = 0
                theta = -1
            else:
                quad = 1
                theta = 1
        else:
            if -1*self.slope[0] > 0:
                quad = 0
                theta = 1
            else:
                quad = 1
                theta = -1

        self.sprite.rotation = theta*(math.atan(abs(self.slope[1]/(self.slope[0]+.0001)))*180/math.pi) + quad*180 + 90 #90 is necessary because sprites are facing up by default

    def update(self, dt):
        self.position = [self.position[0]-(dt*self.slope[0]), self.position[1]-(dt*self.slope[1])]
        self.sprite.x = self.position[0]
        self.sprite.y = self.position[1]

    def draw(self):
        pass
