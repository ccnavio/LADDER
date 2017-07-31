# Mission Planner Script
# Purpose: LEFT SIDE QUAD, Q1

import math
import time
# global exit_arm
# exit_arm = 0

def Safety_Check():
	if cs.ch7in > 1800:
		Script.SendRC(1,0,True)
		Script.SendRC(2,0,True)
		Script.SendRC(3, Script.GetParam('RC3_MIN'), True)
		Script.SendRC(4,0,True)
		Script.SendRC(5,0,True)

		Script.ChangeMode("Stabilize")
		print 'Safety Override'
		exit()
	else:
		return 0

def Check_Status():

	KILLROLL=0

	if cs.alt - Start_alt > 1.5:
		print 'Exceeded 1.5m'
		KILLROLL=1
	elif abs(cs.roll) > 15:
		KILLROLL=1
		print 'Exceeded roll of 15'
	elif cs.ch3in > 1800:
		KILLROLL=1
		print 'Ch 3 in exceeded 1800'
	elif cs.ch3out > 1800: #roll specific
		KILLROLL=1
		print 'Ch 3 out exceeded 1800'
	elif abs(cs.climbrate) > .75:
		KILLROLL=1
		print 'Exceeded climbrate'
	elif abs(cs.pitch) > 15:
		KILL=1
		print 'Exceeded pitch of 15 degrees'
	else:
		print 'Ok'
		
	if KILLROLL==1:
		Script.SendRC(1,0,True)
		Script.SendRC(2,0,True)
		Script.SendRC(3, Script.GetParam('RC3_MIN'), True)
		Script.SendRC(4,0,True)
		Script.SendRC(5,0,True)
		Script.ChangeMode("Stabilize")
		print 'Safety Override'
		exit()
	else:
		return 0 

def Arming_Check():
	attempt = 0
	yawcenter = cs.ch4in
	while cs.armed == False:
		Safety_Check()
		print 'MAV command failed to arm, trying again'
		if attempt > 7:
			Script.SendRC(3,992,True)
			Script.SendRC(4,2015,True)
			print 'Attempting to manually arm'
			Looping_Safety(3000)
			if cs.armed == False:
				print 'Arming failure, please reboot'
				Script.SendRC(7,1900,True)
				Safety_Check()
		Looping_Safety(200)
		MAV.doARM(True)
		attempt = attempt + 1
		print 'Attempt to arm #%d' % attempt

	#Checks to ensure that you dont take off with extreme yaw
	Script.SendRC(4,yawcenter,True)
	while cs.ch4in != yawcenter:
		Looping_Safety(50)
		print 'Yaw not aligned'

# Instead of Script.Sleep this will allow 
# safety loop to continue checking time in ms
def Looping_Safety(time):
	loop_var = 0
	while loop_var < time/25:
		Safety_Check()
		loop_var = loop_var + 1
		Script.Sleep(25)

# Is the leftside quad at a negative angle? 
# Take in a PWM value for throttle. You slowly increase throttle 
# until the angle of roll is about 2(?) degress off of your starting
# angle. At this point you should be in hover and then you wait for 
# a small alt change. 

def Control_Roll(init_roll, roll_pwm, Start_alt):
	delta_time = 0.1
	accum_error = 0
	last_error = 0
	Kp = 0.135
	Ki = 0.09
	Kd = 0.0036
	check = 0
	print 'In Control Roll'
	Check_Status()
	# Change to 1.6?
	while cs.mode == 'Stabilize':
		Check_Status()
		Safety_Check()

		if cs.alt - Start_alt > 1.3:
			check += 1
			if check == 15:
				return 0
				print 'Achieved constant alt, exiting control roll'

		print 'Control roll loop'
		error = cs.roll - init_roll	

		#Max angle
		if abs(error) >= 15:
			cs.ch7in = 1900
			print 'Max angle in control_roll'
			Safety_Check()

		#PID
		elif abs(error) > 2: 
			accum_error += error * delta_time
			der_error = (error - last_error)/delta_time
			output = (error * Kp) + (accum_error * Ki) + (der_error * Kd)
			last_error = error

			roll_pwm += -output*0.5 

			if roll_pwm > rc3max:
				roll_pwm = rc3max - 100
			elif roll_pwm < rc3min:
				roll_pwm = rc3min + 10

		Check_Status()
		Safety_Check()
		print 'Throttle input: %f' % roll_pwm
		Script.SendRC( 3, roll_pwm, True)
		Safety_Check()

	print 'Happily exiting control roll'

# ********************************* MAIN PROGRAM ********************************** #

Script.ChangeMode("Stabilize")
print 'Starting Script'
# implement for all channels from 1-9s
for chan in range(1,5):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

print 'Initializing 6-9 to False'
for chan in range (6,9):
	Script.SendRC(chan,0,False)
	Script.SendRC(3,Script.GetParam('RC3_MIN'), True)

Start_alt = cs.alt
init_roll = cs.roll
init_yaw = cs.yaw
PWM_in = 1460 # Jake's copter. Find throttle value
KILLROLL=0
rc3max = Script.GetParam('RC3_MAX') 
rc3min = Script.GetParam('RC3_MIN')

#ALTHOLD PARAMS
# Switch deadband (THR_DZ) to 10%
# A value of 100 means deadband is 10% above and below 50% 
# throttle (40%-60% throttle will trigger alt hold)
Script.ChangeParam("THR_DZ", 100)

#Max speed the pilot may request, in cm/s from 50 to 500.
Script.ChangeParam("PILOT_VELZ_MAX", 50)

Looping_Safety(2000)


# ----------------------------------- TAKEOFF ------------------------------------- #
print 'Copter should start arming'
arming = MAV.doARM(True)

Arming_Check()
print 'Copter armed'
Looping_Safety(3000)
				

# Takeoff parameters of Q3 would include this:
# If it's in stabilize, the roll and pitch will level
# out on their own. 

# The degree of roll initially is very dependent on the pixhawk itself.
# The degree of roll should be taken into consideration pre-flight and
# monitor the movement of the pixhawk. As the pixhawk moves, the roll
# degree changes accordingly. As of now, the angle of degree change will
# be set to 5 before wanting to fix the displacement.
print 'Initial roll: %f' % init_roll
Script.SendRC(3, PWM_in, True)
Control_Roll(init_roll, PWM_in, Start_alt)

print 'Exited Control_Roll'

Script.SendRC(3, PWM_in, True)
Check_Status()
print 'Throttle in = %d' %cs.ch3in
print 'Holding altitude for 4 sec'
Looping_Safety(4000)

# Landing sequence
# Script.ChangeParam("LAND_SPEED", 30)
# Script.ChangeMode("Land")
# print 'Landing'
# while cs.alt > Start_alt:
# 	Safety_Check()

print 'Ending script'
for chan in range(1,9):
	Script.SendRC(chan,0,True)

print 'Copter Disarming'
MAV.doARM(False)

print 'Script Over'
