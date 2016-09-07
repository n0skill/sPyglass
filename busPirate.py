# TODO: move all communication handling in this file/class
import serial
import time

class Capture:
	def __init__(self, values):
		# Capture is an array of values
		capture = self.values


def recv(port):
	try:
		ser	= serial.Serial(port, 115200, timeout=5)
		recv = ''
		print('Listening...')
		time.sleep(1)
		if ser.is_open:
			while ser.inWaiting() > 0:
				recv += ser.readline()
		print(recv)
	except serial.SerialException as e:
		if e.errno == 2:
			print('Could not find device. Check spelling.')
		if e.errno == 16:
			print('The device is busy. Stop other programs using it')
		else:
			print(e)

def send_cmd(port, cmd):
	print('Sending cmd: ' + str(cmd) + ' to ' + str(port))
	cmd = cmd+'\r' # Carriage return to execute command
	try:
		ser	= serial.Serial(port, 115200, timeout=5)
		if ser.is_open:
			print('open!')
			ser.write(cmd.encode())
			time.sleep(2)
			recv = ""
			while ser.inWaiting() > 0:
				recv += ser.read().decode("utf-8")
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
	voltage_cmd = 'v%'
	cmd=""
	for i in range(0, time):
		cmd += voltage_cmd
	values = send_cmd(port, cmd)
	e = capture(values)
if __name__ is '__main__':
	capture_voltage(10)
