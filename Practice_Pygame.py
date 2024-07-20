# import pygame
# import random
# import math
# from pygame import mixer

# # Initialize Pygame
# pygame.init()

# # Set up the display
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Sorting Visualiser")

# #  Adding Background sound
# mixer.music.load('background.wav')
# mixer.music.play(-1)

# #  setting for the player

# playerimg = pygame.image.load('space-invaders.png')
# player_x = 370
# player_y = 480
# player_x_change = 0

# #  setting for the enemy

# enemyimg = []
# enemy_x = []
# enemy_y = []
# enemy_x_change = []
# enemy_y_change = []
# no_of_enemy = 6
# for i in range(no_of_enemy):
#     enemyimg.append(pygame.image.load('space-invaders (1).png'))
#     enemy_x.append(random.randint(0, 736))
#     enemy_y.append(random.randint(50, 100))
#     enemy_x_change.append(0.3)
#     enemy_y_change.append(40)


# # setting for the bullet

# bulletimg = pygame.image.load('bullet.png')
# bullet_x = 0
# bullet_y = 480
# bullet_y_change = 1.5
# bullet_state = "ready"
# #  Score value
# score = 0
# font = pygame.font.Font('freesansbold.ttf', 32)
# text_x = 10
# text_y = 10

# def show_score(x, y):
#     score_value = font.render("Score: " + str(score), True, (255,255,255))
#     screen.blit(score_value, (x, y))

# def player(x, y):
#     screen.blit(playerimg, (x, y))
    
    
# def enemy(x, y, i):
#     screen.blit(enemyimg[i], (x, y))
    
# def bullet(x, y):
#     global bullet_state
#     bullet_state = "fire"
#     screen.blit(bulletimg, (x + 16,y + 10))
    
# # Checking for collision

# def iscollision(enemyx, enemyy, bulletx, bullety):
#     distance = math.sqrt(math.pow(enemyx - bulletx, 2) + math.pow(enemyy - bullety, 2))
#     if(distance < 27):
#         return True
#     else:
#         return False


# # Main loop
# running = True
# while running:
#     # changing the color of the screen but not updated
#     screen.fill((155, 0, 55))
    
#     # Event handling
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         # if keystroke is pressed check whether it is left or right
#         if (event.type == pygame.KEYDOWN):
#             if(event.key == pygame.K_LEFT):
#                 player_x_change = -0.3
#             if(event.key == pygame.K_RIGHT):
#                 player_x_change = 0.3
#             if (event.key == pygame.K_SPACE):
#                 if(bullet_state == 'ready'):
#                     bullet_sound = mixer.Sound('laser.wav')
#                     bullet_sound.play()
#                     bullet_x = player_x
#                     bullet(player_x, bullet_y)
#         if (event.type == pygame.KEYUP):
#             if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
#                 player_x_change = 0
            
#     # setting the player for boundary
#     player_x += player_x_change
#     if(player_x > 736):
#         player_x = 736
    
#     elif(player_x < 0):
#         player_x = 0
    
#     # setting the enemy for boundary
#     for i in range(no_of_enemy):
#         enemy_x[i] += enemy_x_change[i]
#         if (enemy_x[i] > 736):
#             enemy_x_change[i] = -0.3
#             enemy_y[i] += enemy_y_change[i]
#         elif (enemy_x[i] <= 0):
#             enemy_x_change[i] = 0.3
#             enemy_y[i] += enemy_y_change[i]
#         elif (enemy_y[i] > 536):
#             enemy_y_change[i] = 0
#             enemy_x_change[i] = 0
#         # Collision workout
#         collision = iscollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
#         if (collision == True):
#             explosion_sound = mixer.Sound('explosion.wav')
#             explosion_sound.play()
#             bullet_y = 480
#             bullet_state = "ready"
#             score += 1
#             print(score)
#             enemy_x[i] = random.randint(0, 736)
#             enemy_y[i] = random.randint(50, 100)
#         enemy(enemy_x[i], enemy_y[i], i)
        
#     # Bullete movement
#     if(bullet_y < -10):
#         bullet_y = 480
#         bullet_state = "ready"
#     if(bullet_state == 'fire'):
#         bullet_y -= bullet_y_change
#         bullet(bullet_x, bullet_y)
    
#     player(player_x, player_y)
#     show_score(text_x, text_y)
    
#     # upadte whatever is updated
#     pygame.display.update()    
    
# # Quit Pygame
# pygame.quit()


import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

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
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		# DOWN
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		# RIGHT
		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

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
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
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

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]:  # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]:  # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()


main(WIN, WIDTH)
