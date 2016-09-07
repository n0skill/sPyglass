def main(time):
	voltage_cmd = 'v'
	cmd=""
	for i in range(0, time):
		cmd += voltage_cmd+'%'
	print(cmd)

if __name__ is '__main__':
	capture_voltage(10)
