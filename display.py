import pygame
import time
import busPirate

class Colors:
	black 	= (0,0,0)
	white 	= (255, 255, 255)
	yello	= (255, 125, 0)
	brown	= (170, 100, 50)
	orang	= (250, 255, 0)
	red		= (255, 0, 0)
	grey	= (125, 125, 125)
	green	= (0, 200, 30)
class Display:
	def __init__(self, name):
		self.name = name

class Channel:
	nb = 0
	height  = 80
	zoom_level=1
	channels = []
	def __init__(self, display, values, color, unit):
		self.margin_l = 100
		self.length = len(values)
		self.height = 90
		self.color = color
		self.unit = unit
		self.values = values
		self.display = display

		# Scale x and y axis
		self.x_scale = (self.display.get_width()-self.margin_l)/self.length
		self.max = max(self.values, key=lambda y: y[1])[1]
		self.min = min(self.values, key=lambda y: y[1])[1]

		self.surface = pygame.Surface((display.get_width(), self.height))
		self.surface.fill((25, 25, 25))
		self.nb = Channel.nb

		pygame.font.init()
		self.font = pygame.font.Font(None, 16)
		self.draw_scale()
		self.draw_labels()
		pygame.display.update()
		Channel.nb = Channel.nb+1
		Channel.channels.append(self)
	def draw_labels(self):
		font = self.font
		labelmax	= font.render(str(self.max), 1, self.color)
		labelmin 	= font.render(str(self.min), 1, self.color)
		self.lab1 	= font.render("ch"+str(self.nb), 1, self.color)
		self.timescale = font.render(str(self.length), 1, self.color)
		self.surface.blit(self.timescale, (self.display.get_width()-20, 10))
		self.surface.blit(self.lab1, (40, Channel.height/2))
		self.surface.blit(labelmax, (self.margin_l-30, 10))
		self.surface.blit(labelmin, (self.margin_l-30, 70))
		self.display.blit(self.surface, (0, self.nb*self.height))
	def draw_scale(self):
		scale = self.x_scale*Channel.zoom_level
		font = self.font
		color = Colors.green
		surface = self.surface
		pygame.draw.line(surface, color, (self.margin_l, 3), (self.display.get_width(), 3), 1)
		for i in range(0, self.length):
			if i%5==0:
				timelbl = font.render(str(i), 1, color)
				time_unit = font.render(self.unit, 1, color)
				surface.blit(time_unit, (self.margin_l-25, -2))
				surface.blit(timelbl, (i*scale+self.margin_l-2, 6))
				pygame.draw.line(surface, color, (i*scale+self.margin_l, 0), (i*scale+self.margin_l, 4), 1)

	def plot(self):
		scaled_vals = []
		scale = self.x_scale*Channel.zoom_level
		font = self.font
		self.surface.fill((25,25,25))
		self.draw_scale()
		self.draw_labels()
		for tup in self.values:
			x_scaled = tup[0]*scale
			y_scaled = (tup[1]-self.min)/((self.max-self.min)+0.01)*(self.height-10)
			scaled_vals.append((x_scaled+self.margin_l, y_scaled+10))
		pygame.draw.aalines(self.surface, self.color, False, scaled_vals, 2)
		self.display.blit(self.surface, (0, self.nb*self.height))
		pygame.display.update()
	def plotall():
		for chan in Channel.channels:
			chan.plot()
	def reset():
		Channel.nb = 0

def zoomIn():
	Channel.reset()
	Channel.zoom_level=Channel.zoom_level+0.3
	for chan in Channel.channels:
		chan.plot()
	pygame.display.update()
def zoomOut():
	Channel.reset()
	if Channel.zoom_level > 0.3:
		Channel.zoom_level=Channel.zoom_level-0.3
		for chan in Channel.channels:
			chan.plot()
	else:
		pass
	pygame.display.update()

# Source: https://pythonprogramming.net/pygame-button-function-events/
def button(evs, disp, x_pos, y_pos, w, h, text, arg, action=None):
	mouse = pygame.mouse.get_pos()
	pos = (0,0)
	for event in evs:
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			if event.button == 1:
				if x_pos+w > pos[0] > x_pos and y_pos+h > pos[1] > y_pos:
					pygame.draw.rect(disp, Colors.yello,(x_pos,y_pos,w,h))
					pygame.display.update()
					action(arg)

	pygame.font.init()
	font = pygame.font.Font(None, 18)
	label = font.render(text, 1, Colors.black)
	pygame.draw.rect(disp, Colors.grey ,(x_pos,y_pos,w,h))
	disp.blit(label, (x_pos, y_pos))

def mouse_action_trigger(events, mouse_btn_no, action=None):
	mouse = pygame.mouse.get_pos()
	for evt in events:
		if evt.type == pygame.MOUSEBUTTONDOWN:
			if evt.button == mouse_btn_no:
				action()

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
	Channel(screen, vals_ch0, Colors.brown,	"ms")
	Channel(screen, vals_ch1, Colors.red, 	"ms")
	Channel(screen, vals_ch2, Colors.yello,	"ms")
	Channel(screen, vals_ch3, Colors.orang,	"ms")
	Channel.plotall()

def disp():
	screen	= pygame.display.set_mode((1024,768))
	screen.fill(Colors.black)
	disp_default_chans(screen)
	pygame.display.update()
	while True:
		evts = pygame.event.get()
		button(evts, screen, 60, 750, 120, 40, 'capture', screen, plot_capture)
		mouse_action_trigger(evts, 4, zoomIn)
		mouse_action_trigger(evts, 5, zoomOut)
		pygame.display.update()
		time.sleep(0.01)
