# TODO: move all communication handling in this file/class
import serial
import time
import re

list_capt = []
class Captured:
	""" Class for data capture and manipulations"""
	def __init__(self, values):
		# Capture is an array of values
		self.values = values
		self.channels = {'ch1': [], 'ch2': [], 'ch3': [], 'ch4': []}
		for k, val in enumerate(self.values):
			self.channels['ch1'].append((k, float(val['BR'])))
			self.channels['ch2'].append((k, float(val['RD'])))
			self.channels['ch3'].append((k, float(val['YW'])))
			self.channels['ch4'].append((k, float(val['RD'])))

class BusPirate():
	def __init__(self, port):
		# Check serial port before instancing new buspirate objects
		self.port 	= port
		try:
			serial.Serial(port, 115200)
			self.reset()
			self.connected = True
		except serial.SerialException as e:
			self.connected = False
			print('Could not find anything on port', port)
			self = None

	def bitbang(self):
		if obj_to_bang.connected:
			obj_to_bang.reset()
			for i in range(0,20):
				obj_to_bang.write(b'\x00')
			if b'BBIO' in obj_to_bang.read(10):
				print('Switched to bitbang !')

	def SPI(self):
		self.bitbang()
		self.write(b'\x01')
		self.read(2)
	def UART(self):
		self.bitbang()
		self.write(b'\x02')
		self.read(2)
	def I2C(self):
		self.bitbang()
		self.write(b'\x03')
		self.read(2)

	def switch_mode(self, mode):
		if mode == "SPI":
			self.SPI()
			pass
		elif mode == "UART":
			self.UART()
			pass
		elif mode == "I2C":
			self.I2C()
		else:
			self.bitbang()

	def isConnected(self):
		try:
			reply = send_cmd(self.port, 'i')
			if reply == None:
				self.connected = False
			else:
				for line in reply.split('\r\n'):
					if line == "Bus Pirate v3a":
						self.connected = False
				return self.connected
		except serial.SerialException as e:
			print('Error occurred: ', e)
			print('Nothing found on  ', self.port)
			self.connected = False
			return self.connected

	def write(self, cmd):
		if self.connected == True:
			conn = serial.Serial(self.port, 112500, timeout=0.01)
			conn.write(cmd)
		else:
			print('Bus Pirate probably is not connected')
	def read(self, bytes):
		if self.connected == True:
			conn = serial.Serial(self.port, 112500, timeout=0.01)
			conn.read(bytes)
	def cli_read(self):
		if self.connected == True:
			reply = ""
			conn = serial.Serial(self.port, 112500, timeout=0.01)
			while conn.inWaiting() > 0:
				reply += conn.read(256).decode("utf-8")
			return reply

	def reset(self):
		for i in range(0,10):
			self.write('\r'.encode())
		self.write('#'.encode())
	def capture_voltage(self, pause, nb):
		vals = []
		capt_v_cmd = '%'*pause
		capt_v_cmd = 'v'+capt_v_cmd
		n_cmds = int(nb*len(capt_v_cmd)/255)+1
		self.write('m')
		self.write('2')
		self.write('W')
		self.write('v')
		self.write('%'*pause)
		for i in range(0,n_cmds+1):
			if i < n_cmds:
				cmd_to_send = capt_v_cmd*(int(255/len(capt_v_cmd))+1)
				self.write(cmd_to_send)
				vals += self.cli_read()
		return vals

def send_cmd(port, cmd):
	print('Sending cmds: ' + str(cmd) + ' to ' + str(port))
	try:
		recv = ""
		conn = serial.Serial(port, 115200, timeout=0.05)
		time.sleep(0.05)
		cmd = cmd+'\n'
		conn.write(cmd.encode())
		time.sleep(0.01)
		while conn.inWaiting() > 0:
			recv += conn.read(256).decode("utf-8")
			time.sleep(0.01)
		return recv

	except serial.SerialException as e:
		if e.errno == 2:
			print('Could not find device. Check spelling.')
			return None
		if e.errno == 16:
			print('The device is busy. Stop other programs using it')
			return None
		else:
			print(e)
			return None
def capture_voltage(pause_times, port='/dev/ttyUSB0', time=100):
	cmd_mode = 'm'
	cmd_w	 = '2'
	cmd_psu	 = 'W'
	voltage_cmd = 'v'
	pause_cmd	= '%'*int(pause_times)
	cmd = (voltage_cmd+pause_cmd)
	print(cmd)
	capt_lst = []
	results = {}
	values = ""
	try:
		send_cmd(port, cmd_mode)
		send_cmd(port, cmd_w)
		send_cmd(port, cmd_psu)
		n_cmds = int(time*len(cmd)/255)+1
		# If the command is longer than what we can use, send multiple commands
		for i in range(1, n_cmds+1):
			# If it's not the last iteration
			if i < n_cmds:
				actual_cmd 	= cmd*(int(255/len(cmd))+1)
				print(actual_cmd)
				values += send_cmd(port, actual_cmd)
			else:
				# It's the last bit that is missing
				print('Lastly: ')
				actual_cmd = cmd*(time%255)
				values += send_cmd(port, actual_cmd)

		clean = re.findall('^(GND.+)$', values, re.MULTILINE)
		for val in clean:
			if val.endswith('L\t\r') or val.endswith('H\t\r'):
				reg = re.findall('(\d+.\d+)', val)
				results = {'BR': reg[0], 'RD': reg[1], 'OR': reg[2], 'YW':reg[3]}
				capt_lst.append(results)
		captured_vals = Captured(capt_lst)
		list_capt.append(captured_vals)
		print('expected values: ' + str(time) + '. Got: ' + str(len(capt_lst)))
		return captured_vals
	except Exception as e:
		print(e)
		return None

def export():
	with open('./spyglass.txt', 'w') as f:
		for data in list_capt:
			f.write(str(data.values))
