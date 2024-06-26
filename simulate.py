import time
import pygame
import numpy as np

# game constants
COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (46, 139, 87)
WINDOW_SIZE = (800, 600)
CELL_SIZE = (60, 80)


def update(screen, cells, size=10, with_progress=False):
	'''
	update cells for the next generation
	'''

	updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
	
	for row, col in np.ndindex(cells.shape):
		alive = np.sum(cells[row-1 : row+2, col-1 : col+2]) - cells[row, col] # sum of neighbours
		color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

		if cells[row, col] == 1: # cell is alive currently
			if alive < 2 or alive > 3:
				if with_progress:
					color = COLOR_DIE_NEXT

			elif 2 <= alive <= 3:
				updated_cells[row, col] = 1 # cell survives next gen
				if with_progress:
					color = COLOR_ALIVE_NEXT

		else:
			if alive == 3:
				updated_cells[row, col] = 1
				if with_progress:
					color = COLOR_ALIVE_NEXT

		# draw individual cells
		pygame.draw.rect(screen, color, (col*size, row*size, size-1, size-1))

	return updated_cells


def clear_screen(screen):
	'''
	clears the window
	'''
	cells = np.zeros(CELL_SIZE)
	screen.fill(COLOR_GRID)
	update(screen, cells)
	pygame.display.flip()

	return cells


def main():
	pygame.init()
	pygame.display.set_caption('Game of Life')
	pygame.display.set_icon(pygame.image.load('icon.ico'))
	screen = pygame.display.set_mode(WINDOW_SIZE)
	
	cells = np.zeros(CELL_SIZE)
	screen.fill(COLOR_GRID)
	update(screen, cells)

	pygame.display.flip()
	pygame.display.update()

	running = False
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					running = not running
					update(screen, cells)
					pygame.display.update()

				if event.key == pygame.K_ESCAPE:
					cells = clear_screen(screen)
					running = False


			if pygame.mouse.get_pressed()[0]:
				try:
					pos = pygame.mouse.get_pos()
					cells[pos[1] // 10, pos[0] // 10] = 1 #10: size
					update(screen, cells)
					pygame.display.update()
				except:
					pass

		screen.fill(COLOR_GRID)

		if running:
			cells = update(screen, cells, with_progress=True)
			pygame.display.update()

		time.sleep(0.001)


if __name__ == '__main__':
	main()