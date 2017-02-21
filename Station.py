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


class Station:

    def __init__(self, rate, owner, position):
        self.rate = rate  #generation speed per minute
        self.interval = int((60/rate)*1000) #time between adding one in ms
        self.size = int(3*math.sqrt(self.rate) + 10)
        self.position = position
        self.owner = owner #owner is a reference to a player
        self.contents = 0
        self.selected = False
        self.mouseSelect = False
        self.elapsed = 0

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

    def draw(self, screen, font):
        pygame.draw.circle(screen, self.owner.color, self.position, self.size)
        nametext = font.render(self.owner.name, 1, self.owner.invcolor)
        contenttext = font.render(str(self.contents), 1, self.owner.invcolor);

        screen.blit(contenttext, (self.position[0] - contenttext.get_rect().width/2, self.position[1] - contenttext.get_rect().height/2))
        screen.blit(nametext, (self.position[0] - nametext.get_rect().width/2, self.position[1] - nametext.get_rect().height - self.size))
