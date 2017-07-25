# Mission Planner Script
# Purpose: LEFT SIDE QUAD, Q1

import math
import time

def Safety_Check():
	if cs.ch7in > 1800:
		if not Script.SendRC(1,0,True)
			print 'Channel 1 NOT set to zero'
		if not Script.SendRC(2,0,True)
			print 'Channel 2 NOT set to zero'
		if not Script.SendRC(3, Script.GetParam('RC3_MIN'), True)
			print 'Channel 3 NOT set to minimum value'
		if not Script.SendRC(4,0,True)
			print 'Channel 4 NOT set to zero'
		if not Script.SendRC(5,0,True)
			print 'Channel 5 NOT set to zero'

		if not Script.ChangeMode("Stabilize")
			print 'Could NOT change mode to Stabilize'
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
	init_pitch_pwm = pitch_pwm
	print 'In Control Yaw'

	while cs.alt - Start_alt < 1.3:	
		# error = cs.yaw - init_yaw	

		# # yaw correction function and updates pitch of Q1 
	 	error = (180/math.pi)* math.asin(math.sin((cs.yaw - init_yaw)*(math.pi/180)))
		print "Error: %d" % error 
		Safety_Check()

		if abs(error) >= 45:
			cs.ch7in = 1900
			Safety_Check()	

		elif abs(error) > 2: 
			accum_error += error * delta_time
			der_error = (error - last_error)/delta_time
			output = (error * Kp) + (accum_error * Ki) + (der_error * Kd)
			last_error = error

			pitch_pwm += -output*0.5 

			if pitch_pwm > Script.GetParam('RC2_MAX'):
				pitch_pwm = Script.GetParam('RC2_MAX') - 200
			elif pitch_pwm < Script.GetParam('RC2_MIN'):
				pitch_pwm = Script.GetParam('RC2_MIN') + 10

		print pitch_pwm
		if not Script.SendRC( 2, pitch_pwm, True)
			print 'Channel 2 pitch pwm NOT sent'
		Safety_Check()

# ---------------------------- MAIN PROGRAM ---------------------------- #
# Takeoff parameters
if not Script.ChangeMode("Stabilize")
	print 'Could NOT change to Stabilize'
print 'Starting Script'
# implement for all channels from 1-9

# Initial pitch value
pitch_pwm = cs.ch2in

for chan in range(1,5):
    if not Script.SendRC(chan,1500,False)
	print 'Could NOT send 1500 to channel: %d' % chan
    if not Script.SendRC(3,Script.GetParam('RC3_MIN'),True)
	print 'Could NOT send minimum value to channel: %d' % chan

print 'Initializing 6-9 to False'
for chan in range (6,9):
	if not Script.SendRC(chan,0,False)
		print 'Could NOT set channel: %d to zero' % chan
	if not Script.SendRC(3,Script.GetParam('RC3_MIN'), True)
		print 'Could NOT set channel: %d to minimum value' % chan

Start_alt = cs.alt
init_yaw = cs.yaw
PWM_in = 1580 # Jonathan's copter. Find throttle value

Looping_Safety(2000)
print 'Copter should start arming'
arming = MAV.doARM(True)

if arming == False:	
	exit()

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
if not Script.SendRC(3, PWM_in, True)
	print 'Could NOT send channel 3 PWM_in'
Control_Yaw(init_yaw, pitch_pwm, Start_alt)
print 'Exit Control_Yaw'

Script.ChangeMode("AltHold")
Looping_Safety(4000)

# Landing sequence
if not Script.SendRC(3, PWM_in, True)
	print 'Could not send channel 3 PWM_in'

while cs.alt > Start_alt:
	Safety_Check()

# Script.ChangeParam("LAND_SPEED", 30)
# Script.ChangeMode("Land")
# print 'Landing'
# while cs.alt > Start_alt:
# 	Safety_Check()

for chan in range(1,9):
	if not Script.SendRC(chan,0,True)
		print 'Could not set channel: %d to zero' % chan

print 'Copter Disarming'
MAV.doARM(False)

print 'Script Over'
