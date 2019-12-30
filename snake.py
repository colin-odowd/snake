import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Cube(object):
	rows = 20
	w = 500
	def __init__(self, start, dirnx=1, dirny=0, color = (255,0,0)):
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.color = color
	
	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0]+dirnx, self.pos[1]+self.dirny)
		
	def draw(self, surface, eyes=False):
		dis = self.w // self.rows
		i = self.pos[0]
		j = self.pos[1]
	
		pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
		
		if eyes:
			center = dis//2
			radius = 3
			circleMiddle = (i*dis+center-radius, j*dis+8)
			circleMiddle2 = (i*dis + dis - radius*2, j*dis+8)
			pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
			pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class Snake(object):
	body = []
	turns = {}
	
	def __init__(self, color, pos):
		self.color = color
		self.head = Cube(pos)
		self.body.append(self.head)
		self.dirnx = 0
		self.dirny = 0
	
	def reset(self, pos):
		self.head = Cube(pos)
		self.body = []
		self.turns = {}
		self.body.append(self.head)
		self.dirnx = 0
		self.dirny = 1		
	
	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			
			keys = pygame.key.get_pressed()
			
			for key in keys:
				if keys[pygame.K_LEFT]:
					self.dirnx= -1
					self.dirny= 0
					#stores position of head at a turn as a key, direction as entries
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
					
				elif keys[pygame.K_RIGHT]:
					self.dirnx= 1
					self.dirny= 0
					
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
				
				elif keys[pygame.K_UP]:
					self.dirnx= 0
					self.dirny= -1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
					
				elif keys[pygame.K_DOWN]:
					self.dirnx= 0
					self.dirny= 1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
		
		#loop to evaluate status of every body cube
		for i, c in enumerate(self.body):
			#copies cube position array
			p = c.pos[:]
			
			#check cube position array against turns array
			if p in self.turns:
				#if found, sets turn direction to the where the head turned
				turn = self.turns[p]
				
				#current cube is moved in the direction that the head turned
				c.move(turn[0], turn[1])
				
				#if all components of the body have moved through that turn, remove the turn from the list
				if i == len(self.body)-1:
					self.turns.pop(p)
					
			# if the body is not passing through a turn, check to see if it is at an edge		
			else: 
				#if at an edge, jump to other side 
				if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
				elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
				elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
				elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
				
				#if not at a turn or edge, move in the same direction as previously
				else: c.move(c.dirnx, c.dirny)
		
	def draw(self, surface):
		for i, c in enumerate(self.body):
			if i == 0:
				#first cube has eyes
				c.draw(surface, True)
			else:
				c.draw(surface)
	
	def addCube(self):
		#last cube on snake
		tail = self.body[-1]
		#current direction of tail
		dx, dy = tail.dirnx, tail.dirny
		
		#adds new cube in the direction that the snake is currently moving
		if dx == 1 and dy == 0:
			self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))	
		elif dx == -1 and dy == 0:
			self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))	
		elif dx == 0 and dy == 1:
			self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
		elif dx == 0 and dy == -1:
			self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))	
		
		#sets moving direction of new cube
		self.body[-1].dirnx = dx
		self.body[-1].dirny = dy
		
def randomSnack(rows, item):
	positions = item.body
	
	while True:
		x = random.randrange(rows)
		y = random.randrange(rows)
		#checks to see if the body of the snake is overlapping the item (snack)
		if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
			continue
		else:
			break
	return (x,y)
						
def drawGrid(w, rows, surface):
	sizeBtwn = w // rows
	x = 0 
	y = 0 
	for l in range(rows):
		x = x + sizeBtwn
		y = y + sizeBtwn
		
		pygame.draw.line(surface, (255, 255, 255), (x,0), (x,w))
		pygame.draw.line(surface, (255, 255, 255), (0,y), (w,y))


def redrawWindow(surface):
	
	global width, rows, s, snack
	surface.fill((0, 0, 0))
	drawGrid(width, rows, surface)
	s.draw(surface)
	snack.draw(surface)
	pygame.display.update()
	
def message_box(subject, content):
	#puts message box as top most window
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, content)
	try:
		root.destroy()
	except:
		pass

def main():

	global width, rows, s, snack
	width = 500
	rows = 20
	
	win = pygame.display.set_mode((width, width))
	
	s = Snake((255, 0, 0), (10,10))
	snack = Cube(randomSnack(rows, s), color = (0, 255, 0))
	flag = True
	
	clock = pygame.time.Clock()
	
	while flag:
		#pygame.event.wait()
		pygame.time.delay(50)
		#caps game at 10fps
		clock.tick(10)
		s.move()
		#if head of snake hits snack, add a cube to snake and regenerate the snack
		if s.body[0].pos == snack.pos:
			s.addCube()
			snack = Cube(randomSnack(rows, s), color = (0, 255, 0))
		
		for x in range(len(s.body)):
			if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
				print('Score: ', len(s.body))
				message_box('You lost!', 'Play again...')
				s.reset((10,10))
				break
		
		
		redrawWindow(win)

main()
