import pygame
import time
import busPirate

# Display class to manage adding, removing channels
class Colors:
	black 	= (0,0,0)
	white 	= (255, 255, 255)
	yello	= (255, 125, 0)
	brown	= (100, 50, 30)
	orang	= (250, 255, 0)
	red		= (255, 0, 0)
	grey	= (125, 125, 125)
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
			cap_tuples.append((id*self.x_scale+40, val*10))
		cap_tuples.append((len(values)*self.x_scale+40, val*10))
		pygame.draw.lines(self.surface, self.color, False, cap_tuples, 2)
		display.blit(self.surface, (0, Channel.nb*Channel.height))
		pygame.display.update()
		Channel.nb = Channel.nb+1

	def show_capture(values):
		pygame.draw.lines(self, brown, False, values, 2)
	def reset():
		Channel.nb = 0

def channel_graph(screen, chanel_data):
	chanel_rect = pygame.Surface()

# Source: https://pythonprogramming.net/pygame-button-function-events/
def button(disp, x_pos, y_pos, width, height, text, arg, action=None):
	evs = pygame.event.get()
	pos = (0,0)
	for event in evs:
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
	mouse = pygame.mouse.get_pos()
	if x_pos+width > pos[0] > x_pos and y_pos+height > pos[1] > y_pos:
		pygame.draw.rect(disp, Colors.yello,(x_pos,y_pos,width,height))
		action(arg)

	pygame.font.init()
	font = pygame.font.Font(None, 18)
	label = font.render(text, 1, Colors.black)
	pygame.draw.rect(disp, Colors.grey ,(x_pos,y_pos,width,height))
	disp.blit(label, (x_pos, y_pos))

def plot_capture(screen):
	screen.fill(Colors.black)
	Channel.reset()
	pygame.display.update()
	ch0 = []
	ch1 = []
	ch2 = []
	ch3 = []
	capture = busPirate.capture_voltage()
	for capture_slice in capture:
		ch0.append(float(capture_slice['BR']))
		ch1.append(float(capture_slice['RD']))
		ch2.append(float(capture_slice['YW']))
		ch3.append(float(capture_slice['OR']))
	Channel(screen, ch0, Colors.brown)
	Channel(screen, ch1, Colors.red)
	Channel(screen, ch2, Colors.yello)
	Channel(screen, ch3, Colors.orang)

def disp():
	screen	= pygame.display.set_mode((1024,768))
	screen.fill(Colors.black)
	pygame.display.update()
	while True:
		button(screen, 60, 750, 120, 40, 'capture', screen, plot_capture)
		pygame.display.update()
		time.sleep(0.01)
