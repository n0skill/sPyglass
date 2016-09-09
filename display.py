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
	def __init__(self, display, values, color, unit):
		margin_l = 100
		self.ampli = 30
		self.zoom_level = 0
		self.length = len(values)
		self.height = 80
		self.color = color
		self.unit = unit
		self.values = values
		self.display = display
		cap_tuples = []

		# Scale x axis
		self.x_scale = (self.display.get_width()-margin_l)/self.length
		self.max = max(values)
		self.min = min(values)

		self.surface = pygame.Surface((display.get_width(), self.height))
		self.surface.fill((25, 25, 25))

		# Add scale to axises
		pygame.draw.line(self.surface, self.color, (margin_l, 2), (self.display.get_width(), 2), 1)
		for i in range(0, self.length):
			if i%5 == 0:
				pygame.draw.line(self.surface, self.color, (i*self.x_scale+margin_l, 0), (i*self.x_scale+margin_l, 4), 1)
		# Add labels to axises
		pygame.font.init()
		font = pygame.font.Font(None, 18)
		self.lab1 = font.render("ch"+str(Channel.nb), 1, self.color)
		self.timescale = font.render(str(self.length), 1, self.color)
		self.surface.blit(self.timescale, (self.display.get_width()-20, 10))
		self.surface.blit(self.lab1, (10, Channel.height/2))

		# Create tuples of (x, y) positions
		for id, val in enumerate(values):
			scaled_val = (val-min(values))/(max(values)-min(values)+0.01)
			cap_tuples.append((id*self.x_scale+100, ((self.height-10)*scaled_val)))
			if id > 1:
				pygame.draw.lines(self.surface, self.color, False, cap_tuples, 2)
				display.blit(self.surface, (0, Channel.nb*Channel.height))
				pygame.display.update()
				time.sleep(0.01)

		# FIXME: invert line
		#pygame.draw.lines(self.surface, self.color, False, cap_tuples, 2)
		self.display.blit(self.surface, (0, Channel.nb*Channel.height))
		pygame.display.update()
		Channel.nb = Channel.nb+1

	def show_capture(self):
		cap_tuples = []
		print('showing !')
		for id, val in enumerate(self.values):
			scaled_val = (val-min(self.values))/(max(self.values)-min(self.values)+0.01)
			cap_tuples.append((id*self.x_scale+100, ((self.height-10)*scaled_val)))
		self.display.blit(self.surface, (0, Channel.nb*Channel.height))
		pygame.display.update()
	def reset():
		Channel.nb = 0

def channel_graph(screen, chanel_data):
	chanel_rect = pygame.Surface()

# Source: https://pythonprogramming.net/pygame-button-function-events/
def button(disp, x_pos, y_pos, width, height, text, arg, action=None):
	evs = pygame.event.get()
	mouse = pygame.mouse.get_pos()
	pos = (0,0)
	for event in evs:
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
	if x_pos+width > pos[0] > x_pos and y_pos+height > pos[1] > y_pos:
		pygame.draw.rect(disp, Colors.yello,(x_pos,y_pos,width,height))
		action(arg)

	pygame.font.init()
	font = pygame.font.Font(None, 18)
	label = font.render(text, 1, Colors.black)
	pygame.draw.rect(disp, Colors.grey ,(x_pos,y_pos,width,height))
	disp.blit(label, (x_pos, y_pos))


def disp_default_chans(screen):
	''' Creates empty channels to display before any capture is made'''
	Channel(screen, [0], Colors.brown, "ms")
	Channel(screen, [0], Colors.red, "ms")
	Channel(screen, [0], Colors.yello, "ms")
	Channel(screen, [0], Colors.orang, "ms")

def plot_capture(screen):
	Channel.reset()
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
	Channel(screen, ch0, Colors.brown, "ms")
	Channel(screen, ch1, Colors.red, "ms")
	Channel(screen, ch2, Colors.yello, "ms")
	Channel(screen, ch3, Colors.orang, "ms")
	#ch0.show_capture()
	#ch1.show_capture()
def disp():
	screen	= pygame.display.set_mode((1024,768))
	screen.fill(Colors.black)
	disp_default_chans(screen)
	pygame.display.update()
	while True:
		button(screen, 60, 750, 120, 40, 'capture', screen, plot_capture)
		pygame.display.update()
		time.sleep(0.01)
