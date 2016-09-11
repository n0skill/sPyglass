import pygame
import time
import busPirate

class Textbox:
	def __init__(self, name, screen, w, h, x_pos, y_pos, backC=(20,20,20), foreC=(0,0,0)):
		self.focus	= False
		self.h 		= h
		self.w 		= w
		self.x_pos 	= x_pos
		self.y_pos 	= y_pos
		self.cur_x	= 20
		self.cur_y 	= 20
		self.line_h	= 12
		self.col 	= backC
		self.input 	= ""
		self.nb_ln 	= 1
		self.screen = screen
		self.surf 	= pygame.Surface((w,h))

		self.surf.fill(backC)
		pygame.font.init()
		self.font = pygame.font.Font(None, 20)
		screen.blit(self.surf, (x_pos, y_pos))

	def action(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = event.pos
				if event.button == 1:
					if self.x_pos+self.w > pos[0] > self.x_pos and self.y_pos+self.h > pos[1] > self.y_pos:
						self.focus=True
					else:
						self.focus=False
			if event.type == pygame.KEYDOWN and self.focus is True:
				cmd = []
				value = ""
				if event.key < 207:
					print(event.unicode)
					if event.unicode == '\r':
						self.nb_ln=1
						self.cur_x = 20
						cmd.append(self.input)
						value = busPirate.send_cmd('/dev/ttyUSB0', cmd)
						self.input=""
						txt = self.font.render(self.input, 1, Colors.green)
						self.surf.blit(txt, (self.cur_x,self.cur_y))
					elif event.unicode == '\b':
						self.input = self.input[:-1]
					else:
						self.input += event.unicode
				else:
					print('cannot process ', event.key)
				if len(value) > 1:
					lines = value.split('\r\n')
					savex = self.cur_x
					self.surf.fill(self.col)
					for line in lines:
						self.nb_ln= self.nb_ln+1
						tabs = line.split('\t')
						for tab in tabs:
							label_l = self.font.render(tab, 1, Colors.green)
							self.surf.blit(label_l, (self.cur_x, self.cur_y))
							self.cur_x+=120
							self.cur_y = self.nb_ln*self.line_h
						self.cur_x = savex
				self.nb_ln = 1
				self.cur_y = self.nb_ln*self.line_h
			if len(self.input) > 0:
				inp = self.font.render(self.input, 1, Colors.green)
				self.surf.fill(self.col)
				self.surf.blit(inp, (self.cur_x, self.cur_y))
			self.screen.blit(self.surf, (self.x_pos, self.y_pos))
			pygame.display.update()

class Box:
	def __init__(self, size, position, text=""):
		self.surface 	= pygame.Surface(size)
		self.text 		= text
		self.pos		= position
		self.size		= size
		self.focus		= False
		pygame.font.init()
		self.font 	= pygame.font.Font(None, 30)
		self.surface.fill(Colors.white)
	def action(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = event.pos
				if event.button == 1:
					if self.pos[0]+self.size[0] > pos[0] > self.pos[0] and self.pos[1]+self.size[1] > pos[1] > self.pos[1]:
						self.focus=True
						self.surface.fill((230, 230, 230))
					else:
						self.focus=False
			if event.type == pygame.KEYDOWN and self.focus is True:
				if event.key < 207:
					if event.unicode == '\b':
						self.text = self.text[:-1]
					else:
						self.text += event.unicode
				self.surface.fill(Colors.white)
				text_render = self.font.render(self.text, 1, Colors.black)
				self.surface.blit(text_render, (0, 0))

class Colors:
	black 	= (0,0,0)
	white 	= (255, 255, 255)
	yello	= (255, 125, 0)
	brown	= (170, 100, 50)
	orang	= (250, 255, 0)
	red		= (255, 0, 0)
	grey	= (125, 125, 125)
	green	= (0, 200, 30)

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
			y_scaled = (tup[1]-self.min)/((self.max-self.min)+0.01)*(self.height-10)
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

def plot_capture(screen):
	channels = Channel.channels
	Channel.reset()
	capt = busPirate.capture_voltage()
	surf = pygame.Surface((screen.get_width(), 50))
	for k, chan in enumerate(capt.channels):
		color = channels[k].color
		Channel(screen, capt.channels[chan], color, "ms")
	Channel.plotall()

def disp():
	connected = busPirate.isConnected()
	screen	= pygame.display.set_mode((1024,768))
	screen.fill(Colors.black)
	disp_default_chans(screen)
	if connected:
		tb = Textbox("console", screen, screen.get_width(), 350, 0, 350)
		bx = Box((80, 40), (300, 720))
		pygame.display.update()
		while True:
			evts = pygame.event.get()
			button(evts, screen, screen.get_width()-120, 720, 120, 40, 'capture', screen, plot_capture)
			tb.action(evts)
			bx.action(evts)
			screen.blit(bx.surface, bx.pos)
			mouse_action_trigger(evts, 4, zoomIn)
			mouse_action_trigger(evts, 5, zoomOut)
			pygame.display.update()
			time.sleep(0.01)
	else:
		print('No bus priate found. Try again !')
