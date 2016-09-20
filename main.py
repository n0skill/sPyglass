import serial
import sys
import time
import busPirate
import display
import re


def main():
	port 	= sys.argv[1]
	if busPirate.isConnected():
		display.display()
	else:
		display.disp_unconnected()
main()
