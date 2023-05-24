import pygame
import neat
import time
import random
import os
pygame.font.init()

WIN_WIDTH = 570
WIN_HEIGHT = 800

GEN = 0

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))]
PIPE_IMGS = pygame.transform.scale2x(pygame.image.l oad(os.path.join("images", "pipe.png")))
BASE_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
BG_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Bird(object):
	IMGS = BIRD_IMGS
	MAX_ROTATTION = 25
	ROT_VEL = 20
	ANIMATION_TIME = 5
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.tilt =  0
		self.tick_count = 0
		self.vel = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0]

	def jump(self):
		self.vel = -10.5
		self.tick_count = 0
		self.height = self.y

	def move(self):
		self.tick_count += 1

		display = self.vel*self.tick_count + 2.25 * self.tick_count**2

		if display >= 16:
			display = 16 
		if display < 0:      
			# print(display)
			display -= 10         
		self.y = self.y + display

		if self.y < self.height + 50:
			if self.tilt < self.MAX_ROTATTION:
				self.tilt = self.MAX_ROTATTION
		else:
			if self.tilt > -60:
				self.tilt -= self.ROT_VEL
	def draw(self, screen):
		self.img_count += 1

		if self.img_count < self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*3:
			self.img = self.IMGS[2]
		elif self.img_count < self.ANIMATION_TIME*4:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*4 + 1:
			self.img = self.IMGS[0]
			self.img_count = 0  
		if self.tilt < -80:
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_TIME * 2

		rotated_image = pygame.transform.rotate(self.img, self.tilt)
		new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
		screen.blit(rotated_image, new_rect.topleft)

	def get_mark(self):
		return pygame.mask.from_surface(self.img)

class Pipe(object):
	GAP = 200
	VEL = 5

	def __init__(self, x):
		self.x = x
		self.height = 0
		self.top = 0
		self.bot = 0
		self.PIPE_TOP = pygame.transform.flip(PIPE_IMGS, False, True)
		self.PIPE_BOTTOM = PIPE_IMGS

		self.passed = False
		self.set_height()
	def set_height(self):
		self.height = random.randrange(50,450)
		self.top = self.height - self.PIPE_TOP.get_height()
		self.bottom = self.height + self.GAP

	def move(self):
		self.x -= self.VEL

	def draw(self, screen):
		screen.blit(self.PIPE_TOP, (self.x, self.top))
		screen.blit(self.PIPE_BOTTOM,(self.x, self.bottom))

	def collide(self, bird):
		bird_mask = bird.get_mark()
		top_mask = pygame.mask.from_surface(self.PIPE_TOP)
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

		top_offset = (self.x - bird.x, self.top - round(bird.y))
		bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

		b_point = bird_mask.overlap(bottom_mask, bottom_offset)
		t_point = bird_mask.overlap(top_mask, top_offset)
		if b_point or t_point:
			return True
		return False

class Base(object):
	VEL = 5
	WIDTH = BASE_IMGS.get_width()
	IMG = BASE_IMGS
	def __init__(self,y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1 + self.WIDTH<0:
			self.x1 = self.x2 + self.WIDTH

		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH

	def draw(self, screen):
		screen.blit(self.IMG, (self.x1, self.y))
		screen.blit(self.IMG, (self.x2, self.y))

def draw_window(screen, birds, pipes, base, score):

	screen.blit(BG_IMGS, (0,0))
	for pipe in pipes:
		pipe.draw(screen)

	text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
	screen.blit(text, (WIN_WIDTH -10 -text.get_width(),10))


	base.draw(screen)
	for bird in birds:
		bird.draw(screen)
	base.move()
	pygame.display.update()

def main():
	birds = [Bird(230,500)]
	base = Base(700)
	pipes = [Pipe(600)]
	score = 0

	screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
	clock = pygame.time.Clock()
	runLoop = 0
	run = True
	while run:
		clock.tick(25)
		if runLoop > 0:
			runLoop += 1
		if runLoop > 20:
			runLoop = 0
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit() 
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE: 
					birds[0].jump() 
		
		rem = [] 
		for pipe in pipes:
			add_pipe = False
			for x, bird in enumerate(birds):
				if pipe.collide(bird):
					birds.pop(x)

				if not pipe.passed and pipe.x < bird.x:
					pipe.passed = True
					add_pipe = True
			if pipe.x + pipe.PIPE_TOP.get_width() < 0:
					rem.append(pipe)
			pipe.move()

			if add_pipe:
				score += 1
				pipes.append(Pipe(600))

		for r in rem:
			pipes.remove(r)

		for x,bird in enumerate(birds):
			if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
				birds.pop(x)
		if len(birds) > 0:
			birds[0].move()
		else:
			run = False 
		draw_window(screen, birds, pipes, base, score)

	


if __name__ == "__main__":
	main()