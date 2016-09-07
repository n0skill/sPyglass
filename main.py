import serial
import sys
import time
import busPirate
import re


def main():
	port 	= sys.argv[1]
	cmd 	= sys.argv[2]
	#busPirate.send_cmd(port, '\r')
	data = busPirate.capture_voltage(port, 20)
	#data = busPirate.send_cmd(port, cmd)
main()
