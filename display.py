import pygame
import time
import busPirate
import bp_SPI

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
				if event.unicode == '[' or event.unicode == ']':
					self.text += event.unicode
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
	def __init__(self, values, color, unit):
		self.margin_l	= 100
		self.length		= len(values)
		self.height 	= 50
		self.color 		= color
		self.unit 		= unit
		self.values 	= values
		self.width		= screen.get_width()
		self.surf 		= pygame.Surface((self.width, self.height))
		self.nb = Channel.nb
		self.surf.fill((25, 25, 25))

		# Scale x and y axis
		self.x_scale = (self.width-self.margin_l)/(self.length+1)
		if len(self.values) > 0:
			self.max = max(self.values, key=lambda y: y[1])[1]
			self.min = min(self.values, key=lambda y: y[1])[1]

		pygame.font.init()
		self.font = pygame.font.Font(None, 16)
		self.draw_scale()
		self.draw_labels()
		Channel.nb = Channel.nb+1
		Channel.channels.append(self)
	def draw_labels(self):
		if len(self.values) > 0:
			labelmax	= self.font.render(str(self.max), 1, self.color)
			labelmin 	= self.font.render(str(self.min), 1, self.color)
			labelch 	= self.font.render("ch"+str(self.nb), 1, self.color)
			timescale 	= self.font.render(str(self.length), 1, self.color)
			self.surf.blit(timescale, (screen.get_width()-50, 10))
			self.surf.blit(labelch, (10, Channel.height/2-20))
			self.surf.blit(labelmax, (self.margin_l-20, 10))
			self.surf.blit(labelmin, (self.margin_l-20, 30))
			screen.blit(self.surf, (0, self.nb*self.height+Channel.margin_top))

	def draw_scale(self):
		scale_surface = pygame.Surface((self.width, 5))
		scale_scale   = self.x_scale*Channel.zoom_level
		pygame.draw.line(scale_surface, Colors.green, (0, 3), (self.width, 3), 1)
		for i in range(0, self.length):
			if i%5==0:
				timelbl 	= self.font.render(str(i), 1, self.color)
				time_unit 	= self.font.render(self.unit, 1, self.color)
				self.surf.blit(time_unit, (self.margin_l-25, -2))
				self.surf.blit(timelbl, (i*scale_scale+self.margin_l-2, 6))
				dash_pos = i*scale_scale
				pygame.draw.line(scale_surface, self.color, (dash_pos, 0), (dash_pos, 4), 1)
		self.surf.blit(scale_surface, (self.margin_l,0))

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
		if len(scaled_vals) > 0:
			pygame.draw.aalines(self.surf, self.color, False, scaled_vals, 2)
			screen.blit(self.surf, (0, self.nb*self.height+Channel.margin_top))
		pygame.display.update()
	def plotall():
		pygame.display.update()
		for chan in Channel.channels:
			chan.plot()
	def reset():
		Channel.nb = 0
		Channel.channels = []
		surface = pygame.Surface((screen.get_width(), 200))
		surface.fill((25,25,25))

		screen.blit(surface, (0, Channel.margin_top))
		Channel.plotall()

class Button():
	"""Class to create buttons for the GUI"""
	btn_lst = []
	def __init__(self, text, position, func, args=None, size=(70, 25)):
		self.font	= pygame.font.SysFont('inconsolata', 20)
		self.x_pos 	= position[0]
		self.y_pos 	= position[1]
		self.text 	= text
		self.size 	= size
		self.func 	= func
		self.args	= args

		self.surface = pygame.Surface(self.size)
		font = self.font.render(text, 1, Colors.black)

		self.surface.fill(Colors.grey)
		self.surface.blit(font, (0,0))
		screen.blit(self.surface, position)
		Button.btn_lst.append(self)

	def action(self, events, dynamic_args):
		x 	= self.x_pos
		y 	= self.y_pos
		w 	= self.size[0]
		h	= self.size[1]
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				evtpos = pygame.mouse.get_pos()
				if x+w > evtpos[0] > x and y+h > evtpos[1] > y:
					if self.args == None:
						if dynamic_args==None:
							return self.func()
						else:
							return self.func(dynamic_args)
					else:
						return self.func(self.args)
				else:
					return False
	def all_btn_actions(events):
		for btn in btn_lst:
			btn.action()

class ModeBtn(Button):
	def __init__(self, text, mode, position, func, args=None, size=(70, 25)):
		Button.__init__(self, text, position, func, args)
	def action(self, mode, evts, dynamic_args=None):
		return Button.action(self, evts, dynamic_args)


# TODO: put these in the Channel class. Not out of it.
def zoomIn():
	Channel.zoom_level=Channel.zoom_level+0.3
	Channel.plotall()
