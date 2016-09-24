import sys
import busPirate
import display
import re

def main():
	port 	= sys.argv[1]
	bp = busPirate.BusPirate(port)
	if bp.isConnected():
		display.display(bp)
	else:
		print('Nothing found on port')
main()
