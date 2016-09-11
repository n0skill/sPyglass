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
	darkgrey= (20, 20, 20)
	green	= (0, 200, 30)

# TODO: implement textbox as a subclass of Box
class Box:
	def __init__(self, size, position, color=Colors.white, text=""):
		self.surface 	= pygame.Surface(size)
		print('sz ', size)
		print('pos', position)
		self.text 		= text
		self.pos		= position
		self.size		= size

		self.cursor_pos = (0, self.size[1]/2)
		self.focus		= False
		self.color		= color
		pygame.font.init()
		self.font 	= pygame.font.Font(None, 30)
		self.surface.fill(color)
	def action(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = event.pos
				if event.button == 1:
					if self.pos[0]+self.size[0] > pos[0] > self.pos[0] and self.pos[1]+self.size[1] > pos[1] > self.pos[1]:
						self.focus=True
					else:
						self.focus=False
			if event.type == pygame.KEYDOWN and self.focus is True:
				if event.key < 207:
					if event.unicode == '\b':
						self.text = self.text[:-1]
					else:
						self.text += event.unicode
				self.surface.fill(self.color)
				text_render = self.font.render(self.text, 1,
					(255-self.color[0], 255-self.color[1], 255-self.color[2]))
				self.surface.blit(text_render, self.cursor_pos)

class Console(Box):
	def __init__(self, size, pos):
		Box.__init__(self, size, pos, Colors.black)
		self.font 	= pygame.font.Font(None, 20)
		self.line_h	= 12
		self.color 	= Colors.black
		self.cursor_pos = (20,20)

	def action(self, events):
		super(Console, self).action(events)
		for event in events:
			if event.type == pygame.KEYDOWN and self.focus is True:
				cmd = []
				value = ""
				if event.unicode == '\r':
					self.text=self.text[:-1]
					cmd.append(self.text)
					value = busPirate.send_cmd('/dev/ttyUSB0', cmd)
					self.text=""

				if len(value) > 1:
					lines = value.split('\r\n')
					savex = self.cursor_pos[0]
					self.surface.fill(self.color)
					for line in lines:
						self.nb_ln= self.nb_ln+1
						tabs = line.split('\t')
						for tab in tabs:
							label_l = self.font.render(tab, 1, Colors.green)
							self.surface.blit(label_l, self.cursor_pos)
							self.cursor_pos = (self.cursor_pos[0]+120, self.nb_ln*self.line_h)
						self.cursor_pos = (savex, self.cursor_pos[1])
				self.nb_ln = 1
				self.cursor_pos = (self.cursor_pos[0], self.nb_ln*self.line_h)
			if len(self.text) > 0:
				inp = self.font.render(self.text, 1, Colors.green)
				self.surface.fill(Colors.black)
				self.surface.blit(inp, self.cursor_pos)
			pygame.display.update()

class Channel:
	nb = 0
	height  = 80
	zoom_level=1
	channels = []
	def __init__(self, display, values, color, unit):
		self.margin_l = 100
		self.length = len(values)
		self.height = 80
		self.color = color
		self.unit = unit
		self.values = values
		self.display = display

		# Scale x and y axis
		self.x_scale = (self.display.get_width()-self.margin_l)/self.length
		self.max = max(self.values, key=lambda y: y[1])[1]
		self.min = min(self.values, key=lambda y: y[1])[1]

		self.surf = pygame.Surface((display.get_width(), self.height))
		self.surf.fill((25, 25, 25))
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
		self.surf.blit(self.timescale, (self.display.get_width()-20, 10))
		self.surf.blit(self.lab1, (40, Channel.height/2))
		self.surf.blit(labelmax, (self.margin_l-30, 10))
		self.surf.blit(labelmin, (self.margin_l-30, 70))
		self.display.blit(self.surf, (0, self.nb*self.height))
	def draw_scale(self):
		scale = self.x_scale*Channel.zoom_level
		font = self.font
		color = Colors.green
		surface = self.surf
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
		self.surf.fill((25,25,25))
		self.draw_scale()
		self.draw_labels()
		for tup in self.values:
			x_scaled = tup[0]*scale
			y_scaled = (tup[1]-self.min)/((self.max-self.min)+0.01)*(self.height-20)
			scaled_vals.append((x_scaled+self.margin_l, y_scaled+10))
		pygame.draw.aalines(self.surf, self.color, False, scaled_vals, 2)
		self.display.blit(self.surf, (0, self.nb*self.height))
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
def zoomOut():
	Channel.reset()
	if Channel.zoom_level > 0.3:
		Channel.zoom_level=Channel.zoom_level-0.3
		for chan in Channel.channels:
			chan.plot()
	else:
		pass

# Source: https://pythonprogramming.net/pygame-button-function-events/
def button(evs, disp, x_pos, y_pos, w, h, text, arg, arg2, action=None):
	mouse = pygame.mouse.get_pos()
	pos = (0,0)
	for event in evs:
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			if event.button == 1:
				if x_pos+w > pos[0] > x_pos and y_pos+h > pos[1] > y_pos:
					pygame.draw.rect(disp, Colors.yello,(x_pos,y_pos,w,h))
					pygame.display.update()
					action(arg, arg2)

	pygame.font.init()
	font = pygame.font.Font(None, 30)
	label = font.render(text, 1, Colors.black)
	pygame.draw.rect(disp, Colors.grey ,(x_pos,y_pos,w,h))
	disp.blit(label, (x_pos+20, y_pos+10))

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

def plot_capture(screen, time):
	channels = Channel.channels
	Channel.reset()
	if time is "":
		time = 10
	else:
		time = int(time)
	capt = busPirate.capture_voltage('/dev/ttyUSB0',time)
	surf = pygame.Surface((screen.get_width(), 50))
	for k, chan in enumerate(capt.channels):
		color = channels[k].color
		Channel(screen, capt.channels[chan], color, "ms")
	Channel.plotall()

def disp():
	connected = busPirate.isConnected()
	screen	= pygame.display.set_mode((1024,768))
	screen.fill(Colors.darkgrey)
	disp_default_chans(screen)
	if connected:
		tb = Console((screen.get_width(), 350), (0, 350))
		bx = Box((80, 40), (700, 720))
		pygame.display.update()
		while True:
			evts = pygame.event.get()
			button(evts, screen, screen.get_width()-120, 720, 120, 40, 'capture', screen, bx.text, plot_capture)
			tb.action(evts)
			bx.action(evts)
			screen.blit(bx.surface, bx.pos)
			screen.blit(tb.surface, tb.pos)
			mouse_action_trigger(evts, 4, zoomIn)
			mouse_action_trigger(evts, 5, zoomOut)
			pygame.display.update()
			time.sleep(0.01)
	else:
		print('No bus priate found. Try again !')
