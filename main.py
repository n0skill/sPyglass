import serial
import sys
import time
import busPirate
import display
import re


def main():
	port 	= sys.argv[1]
	cmd 	= sys.argv[2]
	#busPirate.send_cmd(port, '\r')
	display.disp()
#	for key in data:
#		print(data[key])
	#display.graph(data)
	#data = busPirate.send_cmd(port, cmd)
main()