def zoomOut():
	if Channel.zoom_level > 0.3:
		Channel.zoom_level=Channel.zoom_level-0.3
		Channel.plotall()
	else:
		Channel.zoom_level=1
		pass

def mouse_action_trigger(events, mouse_btn_no, action=None):
	mouse = pygame.mouse.get_pos()
	for evt in events:
		if evt.type == pygame.MOUSEBUTTONDOWN:
			if evt.button == mouse_btn_no:
				action()

def disp_default_chans():
	''' Creates empty channels to display before any capture is made'''
	Channel.reset()
	Channel([], Colors.brown,"ms")
	Channel([], Colors.red, 	"ms")
	Channel([], Colors.yello,"ms")
	Channel([], Colors.orang,"ms")
	pygame.display.update()
	print('Default channels displayed')

def show_spi_opts(bp):
	Channel.reset()

	ch_SCLK = Channel([], Colors.red, "ms")
	ch_MOSI = Channel([], Colors.red, "ms")
	ch_MOSI = Channel([], Colors.red, "ms")
	ch_MOSI = Channel([], Colors.red, "ms")

	btn_sniff_CSH = 	ModeBtn("CSH", "", (100, 260), bp.spi_sniff_csh)
	btn_sniff_CSL = 	ModeBtn("CSL", "", (10, 260), bp.spi_sniff_csl)
	btn_bulk_transfer = ModeBtn("TRSFR", "", (200, 260), bp.spi_transfer)
	btn_spi_speed = 	ModeBtn("Speed", "", (300, 260), bp.spi_speed)
	btn_write_read = 	ModeBtn("WR", "", (400, 260), bp.spi_write_read)

def capture_and_plot(inputs):
	nb_cap = int(inputs[0])
	wait_c = int(inputs[1])
	bp_obj = inputs[2]
	channels = Channel.channels
	Channel.reset()
	capt = bp_obj.capture_voltage(wait_c, nb_cap)
	surf = pygame.Surface((screen.get_width(), 50))
	for k, chan in enumerate(capt.channels):
		color = channels[k].color
		Channel(capt.channels[chan], color, "ms")
	Channel.plotall()
	pygame.display.update()
def reset():
	screen.fill(Colors.darkgrey)

def disp_test(text, position, surface):
	pygame.font.init()
	font = pygame.font.SysFont('inconsolata', 25)
	text_render = font.render(text, True, color)
	surface.blit(text_render, position)

def get_events():
	return pygame.event.get()

def display(bp):
	disp_default_chans()
	tb 				= Console((screen.get_width(), 350), (0, 400))
	bx_nb_capture 	= Box((70, 25), (650, 20), Colors.white, "Nb of V capt.")
	bx_wait_time  	= Box((70, 25), (750, 20), Colors.white, "Delay [ms]")
	btn_capture   	= Button("Capture", (screen.get_width()-80, 20), capture_and_plot)
	btn_export		= Button("Export", 	(20, 20),  busPirate.export)
	btn_binarymode  = ModeBtn("Binary", "", (120, 20), bp.bitbang)
	btn_bin_spi  	= ModeBtn("SPI",	"SPI", (200, 20), bp.enter_spi)
	btn_bin_i2c  	= ModeBtn("I2C", 	"I2C", (360, 20), bp.enter_spi)
	while True:
		if bp.connected:
			evts = get_events()
			tb.action(evts)
			bx_wait_time.action(evts)
			btn_capture.action(evts, [bx_nb_capture.text, bx_wait_time.text, bp])
			btn_binarymode.action(bp.mode, evts) # This calls self.aciton() not action()
			if btn_bin_spi.action(bp.mode, evts):
				show_spi_opts(bp)
			btn_bin_i2c.action(bp.mode, evts)
			mouse_action_trigger(evts, 4, zoomIn)
			mouse_action_trigger(evts, 5, zoomOut)
			bx_nb_capture.action(evts)
			btn_export.action(evts, busPirate.export)
			screen.blit(tb.surface, tb.pos)
		else:
			print('No buspirate found. Check again')
			bp.isConnected()
		pygame.display.update()
		time.sleep(0.01)

def not_connected(bp):
	print(bp)
	pygame.font.init()
	font	= pygame.font.SysFont('inconsolata', 25)
	txt_not_connected = "Not connected"
	text_render = font.render(txt_not_connected, True, Colors.grey)
	surface = pygame.Surface((screen.get_width(), screen.get_height()))
	surface.fill(Colors.darkgrey)
	surface.blit(text_render, (screen.get_width()/2-50, screen.get_height()/2))
	screen.blit(surface, (0,0))
	pygame.display.update()
	while True:
		time.sleep(0.5)
		bp.isConnected()
