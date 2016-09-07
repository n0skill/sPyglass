import serial
import sys
import time
import busPirate

def main():
	port 	= sys.argv[1]
	try:
		ser	= serial.Serial(port, 115200, timeout=5)
		if ser.is_open:
			print('open!')
			ser.write('\r'.encode()) # We have to send an \r to get to the menu
			ser.write('?\r'.encode())# Tesing: get the menu
			out = ''
			time.sleep(1)
			while ser.inWaiting() > 0:
				out += str(ser.readline())
			print(out)
			ser.close()
			print('done.')
			busPirate.main(10)
	except serial.SerialException as e:
		if e.errno == 2:
			print('Could not find device. Check spelling.')
		if e.errno == 16:
			print('The device is busy. Stop other programs using it')
		else:
			print(e)
main()
