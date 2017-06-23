# Carie Navio
# Mission Planner Script
# Purpose: Waypoint script testing
# THIS DOES NOT INCLUDE THE UNLINKING PORTION

# 1 roll
# 2 pitch
# 3 throttle
# 4 yaw
# 5 flight modes
# 6 empty
# 7 autotune (?)
# 8 empty (?)
# 9 epm activation 

# safety switch on radio 7
def Safety_Check():
	if cs.ch7in > 1800:
		for chan in range(1,9):
			Script.SendRC(chan,0,True)

		# Returns power back to the pilot 
		Script.Sleep(25)
		print 'Safety Override'
		exit()
	else:
		return 0

def Looping_Safety(time):	# in ms 
	loop_var = 0
	while_var = 0
	while_var = time/50
	while loop_var < while_var:
		Safety_Check()
		Script.Sleep(50)
		loop_var = loop_var + 1
	print 'End Safety Loop'

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

def Takeoff(PWM_in):
	while cs.alt < 1:
		cs.verticalspeed = 0.1
		Script.SendRC(3, PWM_in, True)
		PWM_in = PWM_in + 1
		Safety_Check()
	return PWM_in

def Landing(PWM_in):
	while cs.alt < 0.1:
		Script.SendRC(3, PWM_in, True)
		cs.verticalspeed = -0.2
		PWM_in = PWM_in - 1
		Safety_Check()
	# return PWM_in

 # def Choose_Alt(wanted_alt, PWM_in, wanted_speed): # in meters

# --------------------------------- MAIN PROGRAM --------------------------------- #
print 'Starting Script'
# implement for all channels from 1-9
takeoff_pwm = 0

for chan in range(1,5):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

print 'Initializing 6-8 to False'
for chan in range (6,14):
	Script.SendRC(chan,0,False)
	Script.SendRC(3,Script.GetParam('RC3_MIN'), True)

print 'Copter should start arming'
MAV.doARM(True)
Looping_Safety(2000)

print 'Taking off'
takeoff_pwm = Takeoff(Script.GetParam('RC3_MIN'))

while cs.alt < 3:
	cs.verticalspeed = 0.2
	Script.SendRC(3, takeoff_pwm, True)

# while cs.alt < 3:
# 	testing_var = Choose_Speed(3,testing_var, 0.25)
print 'PosHold copter'
Script.SendRC(5,1400,True)
Looping_Safety(2000)

print 'Landing'
Landing(testing_var)

MAV.doARM(False)

for chan in range(1,9):
	Script.SendRC(chan,0,True)

print 'Done'