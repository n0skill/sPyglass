import pygame
import time
def disp(data):
	screen	= pygame.display.set_mode((1024,768))
	black 	= (0,0,0)
	white 	= (255, 255, 255)
	yello	= (255, 125, 0)
	brown	= (125, 125, 50)
	orang	= (250, 255, 0)
	red		= (255, 0, 0)
	tickl 	= 100
	tickn 	= 0
	x_ofs	= 500
	y_ofs	= 50
	am_coef = 120

	screen.fill(black)
	pygame.display.update()

	# Store unique channels to draw with different colors
	ch0 = []
	ch1 = []
	ch2 = []
	ch3 = []

	# Each slice contains the 4 channels
	for capture_slice in data:
		ch0.append((tickl*tickn + x_ofs, am_coef*float(capture_slice['BR'])+y_ofs))
		ch1.append((tickl*tickn + x_ofs, am_coef*float(capture_slice['RD'])+y_ofs+20))
		ch2.append((tickl*tickn + x_ofs, am_coef*float(capture_slice['YW'])+y_ofs+40))
		ch3.append((tickl*tickn + x_ofs, am_coef*float(capture_slice['OR'])+y_ofs+60))
		tickn = tickn + 1
	print(ch0)
	pygame.draw.lines(screen, brown, False, ch0, 2)
	pygame.draw.lines(screen, red, False, ch1, 2)
	pygame.draw.lines(screen, yello, False, ch2, 2)
	pygame.draw.lines(screen, orang, False, ch3, 2)

	while True:
		pygame.display.update()
		time.sleep(5)
