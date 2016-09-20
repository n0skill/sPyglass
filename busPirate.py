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

class DigitalCapture(object):
	"""docstring for """
	def __init__(self, arg):
		super(DigitalCapture, self).__init__()
		self.arg = arg

class AnalogCapture(object):
	"""docstring for AnalogCapture"""
	def __init__(self, arg):
		super(AnalogCapture, self).__init__()
		self.arg = arg


def isConnected(port='/dev/ttyUSB0'):
	try:
		ser = serial.Serial(port, 115200, timeout=0.5)
		command = 'i'
		reply = send_cmd(port, command)
		for line in reply.split('\r\n'):
			print(line)
			if line == "Bus Pirate v3a":
				print('okay')
				return True
	except serial.SerialException:
		print('Nothing found on ', port)
		return False

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
		if e.errno == 16:
			print('The device is busy. Stop other programs using it')
		else:
			print(e)

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
def bitbang_mode():
	conn = serial.Serial('/dev/ttyUSB0', 112500, timeout=0.01)
	for i in range(0,20):
		conn.write(b'\x00')
		if b'BBIO' in conn.read(10):
			return True
	return False
