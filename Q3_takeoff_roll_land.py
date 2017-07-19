# Mission Planner Script
# Purpose: LEFT SIDE QUAD, Q1

import math
import time

def Safety_Check():
	if cs.ch7in > 1800:
		Script.ChangeMode("Stabilize")
		for chan in range(1,9):
			Script.SendRC(chan,0,True)
		Script.Sleep(25)
		print 'Safety Override'
		exit()
	else:
		return 0

# Instead of Script.Sleep this will allow 
# safety loop to continue checking time in ms
def Looping_Safety(time):
	loop_var = 0
	while_var = 0
	while_var = time/50
	while loop_var < while_var:
		Safety_Check()
		Script.Sleep(50)
		loop_var = loop_var + 1
	print 'End Safety Loop'

# Is the leftside quad at a negative angle? 
# Take in a PWM value for throttle. You slowly increase throttle 
# until the angle of roll is about 2(?) degress off of your starting
# angle. At this point you should be in hover and then you wait for 
# a small alt change. 
def Takeoff(PWM_in, init_roll):
	while cs.roll < init_roll + 3:
		Safety_Check()
		PWM_in = PWM_in + 1
		if cs.roll > init_roll + 2:
			count_roll = count_roll + 1
			if count_roll == 10:
				return PWM_in

def Control_Roll(init_roll, roll_pwm, Start_alt):
	delta_time = 0.1
	accum_error = 0
	last_error = 0
	Kp = 0.135
	Ki = 0.09
	Kd = 0.0036
	check = 0
	print 'In Control Roll'

	# Change to 1.6?
	while cs.alt - Start_alt < 1.6:	

		if cs.alt - Start_alt > 1.3:
			check += 1
			if check == 15:
				return 0
				print 'Exiting check alt'

		print 'While loop'
		error = cs.roll - init_roll	
		Safety_Check()
		# # yaw correction function and updates pitch of Q1 
		if abs(error) > 2: 
			accum_error += error * delta_time
			der_error = (error - last_error)/delta_time
			output = (error * Kp) + (accum_error * Ki) + (der_error * Kd)
			last_error = error

			# f.write("Output: %d\n" % output)
			roll_pwm += -output*0.5 

			if roll_pwm > Script.GetParam('RC3_MAX'):
				roll_pwm = Script.GetParam('RC3_MAX') - 100
			elif roll_pwm < Script.GetParam('RC3_MIN'):
				roll_pwm = Script.GetParam('RC3_MIN') + 10

		print roll_pwm
		Script.SendRC( 3, roll_pwm, True)
		Safety_Check()

# --------------------------------- MAIN PROGRAM --------------------------------- #
# Takeoff parameters
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

Looping_Safety(2000)
print 'Copter should start arming'
MAV.doARM(True)

Looping_Safety(2000)
print 'Copter should be armed'				

# Takeoff parameters of Q3 would include this:
# If it's in stabilize, the roll and pitch will level
# out on their own. 

# The degree of roll initially is very dependent on the pixhawk itself.
# The degree of roll should be taken into consideration pre-flight and
# monitor the movement of the pixhawk. As the pixhawk moves, the roll
# degree changes accordingly. As of now, the angle of degree change will
# be set to 5 before wanting to fix the displacement.
print init_roll
Script.SendRC(3, PWM_in, True)
Control_Roll(init_roll, PWM_in, Start_alt)
print 'Exit Control_Roll'

# Script.SendRC(3, PWM_in, True)
Script.ChangeMode("AltHold")
Looping_Safety(4000)

# Landing sequence
# Script.ChangeParam("LAND_SPEED", 30)
# Script.ChangeMode("Land")
# print 'Landing'
# while cs.alt > Start_alt:
# 	Safety_Check()

while cs.landed == False:
	Script.SendRC(3, PWM_in, True)
	Safety_Check()

for chan in range(1,9):
	Script.SendRC(chan,0,True)

print 'Copter Disarming'
MAV.doARM(False)

print 'Script Over'
