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
		self.connected = True
		try:
			serial.Serial(port, 115200)
			self.reset()
		except serial.SerialException as e:
			self.connected = False
			print('Could not find anything on port', port)

	def bitbang(self):
		if self.connected:
			self.reset()
			for i in range(0,20):
				self.write(b'\x00')
			vals = self.read(10)

			if vals is not None:
				if b'BBIO' in vals:
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
	def cli_rw(self, cmd):
		if self.connected == True:
			reply = ""
			cmd = cmd+'\n'
			conn = serial.Serial(self.port, 112500, timeout=0.01)
			time.sleep(0.02)
			conn.write(cmd.encode())
			time.sleep(0.05)
			while conn.inWaiting() > 0:
				reply += conn.read(256).decode("utf-8")
				time.sleep(0.01)
			return reply

	def reset(self):
		for i in range(0,10):
			self.write('\r'.encode())
		self.write('#'.encode())

	def capture_voltage(self, pause, nb):
		values = ""
		capt_lst = []
		results = {}

		capt_v_cmd = 'v'
		capt_v_cmd = capt_v_cmd+str('%'*pause)
		self.cli_rw('m')
		self.cli_rw('2')
		self.cli_rw('W')
		n_cmds = int(nb*len(capt_v_cmd)/255)+1
		for i in range(1,n_cmds+1):
			if i < n_cmds:
				cmd_to_send = capt_v_cmd*(int(255/len(capt_v_cmd))+1)
				print(cmd_to_send)
				values += self.cli_rw(cmd_to_send)
			else:
				cmd_to_send = capt_v_cmd*(nb%255)
				values += self.cli_rw(cmd_to_send)

		clean = re.findall('^(GND.+)$', values, re.MULTILINE)
		for val in clean:
			if val.endswith('L\t\r') or val.endswith('H\t\r'):
				reg = re.findall('(\d+.\d+)', val)
				results = {'BR': reg[0], 'RD': reg[1], 'OR': reg[2], 'YW':reg[3]}
				capt_lst.append(results)
		captured_vals = Captured(capt_lst)
		list_capt.append(captured_vals)
		print('expected values: ' + str(nb) + '. Got: ' + str(len(capt_lst)))
		return captured_vals

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

def export():
	with open('./spyglass.txt', 'w') as f:
		for data in list_capt:
			f.write(str(data.values))
