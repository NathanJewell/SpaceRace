import pygame
from pygame.locals import *
import math
import time

#manage generation for objects
#basic info for objects that generate stuff

class Station:
	#self.rate = 1 #generation speed per timestep
	#self.contents = 100
	#self.owner = 0 #owner is a reference to a player
	#self.size = 5
	#self.position = (0, 0)

	def __init__(self, rate, owner, position):
		self.rate = rate
		self.size = int(5*math.sqrt(self.rate) + 10)
		self.position = position
		self.owner = owner
		self.contents = 100

	def generate(self):
		self.contents += self.rate

	def attack(self, amount): #attack something with this amount
		self.contents -= amount

	def recieve(self, amount): #recieving contents from friendly
		self.content += amount

	def draw(self, screen, font):
		pygame.draw.circle(screen, self.owner.color, self.position, self.size)
		nametext = font.render(self.owner.name, 1, self.owner.invcolor)
		contenttext = font.render(str(self.contents), 1, self.owner.invcolor);

		screen.blit(contenttext, (self.position[0] - contenttext.get_rect().width/2, self.position[1] - contenttext.get_rect().height/2))
		screen.blit(nametext, (self.position[0] - nametext.get_rect().width/2, self.position[1] - nametext.get_rect().height - self.size))



class Player:
	#self.color = (0, 255, 0)	#color for player planets and units
	#self.name = "unknown"		#custom player name

	def __init__(self, color, invcolor, name):
		self.color = color
		self.invcolor = invcolor
		self.name = name

#class Earth:




class Game:

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((1024, 768), DOUBLEBUF)
		self.end = False
		self.objects = []
		self.players = []
		self.dt = 1000	#units generate every one second

	def setup(self):
		self.players.append(Player((128,128,128), (255, 0, 0), "neutral"))
		self.players.append(Player((0, 255, 0), (0, 0, 255), "player2"))
		self.objects.append(Station(4, self.players[0], (100, 200)))
		self.objects.append(Station(10, self.players[0], (200, 300)))


		self.objects.append(Station(1000, self.players[1], (300, 500)))

		self.gamefont = pygame.font.SysFont("monospace", 15)


	def start(self):
		self.setup()
		targetFPS = 120;
		targetFrametimeMs = int(1000/targetFPS)
		t = time.time() * 1000
		lastelapsed = 0
		while not self.end:	#main game loop
			framestart = time.time() * 1000
			elapsed = int((framestart-t)) #elapsed time in ms
			#event handling
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.end = True
			

			#updating
			if(elapsed-lastelapsed >= 1000): #if it is a dt or greater
				lastelapsed = elapsed + (elapsed-lastelapsed-1000)
				for o in self.objects: 
					o.generate()
			
		

			#drawing
			for o in self.objects:
				o.draw(self.screen, self.gamefont)

			pygame.display.flip() #flip buffer

			frametime = time.time() * 1000 -framestart
			waittime = int(targetFrametimeMs - frametime)
			if waittime > 0:
				pygame.time.wait(waittime)

def main():
	game = Game()
	game.start()


if __name__ == "__main__":
	main()