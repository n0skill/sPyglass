import sys
import busPirate
import display
import re

def main():
	if len(sys.argv) > 1:
		port = sys.argv[1]
	else:
		port = "/dev/ttyUSB0"

	bp	= busPirate.BusPirate(port, 115200)
	try:
		if bp.connected == True:
			display.display(bp)
		else:
			display.not_connected(bp)
			print('Not connected')

	except KeyboardInterrupt:
		print('Interrupted. Quit nicely pls. kthxbye')
		bp.reset()
main()
