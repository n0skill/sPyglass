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
	y_ofs	= 20
	am_coef = 30

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
	pygame.font.init()
	font = pygame.font.Font(None, 18)
	lab1 = font.render("ch1", 1, brown)
	lab2 = font.render("ch2", 1, red)
	lab3 = font.render("ch3", 1, yello)
	lab4 = font.render("ch4", 1, orang)
	screen.blit(lab1, (x_ofs-30, 100))
	screen.blit(lab2, (x_ofs-30, 120))
	screen.blit(lab3, (x_ofs-30, 140))
	screen.blit(lab4, (x_ofs-30, 160))

	pygame.draw.lines(screen, brown, False, ch0, 2)
	pygame.draw.lines(screen, red, False, ch1, 2)
	pygame.draw.lines(screen, yello, False, ch2, 2)
	pygame.draw.lines(screen, orang, False, ch3, 2)

	while True:
		pygame.display.update()
		time.sleep(5)
