# TODO: move all communication handling in this file/class
import serial
import time
import re

class Capture:
	def __init__(self, values):
		# Capture is an array of values
		self.values = values
def send_cmd(port, cmd):
	print('Sending cmd: ' + str(cmd) + ' to ' + str(port))
	cmd = cmd+'\r' # Carriage return to execute command
	try:
		ser	= serial.Serial(port, 115200, timeout=3)
		time.sleep(1)
		if ser.is_open:
			print('open!')
			ser.write(cmd.encode())
			time.sleep(1)
			recv = ""
			while ser.inWaiting() > 0:
				recv += ser.read(256).decode("utf-8")
			ser.close()
			return recv

	except serial.SerialException as e:
		if e.errno == 2:
			print('Could not find device. Check spelling.')
		if e.errno == 16:
			print('The device is busy. Stop other programs using it')
		else:
			print(e)

def capture_voltage(port, time):
	voltage_cmd = 'v%%'
	cmd=""
	capt = []
	results = {}
	try:
		for i in range(0, time):
			cmd += voltage_cmd
		values = send_cmd(port, cmd)
		clean = re.findall('^(GND.+)$', values, re.MULTILINE)
		for val in clean:
			if val.endswith('L\t\r') or val.endswith('H\t\r'):
				# print(val)
				reg = re.findall('(\d+.\d+)', val)
				print(reg[0], reg[1], reg[2], reg[3])
				results = {'BR': reg[0], 'RD': reg[1], 'OR': reg[2], 'YW':reg[3]}
				#for key in results:
				#	print(results[key])
				capt.append(results)
		return capt
	except Exception as e:
		print(e)
		return None
