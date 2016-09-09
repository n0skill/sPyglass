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
		self.margin_l = 100
		self.ampli = 30
		self.zoom_level = 0
		self.length = len(values)
		self.height = 80
		self.color = color
		self.unit = unit
		self.values = values
		self.display = display
		self.nb = Channel.nb
		# Scale x axis
		self.x_scale = (self.display.get_width()-self.margin_l)/self.length
		self.max = max(self.values, key=lambda y: y[1])[1]
		self.min = min(self.values, key=lambda y: y[1])[1]

		self.surface = pygame.Surface((display.get_width(), self.height))
		self.surface.fill((25, 25, 25))
		self.nb = Channel.nb

		pygame.draw.line(self.surface, self.color, (self.margin_l, 2), (self.display.get_width(), 2), 1)
		for i in range(0, self.length):
			if i%5 == 0:
				pygame.draw.line(self.surface, self.color, (i*self.x_scale+self.margin_l, 0), (i*self.x_scale+self.margin_l, 4), 1)

		pygame.font.init()
		font = pygame.font.Font(None, 18)
		labelmax = font.render(str(self.max), 1, self.color)
		labelmin = font.render(str(self.min), 1, self.color)

		self.lab1 = font.render("ch"+str(Channel.nb), 1, self.color)
		self.surface.blit(self.lab1, (40, Channel.height/2))

		self.timescale = font.render(str(self.length), 1, self.color)
		self.surface.blit(self.timescale, (self.display.get_width()-20, 10))

		self.surface.blit(labelmax, (self.margin_l, 10))
		self.surface.blit(labelmin, (self.margin_l, 70))
		self.display.blit(self.surface, (0, self.nb*self.height))
		pygame.display.update()
		Channel.nb = Channel.nb+1

	def plot(self):
		scaled_vals = []
		for tup in self.values:
			x_scaled = tup[0]*self.x_scale
			y_scaled = (tup[1]-self.min)/((self.max-self.min)+0.01)*self.height
			scaled_vals.append((x_scaled+self.margin_l, y_scaled))
		pygame.draw.lines(self.surface, self.color, False, scaled_vals, 2)
		self.display.blit(self.surface, (0, self.nb*self.height))
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
		pygame.display.update()
		action(arg)

	pygame.font.init()
	font = pygame.font.Font(None, 18)
	label = font.render(text, 1, Colors.black)
	pygame.draw.rect(disp, Colors.grey ,(x_pos,y_pos,width,height))
	disp.blit(label, (x_pos, y_pos))

def disp_default_chans(screen):
	Channel.reset()
	''' Creates empty channels to display before any capture is made'''
	Channel(screen, [(0,0),(0,0)], Colors.brown, 	"ms")
	Channel(screen, [(0,0),(0,0)], Colors.red, 		"ms")
	Channel(screen, [(0,0),(0,0)], Colors.yello, 	"ms")
	Channel(screen, [(0,0),(0,0)], Colors.orang, 	"ms")
	pygame.display.update()

def plot_capture(screen):
	Channel.reset()
	#Capture
	vals_ch0 = []
	vals_ch1 = []
	vals_ch2 = []
	vals_ch3 = []
	capture = busPirate.capture_voltage()
	surf = pygame.Surface((screen.get_width(), 50))

	# Create a tuple list for each channel
	for id, capture_slice in enumerate(capture):
		vals_ch0.append((id, float(capture_slice['BR'])))
		vals_ch1.append((id, float(capture_slice['RD'])))
		vals_ch2.append((id, float(capture_slice['YW'])))
		vals_ch3.append((id, float(capture_slice['OR'])))
	# Plot them
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
