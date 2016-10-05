import sys
import busPirate
import display
import re

def main():
	try:
		if len(sys.argv) > 1:
			port = sys.argv[1]
		else:
			port = "/dev/ttyUSB0"
		bp	= busPirate.BusPirate(port)
		if bp == None:
			print('Its a none, so it dosent exist')
		print(bp)
		display.display(bp)

	except KeyboardInterrupt:
		print('Interrupted. Quit nicely pls. kthxbye')
		bp.reset()
main()
