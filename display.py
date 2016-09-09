import pygame
import time
import busPirate

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
		self.nb = Channel.nb
		cap_tuples = []

		# Scale x axis
		self.x_scale = (self.display.get_width()-margin_l)/self.length
		self.max = max(values)
		self.min = min(values)

		self.surface = pygame.Surface((display.get_width(), self.height))
		self.surface.fill((25, 25, 25))
		self.nb = Channel.nb
		Channel.nb = Channel.nb+1

	def plot(self):
		margin_l = 100
		# Add scale to axises
		pygame.draw.line(self.surface, self.color, (margin_l, 2), (self.display.get_width(), 2), 1)
		for i in range(0, self.length):
			if i%5 == 0:
				pygame.draw.line(self.surface, self.color, (i*self.x_scale+margin_l, 0), (i*self.x_scale+margin_l, 4), 1)
		# Add labels to axises
		pygame.font.init()
		font = pygame.font.Font(None, 18)
		labelmax = font.render(str(self.max), 1, self.color)
		labelmin = font.render(str(self.min), 1, self.color)
		self.lab1 = font.render("ch"+str(Channel.nb), 1, self.color)
		self.timescale = font.render(str(self.length), 1, self.color)
		self.surface.blit(self.timescale, (self.display.get_width()-20, 10))
		self.surface.blit(self.lab1, (10, Channel.height/2))
		self.surface.blit(labelmax, (margin_l, 10))
		self.surface.blit(labelmin, (margin_l, 70))

		# FIXME: invert line
		#pygame.draw.lines(self.surface, self.color, False, cap_tuples, 2)
		self.display.blit(self.surface, (0, self.nb*Channel.height))
		cap_tuples = []
		for id, val in enumerate(self.values):
			scaled_val = (val-min(self.values))/(max(self.values)-min(self.values)+0.01)
			cap_tuples.append((id*self.x_scale+100, ((self.height-10)*scaled_val)))
			if id > 1:
				pygame.draw.lines(self.surface, self.color, False, cap_tuples, 2)
				self.display.blit(self.surface, (0, self.nb*Channel.height))
				pygame.display.update()
				time.sleep(0.01)

		pygame.draw.lines(self.surface, self.color, False, cap_tuples, 2)
		self.display.blit(self.surface, (0, self.nb*Channel.height))
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
	Channel.reset()
	''' Creates empty channels to display before any capture is made'''
	Channel(screen, [0,0], Colors.brown, 	"ms").plot()
	Channel(screen, [0,0], Colors.red, 	"ms").plot()
	Channel(screen, [0,0], Colors.yello, 	"ms").plot()
	Channel(screen, [0,0], Colors.orang, 	"ms").plot()
	pygame.display.update()

def plot_capture(screen):
	Channel.reset()
	#Capture
	vals_ch0 = []
	vals_ch1 = []
	vals_ch2 = []
	vals_ch3 = []
	capture = busPirate.capture_voltage()
	for capture_slice in capture:
		vals_ch0.append(float(capture_slice['BR']))
		vals_ch1.append(float(capture_slice['RD']))
		vals_ch2.append(float(capture_slice['YW']))
		vals_ch3.append(float(capture_slice['OR']))
	Channel(screen, vals_ch0, Colors.brown,	"ms").plot()
	Channel(screen, vals_ch1, Colors.red, 	"ms").plot()
	Channel(screen, vals_ch2, Colors.yello,	"ms").plot()
	Channel(screen, vals_ch3, Colors.orang,	"ms").plot()

def disp():
	screen	= pygame.display.set_mode((1024,768))
	screen.fill(Colors.black)
	disp_default_chans(screen)
	pygame.display.update()
	while True:
		button(screen, 60, 750, 120, 40, 'capture', screen, plot_capture)
		pygame.display.update()
		time.sleep(0.01)
