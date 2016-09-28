import sys
import busPirate
import display
import re

def main():
	try:
		if len(sys.argv) > 1:
			port 	= sys.argv[1]
		else:
			port	= "/dev/ttyUSB0"
		bp 		= busPirate.BusPirate(port)
		if bp.isConnected():
			display.display(bp)
		else:
			display.not_connected()
	except KeyboardInterrupt:
		print('Interrupted. Quit nicely pls. kthxbye')
		bp.reset()
main()
