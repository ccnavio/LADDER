# Mission Planner Script
# Purpose: LEFT SIDE QUAD, Q1

import math
import time

def Safety_Check():
	if cs.ch7in > 1800:
		for chan in range(1,9):
			Script.SendRC(chan,0,True)
		Script.ChangeMode("Stabilize")
		print 'Safety Override'
		exit()
	else:
		return 0

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
	count = 0
	print 'In Control Yaw'

	while cs.alt - Start_alt < 1.3:	
		print 'While loop'
		error = cs.yaw - init_yaw	

		Safety_Check()
		# # yaw correction function and updates pitch of Q1 
		if abs(error) > 2: 
			accum_error += error * delta_time
			der_error = (error - last_error)/delta_time
			output = (error * Kp) + (accum_error * Ki) + (der_error * Kd)
			last_error = error

			pitch_pwm += -output*0.5 

			if pitch_pwm > Script.GetParam('RC2_MAX'):
				pitch_pwm = Script.GetParam('RC2_MAX') - 100
			elif pitch_pwm < Script.GetParam('RC2_MIN'):
				pitch_pwm = Script.GetParam('RC2_MIN') + 10

		print pitch_pwm
		Script.SendRC( 2, pitch_pwm, True)
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
MAV.doARM(True)

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
print init_yaw
Script.SendRC(3, PWM_in, True)
Control_Yaw(init_yaw, pitch_pwm, Start_alt)
print 'Exit Control_Yaw'

Script.ChangeMode("AltHold")
Looping_Safety(4000)

# Landing sequence
Script.SendRC(3, PWM_in, True)

while cs.alt > Start_alt:
	Safety_Check()

# Script.ChangeParam("LAND_SPEED", 30)
# Script.ChangeMode("Land")
# print 'Landing'
# while cs.alt > Start_alt:
# 	Safety_Check()

for chan in range(1,9):
	Script.SendRC(chan,0,True)

print 'Copter Disarming'
MAV.doARM(False)

print 'Script Over'
