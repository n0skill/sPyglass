import serial
from bp_SPI import SPI
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
			self.channels['ch4'].append((k, float(val['OR'])))

class BusPirate():
	def __init__(self, port, baudrate):
		# Check serial port before instancing new buspirate objects
		self.port 		= port
		self.connected 	= True
		self.mode 		= None
		self.baudrate 	= baudrate
		try:
			self.reset()
		except serial.SerialException as e:
			self.connected = False
			print('Could not find anything on port', port)

	def open_connection(self):
		return serial.Serial(self.port, self.baudrate)

	def bitbang(self):
		modes = {
			# TODO: See if there are common command so that we can simply use
			# an array (and the positions therein as the commands "ids" like
			# pos 1 = read etc. instead of a hash table....
			'UART': 	{'read': b'\x02', 'write': b'\x03', 'send': b'\x04'},
			'1-Wire': 	{'read': b'\x03', 'write': b'\x04', 'send': b'\x05'},
			'RAW': 		{'read': b'\x1A', 'write': b'\x1B', 'send': b'\x1C'}
		}

		# From the wiki
		if self.connected:
			if self.mode is not 'BBIO1':
				vals = self.write(b'\x00', 20, 5)
				if vals is not None:
					if b'BBIO1' in vals:
						print('Switched to bitbang !')
						self.mode = 'BBIO1'
			else:
				print('already in binary mode !')
	# SPI
	def enter_spi(self):
		if self.mode is not 'BBIO1':
			self.bitbang()
		if SPI.enter_mode(self):
			return True
		else:
			return False

	def spi_sniff_csl(self):
		SPI.sniff(self)

	def spi_sniff_csh(self):
		print('call csi')
		SPI.CS_high(self)
		pass

	def spi_transfer(self):
		SPI.transfer(self, 0xFF)
		pass

	def spi_speed(self):
		SPI.speed(self)
		pass

	def spi_write_read(self):
		SPI.write_read(self)
		pass

	def isConnected(self):
		try:
			self.write('i')
			reply = self.read(10)
			print(reply, ' in isConnected')
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

	def write(self, cmd, times=1, reply_length=1):
		if self.connected == True:
			conn = serial.Serial(self.port, 112500)
			for i in range(0, times):
				conn.write(cmd)
			return conn.read(reply_length)
		else:
			print('Bus Pirate probably is not connected')
	def read(self, bytes):
		if self.connected == True:
			conn = serial.Serial(self.port, self.baudrate, timeout=0.01)
			conn.read(bytes)
	def cli_rw(self, cmd):
		if self.connected == True:
			reply = ""
			cmd = cmd+'\n'
			conn = serial.Serial(self.port, self.baudrate, timeout=0.01)
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
		self.write('#\r'.encode())

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
