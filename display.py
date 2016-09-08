import pygame
import time

# Display class to manage adding, removing channels
class Colors:
	black 	= (0,0,0)
	white 	= (255, 255, 255)
	yello	= (255, 125, 0)
	brown	= (125, 125, 50)
	orang	= (250, 255, 0)
	red		= (255, 0, 0)
class Display:
	def __init__(self, name):
		self.name = name

class Channel:
	chan_nb = 0
	chan_h  = 80
	def __init__(self, display, values):
		pygame.font.init()
		font = pygame.font.Font(None, 18)
		self.lab1 = font.render("ch1", 1, Colors.brown)
		self.surface = pygame.Surface((display.get_width(), 80))
		self.surface.fill((100, 100, 100))
		display.blit(self.lab1, (0, (Channel.chan_nb*Channel.chan_h)+Channel.chan_nb*10))
		display.blit(self.surface, (0, Channel.chan_nb*Channel.chan_h+Channel.chan_nb*20))
		pygame.draw.lines(display, Colors.brown, False, values, 2)
		Channel.chan_nb = Channel.chan_nb+1

	def show_capture(values):
		pygame.draw.lines(self, brown, False, values, 2)

def channel_graph(screen, chanel_data):
	chanel_rect = pygame.Surface()
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

	# Each slice of time contains the 4 channels
	for capture_slice in data:
		ch0.append((tickl*tickn, float(capture_slice['BR'])))
		ch1.append((tickl*tickn, float(capture_slice['RD'])))
		ch2.append((tickl*tickn, float(capture_slice['YW'])))
		ch3.append((tickl*tickn, float(capture_slice['OR'])))
		tickn = tickn + 1

	Channel(screen, ch0)
	Channel(screen, ch1)
	Channel(screen, ch2)
	Channel(screen, ch3)

	#pygame.draw.lines(screen, brown, False, ch0, 2)
	#pygame.draw.lines(screen, red, False, ch1, 2)
	#pygame.draw.lines(screen, yello, False, ch2, 2)
	#pygame.draw.lines(screen, orang, False, ch3, 2)
	while True:
		pygame.display.update()
		time.sleep(5)
