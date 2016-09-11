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
4
def isConnected(port='/dev/ttyUSB0'):
	try:
		ser = serial.Serial(port, 115200, timeout=1)
		return True
	except serial.SerialException:
		print('Nothing found on ', port)
		return False
def send_cmd(port, cmd_lst):
	print('Sending cmds: ' + str(cmd_lst) + ' to ' + str(port))
	try:
		ser	= serial.Serial(port, 115200, timeout=1)
		recv = ""
		time.sleep(0.5)
		if ser.is_open:
			for cmd in cmd_lst:
				cmd = cmd+'\n'
				ser.write(cmd.encode())
				time.sleep(0.01) # Do not monopolize CPU in order to recieve data
			while ser.inWaiting() > 0:
				recv += ser.read(1024).decode("utf-8")
				time.sleep(0.01) # Do not monopolize CPU
			ser.close()
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
	voltage_cmd = 'v%'
	volts = ''
	capt_lst = []
	results = {}
	try:
		for i in range(0, time):
			volts += voltage_cmd
		cmds = [mode, w, psu, volts]
		values = send_cmd(port, cmds)
		clean = re.findall('^(GND.+)$', values, re.MULTILINE)
		for val in clean:
			if val.endswith('L\t\r') or val.endswith('H\t\r'):
				reg = re.findall('(\d+.\d+)', val)
				results = {'BR': reg[0], 'RD': reg[1], 'OR': reg[2], 'YW':reg[3]}
				capt_lst.append(results)
		zerg = Captured(capt_lst)
		zerg.print_all()
		#print('expected values: ' + str(time) + '. Got: ' + str(len(capt_lst)))
		return zerg
	except Exception as e:
		print(e)
		return None
