import pygame
import time
import busPirate

screen	= pygame.display.set_mode((1024,768))

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

class Box:
	""" Class for displaying simple input textboxes """
	def __init__(self, size, position, color=Colors.white, label=""):
		self.surface 	= pygame.Surface(size)
		self.text 		= ""
		self.label 		= label
		self.pos		= position
		self.size		= size
		self.cursor_pos = (0, self.size[1]/4)
		self.focus		= False
		self.color		= color
		self.surface.fill(color)
		pygame.font.init()
		self.font 	= pygame.font.SysFont("inconsolata", 18)
		self.draw_label()
		screen.blit(self.surface, self.pos)
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
				text_render = self.font.render(self.text, True, Colors.black)
				self.surface.blit(text_render, (self.cursor_pos[0], self.cursor_pos[1]))
				screen.blit(self.surface, self.pos)
	def draw_label(self):
		label_surf = pygame.Surface((60, 10), pygame.SRCALPHA, 32)
		label_surf.convert_alpha()
		font = pygame.font.SysFont('Inconsolata', 10)
		text_l = font.render(self.label, 1, Colors.green)
		label_surf.blit(text_l, (0,0))
		screen.blit(label_surf, (self.pos[0], self.pos[1]-self.size[1]/2))
		pygame.display.update()

class Console(Box):
	""" Console class: Displays a command line interface
	 	and sends the values to the serial port """
	def __init__(self, size, pos):
		Box.__init__(self, size, pos, Colors.black)
		self.font 	= pygame.font.SysFont("inconsolata", 20)
		self.line_h	= 18
		self.color 	= Colors.black
		self.cursor_pos = (20,20)
		self.nb_ln = 1

	# Don't draw labels on console objects
	def draw_label(self):
		super(Console, self).draw_label
		return None

	def action(self, events):
		super(Console, self).action(events)
		for event in events:
			if event.type == pygame.KEYDOWN and self.focus is True:
				cmd = ""
				value = ""
				if event.unicode == '\r':
					self.text=self.text[:-1]
					cmd = cmd+self.text
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
							self.cursor_pos = (self.cursor_pos[0]+80, self.nb_ln*self.line_h)
						self.cursor_pos = (savex, self.cursor_pos[1])
				self.nb_ln = 1
				self.cursor_pos = (self.cursor_pos[0], self.nb_ln*self.line_h)
			if len(self.text) > 0:
				inp = self.font.render(self.text, 1, Colors.green)
				self.surface.fill(Colors.black)
				self.surface.blit(inp, self.cursor_pos)
			pygame.display.update()

