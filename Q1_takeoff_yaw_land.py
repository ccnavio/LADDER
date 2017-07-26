# Mission Planner Script
# Purpose: LEFT SIDE QUAD, Q1

import math
import time

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

	KILL = 0

	if cs.alt - Start_alt > 1.5:
		print 'Exceeded 2 m'
		KILL=1
	elif abs(cs.roll) > 15:
		KILL=1
		print 'Exceeded roll of 15 degrees'
	elif cs.ch3in > 1800:
		KILL=1
		print 'Ch 3 in exceeded 1800'
	elif abs(cs.climbrate) > .15:
		KILL=1
		print 'Exceeded climbrate'
	elif abs(cs.pitch) > 15:
		KILL=1
		print 'Exceeded pitch of 15 degrees'
	else:
		print 'Ok'
		
	if KILL==1:
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
	attempt = 1
	yawcenter = cs.ch4in
	while cs.armed == False:
		Safety_Check()
		print 'MAV command failed to arm, trying again'
		print '#%d' % attempt
		if attempt > 1:
			Script.SendRC(3,992,True)
			Script.SendRC(4,2015,True)
			print 'Attempting to manually arm (5 sec)'
			Looping_Safety(5000)
			if cs.armed == False:
				print 'Arming failure, please reboot'
				Script.SendRC(7,1900,True)
				Safety_Check()
		Looping_Safety(1000)
		attempt = attempt + 1

	#Checks to ensure that you dont take off with extreme yaw
	Script.SendRC(4,yawcenter,True)
	while cs.ch4in != yawcenter:
		Looping_Safety(50)
		print 'Yaw not aligned, please wait'


# Instead of Script.Sleep this will allow 
# safety loop to continue checking time in ms
def Looping_Safety(time):
	loop_var = 0
	while loop_var < time/25:
		Safety_Check()
		loop_var = loop_var + 1
		Script.Sleep(25)

def Control_Yaw(init_yaw, pitch_pwm, Start_alt):
	delta_time = 0.1
	accum_error = 0
	last_error = 0
	Kp = 0.135
	Ki = 0.09
	Kd = 0.0036
	init_pitch_pwm = pitch_pwm
	print 'In Control Yaw'
	print 'Initial relative altitude %f' % (cs.alt - Start_alt)
	while cs.alt - Start_alt < 0.5:	
		error = cs.yaw - init_yaw	
		print 'Relative altitude %f' % (cs.alt - Start_alt)
		# # yaw correction function and updates pitch of Q1 
	 	error = (180/math.pi)* math.asin(math.sin((cs.yaw - init_yaw)*(math.pi/180)))
		print "Error: %d" % error 
		Safety_Check()
		Check_Status()
		if abs(error) >= 45:
			cs.ch7in = 1900
			print 'Exceeded 45 degrees'
			Safety_Check()	

		elif abs(error) > 2: 
			accum_error += error * delta_time
			der_error = (error - last_error)/delta_time
			output = (error * Kp) + (accum_error * Ki) + (der_error * Kd)
			last_error = error

			pitch_pwm += -output
			Check_Status()
			if pitch_pwm > Script.GetParam('RC2_MAX'):
				pitch_pwm = Script.GetParam('RC2_MAX') - 200
			elif pitch_pwm < Script.GetParam('RC2_MIN'):
				pitch_pwm = Script.GetParam('RC2_MIN') + 10

		print 'CH2 In: %d' % pitch_pwm
		Script.SendRC(2, pitch_pwm, True)
		Safety_Check()

# ---------------------------- MAIN PROGRAM ---------------------------- #
# Takeoff parameters
Script.ChangeMode("Stabilize")
print 'Starting Script'
# implement for all channels from 1-9

# Initial pitch value
pitch_pwm = cs.ch2in

for chan in range(1,5):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

print 'Initializing 6-9 to False'
for chan in range (6,9):
	Script.SendRC(chan,0,False)
	Script.SendRC(3,Script.GetParam('RC3_MIN'), True)

Start_alt = cs.alt
init_yaw = cs.yaw
PWM_in = 1580 # Jonathan's copter. Find throttle value

Looping_Safety(2000)
print 'Copter should start arming'
arming = MAV.doARM(True)

Arming_Check()

Looping_Safety(2000)
print 'Copter should be armed'				

# Takeoff parameters of Q1 would include this:
# If it's in stabilize, the roll and pitch will level
# out on their own. 

# The degree of roll initially is very dependent on the pixhawk itself.
# The degree of roll should be taken into consideration pre-flight and
# monitor the movement of the pixhawk. As the pixhawk moves, the roll
# degree changes accordingly. As of now, the angle of degree change will
# be set to 5 before wanting to fix the displacement.
print 'Initial Yaw: %d' % init_yaw
Script.SendRC(3, PWM_in, True)
Check_Status()
Control_Yaw(init_yaw, pitch_pwm, Start_alt)
print 'Exit Control_Yaw'

Script.ChangeMode("AltHold")
while cs.mode != 'AltHold':
	print 'waiting to switch to alt hold'
	Looping_Safety(2000)
	Script.ChangeMode("AltHold")

# Landing sequence
Script.SendRC(3, PWM_in, True)

# Script.ChangeParam("LAND_SPEED", 30)
# Script.ChangeMode("Land")
# print 'Landing'

for chan in range(1,9):
	Script.SendRC(chan,0,True)

print 'Copter Disarming'
MAV.doARM(False)

print 'Script Over'