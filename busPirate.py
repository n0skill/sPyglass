# TODO: move all communication handling in this file/class
import serial
import time
import re

class Captured:
	def __init__(self, values):
		# Capture is an array of values
		self.values = values
		self.channels = {'ch1': [], 'ch2': [], 'ch3': [], 'ch4': []}
		for k, val in enumerate(self.values):
			self.channels['ch1'].append((k, float(val['BR'])))
			self.channels['ch2'].append((k, float(val['RD'])))
			self.channels['ch3'].append((k, float(val['YW'])))
			self.channels['ch4'].append((k, float(val['RD'])))
	def print_all(self):
		for i in self.channels:
			print(self.channels[i])

def isConnected(port='/dev/ttyUSB0'):
	try:
		ser = serial.Serial(port, 115200, timeout=0.05)
		command = ['i']
		reply = send_cmd(port, command)
		for line in reply.split('\r\n'):
			print(line)
			if line == "Bus Pirate v3a":
				print('okay')
				return True
	except serial.SerialException:
		print('Nothing found on ', port)
		return False

def send_cmd(port, cmd_lst):
	print('Sending cmds: ' + str(cmd_lst) + ' to ' + str(port))
	try:
		recv = ""
		conn = serial.Serial(port, 115200, timeout=0.01)
		time.sleep(0.01)
		for cmd in cmd_lst:
			cmd = cmd+'\n'
			conn.write(cmd.encode())
			time.sleep(0.008)
		while conn.inWaiting() > 0:
			recv += conn.read(256).decode("utf-8")
		return recv

	except serial.SerialException as e:
		if e.errno == 2:
			print('Could not find device. Check spelling.')
		if e.errno == 16:
			print('The device is busy. Stop other programs using it')
		else:
			print(e)

def capture_voltage(port='/dev/ttyUSB0', time=100):
	mode = 'm'
	w	 = '2'
	psu	 = 'W'
	voltage_cmd = 'v'
	capt_lst = []
	results = {}
	values = ""
	try:
		send_cmd(port, mode)
		send_cmd(port, w)
		send_cmd(port, psu)
		for i in range(0, time):
			values += send_cmd(port, voltage_cmd)
		clean = re.findall('^(GND.+)$', values, re.MULTILINE)
		for val in clean:
			if val.endswith('L\t\r') or val.endswith('H\t\r'):
				reg = re.findall('(\d+.\d+)', val)
				results = {'BR': reg[0], 'RD': reg[1], 'OR': reg[2], 'YW':reg[3]}
				capt_lst.append(results)
		captured_vals = Captured(capt_lst)
		print('expected values: ' + str(time) + '. Got: ' + str(len(capt_lst)))
		return captured_vals
	except Exception as e:
		print(e)
		return None