class Channel:
	"""	Class to display separate channel captures"""
	nb = 0
	height  = 80
	margin_top = 50
	zoom_level=1
	channels = []
	def __init__(self, display, values, color, unit):
		self.margin_l	= 100
		self.length		= len(values)
		self.height 	= 80
		self.color 		= color
		self.unit 		= unit
		self.values 	= values
		self.display 	= display
		self.width		= display.get_width()
		self.surf = pygame.Surface((self.width, self.height))
		self.surf.fill((25, 25, 25))
		self.nb = Channel.nb

		# Scale x and y axis
		self.x_scale = (self.width-self.margin_l)/self.length+1
		self.max = max(self.values, key=lambda y: y[1])[1]
		self.min = min(self.values, key=lambda y: y[1])[1]

		pygame.font.init()
		self.font = pygame.font.Font(None, 16)
		self.draw_scale()
		self.draw_labels()
		#pygame.display.update()
		Channel.nb = Channel.nb+1
		Channel.channels.append(self)
	def draw_labels(self):
		font = self.font
		labelmax	= font.render(str(self.max), 1, self.color)
		labelmin 	= font.render(str(self.min), 1, self.color)
		labelch 	= font.render("ch"+str(self.nb), 1, self.color)
		timescale 	= font.render(str(self.length), 1, self.color)
		self.surf.blit(timescale, (self.display.get_width()-20, 10))
		self.surf.blit(labelch, (40, Channel.height/2))
		self.surf.blit(labelmax, (self.margin_l-30, 10))
		self.surf.blit(labelmin, (self.margin_l-30, 70))
		self.display.blit(self.surf, (0, self.nb*self.height+Channel.margin_top))
	def draw_scale(self):
		scale_surface = pygame.Surface((self.width, 5))
		scale_surface.fill(Colors.grey)
		pygame.draw.line(scale_surface, Colors.green, (self.margin_l, 3), (self.width, 3), 1)
		for i in range(0, self.length):
			if i%10==0:
				timelbl 	= self.font.render(str(i), 1, self.color)
				time_unit 	= self.font.render(self.unit, 1, self.color)
				self.surf.blit(time_unit, (self.margin_l-25, -2))
				self.surf.blit(timelbl, (i*scale_+self.margin_l-2, 6))
				pygame.draw.line(scale_surface, self.color, (i*scale+self.margin_l, 0), (i*scale+self.margin_l, 4), 1)
		self.surf.blit(scale_surface, (0,0))

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
			scaled_vals.append((x_scaled+self.margin_l, y_scaled+15))
		pygame.draw.aalines(self.surf, self.color, False, scaled_vals, 2)
		self.display.blit(self.surf, (0, self.nb*self.height+Channel.margin_top))
		pygame.display.update()
	def plotall():
		for chan in Channel.channels:
			chan.plot()
	def reset():
		Channel.nb = 0
		Channel.channels = []

class Button():
	"""Class to create buttons for the GUI"""
	def __init__(self, text, position):
		self.x_pos 	= position[0]
		self.y_pos 	= position[1]
		self.w		= 80
		self.h		= 25
		self.font	= pygame.font.SysFont('inconsolata', 20)
		font = self.font.render(text, 1, Colors.black)
		self.surface = pygame.Surface((self.w, self.h))
		self.surface.fill(Colors.grey)
		self.surface.blit(font, (0,0))
		screen.blit(self.surface, position)

	def action(self, events, action, inputs=None):
		x 	= self.x_pos
		y 	= self.y_pos
		w 	= self.w
		h	= self.h
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				evtpos = pygame.mouse.get_pos()
				if x+w > evtpos[0] > x and y+h > evtpos[1] > y:
					if inputs == None:
						action()
					else:
						action(inputs)

# TODO: put these in the Channel class. Not out of it.
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
	print('Default channels displayed')

def capture_and_plot(inputs):
	channels = Channel.channels
	Channel.reset()
	capt = busPirate.capture_voltage(int(inputs[1]), '/dev/ttyUSB0',int(inputs[0]))
	surf = pygame.Surface((screen.get_width(), 50))
	for k, chan in enumerate(capt.channels):
		color = channels[k].color
		Channel(screen, capt.channels[chan], color, "ms")
	Channel.plotall()

def reset():
	screen.fill(Colors.darkgrey)

def disp_unconnected():
	reset()
	disp_default_chans(screen)

def display():
	reset()
	disp_default_chans(screen)
	bx_nb_capture 	= Box((70, 25), (650, 20), Colors.white, "Nb of V capt.")
	bx_wait_time  	= Box((70, 25), (750, 20), Colors.white, "Delay [ms]")
	btn_capture   	= Button("Capture", (screen.get_width()-80, 20))
	btn_export		= Button("Export", (30, 20))
	tb = Console((screen.get_width(), 350), (0, 400))
	while True:
		evts = pygame.event.get()
		tb.action(evts)
		bx_nb_capture.action(evts)
		bx_wait_time.action(evts)
		btn_capture.action(evts, capture_and_plot, [bx_nb_capture.text, bx_wait_time.text])
		btn_export.action(evts, busPirate.export, None)
		screen.blit(tb.surface, tb.pos)
		mouse_action_trigger(evts, 4, zoomIn)
		mouse_action_trigger(evts, 5, zoomOut)
		pygame.display.update()
		time.sleep(0.01)
