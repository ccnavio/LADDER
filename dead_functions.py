# Dead functions
# Bruh don't use these

def Choose_Speed(wanted_h, PWM_in):	# in m/s
	while cs.alt < wanted_h:
		Script.SendRC(3, PWM_in, True)
		if PWM_in < 1800:
			PWM_in = PWM_in + 2
			Safety_Check()
		else:
			Safety_Check()

	while cs.alt > wanted_h + 0.5:
		Script.SendRC(3, PWM_in, True)
		if PWM_in > 1000:
			PWM_in = PWM_in - 2
			Safety_Check()
		else:
			Safety_Check()
	return PWM_in

def Takeoff(PWM_in, height):
	while cs.alt < 0.2:
		cs.verticalspeed = 0.2
		Script.SendRC(3, PWM_in, True)
		PWM_in = PWM_in + 1
		Safety_Check()

	while cs.alt < height:
		cs.verticalspeed = 0.15
		Script.SendRC(3, PWM_in, True)
		if cs.verticalspeed > 0.3:
			PWM_in = PWM_in - 1
			print 'in takeoff loop'
		Safety_Check()

	return PWM_in

def Vertical_Speed(PWM_in, wanted_alt):
	while cs.alt < wanted_alt - 2:
		cs.verticalspeed = 0.2
		Script.SendRC(3, PWM_in, True)
		if cs.verticalspeed > 0.5:
			# PWM_in = PWM_in - 1
			print 'in first vs loop'
		Safety_Check()

	while cs.alt < wanted_alt - 1:
		cs.verticalspeed = 0.1
		Script.SendRC(3, PWM_in, True)
		if cs.verticalspeed > 0.2:
			# PWM_in = PWM_in - 1
			print 'in second vs loop'
		Safety_Check()

	while cs.alt < wanted_alt:
		Script.SendRC(3, PWM_in, True)
		Safety_Check()

	return PWM_in