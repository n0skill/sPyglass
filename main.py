import serial
import sys
import time
import busPirate

def main():
	port 	= sys.argv[1]
	#busPirate.send_cmd(port, '\r')
	busPirate.capture_voltage(port, 1)

main()
