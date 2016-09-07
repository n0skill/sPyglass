import serial
import sys
import time

def main():
	port 	= sys.argv[1]
	try:
		ser	= serial.Serial(port, 115200, timeout=5)
		if ser.is_open:
			print('open!')
			ser.write(b'?')
			out = ''
			time.sleep(1)
			out += str(ser.readline())
			print(out)
			ser.close()
			print('done.')
	except serial.SerialException as e:
		if e.errno == 2:
			print('Could not find device. Check spelling.')
		if e.errno == 16:
			print('The device is busy. Stop other programs using it')
		else:
			print(e)
main()
