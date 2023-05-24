import pygame
import math
from queue import PriorityQueue

WIDTH = 700
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Path Finding Algorithm")
clock = pygame.time.Clock()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot(object):
	"""docstring for Spot"""
	def __init__(self, row, col, width, total_rows, total_cols):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.height = width
		self.total_rows = total_rows
		self.total_cols = total_cols

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return color == TURQUOISE

	def reset(self):
		self.color = WHITE
		
	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_start(self):
		self.color = ORANGE

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def make_run(self):
		self.color = PURPLE

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height))

	def update_neighbors(self, grid):
		self.neighbors
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # down
			self.neighbors.append(grid[self.row + 1][self.col])
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # up
			self.neighbors.append(grid[self.row - 1][self.col])
		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # left
			self.neighbors.append(grid[self.row][self.col - 1])
		if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier(): # right
			self.neighbors.append(grid[self.row][self.col + 1])

	def __lt__(self, other):
		return False

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		# clock.tick(5)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			# make path
			reconstruct_path(came_from, end, draw)
			start.make_start()
			end.make_end()
			return True
		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()
		print(count)
		current.make_run()
		draw()

		if current != start:
			current.make_closed()
			pass
	return False

def make_grid(rows, cols, width):
	grid = []
	gap = width // rows

	for i in range(rows):
		grid.append([])
		for j in range(cols):
			spot = Spot(i, j, gap, rows, cols)
			grid[i].append(spot)

	return grid

def draw_grid(screen, rows, cols, width, height):
	gap = width // rows
	for i in range(cols):
		pygame.draw.line(screen, GREY, (0, i * gap), (width, i * gap))

	for i in range(rows):
		pygame.draw.line(screen, GREY, (i * gap, 0), (i * gap, height))


def drawWindow(screen, grid, rows, cols, width, height):
	screen.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(screen)

	draw_grid(screen, rows, cols, width, height)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap 

	return row, col

def main(screen, width, height):
	ROWS = 50
	COLS = 50
	grid = make_grid(ROWS, COLS, width)

	start = None
	end = None

	running = True
	started = False

	while running :
		drawWindow(screen, grid, ROWS, COLS, width, height)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			if started:
				continue

			if pygame.mouse.get_pressed()[0]: #left mouse
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot!= end and spot!= start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: #right mouse
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				if spot == end:
					end = None
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
					algorithm(lambda: drawWindow(screen, grid, ROWS, COLS, width, height), grid, start, end)
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, COLS, width)
if __name__ == "__main__":
	main(screen, WIDTH, HEIGHT)