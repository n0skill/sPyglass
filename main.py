import serial
import sys
import time
import busPirate
import display
import re


def main():
	port 	= sys.argv[1]
	cmd 	= sys.argv[2]
	if busPirate.isConnected():
		display.disp()
	else:
		display.disp_unconnected()
main()
