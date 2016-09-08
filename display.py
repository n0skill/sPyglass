import pygame
import time

# Display class to manage adding, removing channels
class Colors:
	black 	= (0,0,0)
	white 	= (255, 255, 255)
	yello	= (255, 125, 0)
	brown	= (100, 50, 30)
	orang	= (250, 255, 0)
	red		= (255, 0, 0)
class Display:
	def __init__(self, name):
		self.name = name

class Channel:
	nb = 0
	height  = 80
	def __init__(self, display, values, color):
		self.ampli = 30
		self.zoom_level = 0
		self.length = len(values)
		self.color = color
		cap_tuples = []

		#Scale x axis
		self.x_scale = (display.get_width()-50)/len(values)
		pygame.font.init()
		font = pygame.font.Font(None, 18)
		self.surface = pygame.Surface((display.get_width(), 80))
		self.surface.fill((100, 100, 100))
		self.lab1 = font.render("ch"+str(Channel.nb), 1, self.color)
		self.surface.blit(self.lab1, (10, Channel.height/2))
		for id, val in enumerate(values):
			cap_tuples.append((id*self.x_scale+40, val*20))
		cap_tuples.append((len(values)*self.x_scale+40, val*20))
		pygame.draw.lines(self.surface, self.color, False, cap_tuples, 2)
		display.blit(self.surface, (0, Channel.nb*Channel.height))
		pygame.display.update()
		Channel.nb = Channel.nb+1

	def show_capture(values):
		pygame.draw.lines(self, brown, False, values, 2)

def channel_graph(screen, chanel_data):
	chanel_rect = pygame.Surface()
def disp(data):
	screen	= pygame.display.set_mode((1024,768))
	screen.fill(Colors.black)
	pygame.display.update()
	# Store unique channels to draw with different colors
	ch0 = []
	ch1 = []
	ch2 = []
	ch3 = []

	# Each slice of time contains the 4 channels
	for capture_slice in data:
		ch0.append(float(capture_slice['BR']))
		ch1.append(float(capture_slice['RD']))
		ch2.append(float(capture_slice['YW']))
		ch3.append(float(capture_slice['OR']))
	Channel(screen, ch0, Colors.brown)
	Channel(screen, ch1, Colors.red)
	Channel(screen, ch2, Colors.yello)
	Channel(screen, ch3, Colors.orang)
	while True:
		pygame.display.update()
		time.sleep(5)
