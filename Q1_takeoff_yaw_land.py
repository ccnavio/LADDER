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
		f.close()
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

def Control_Yaw(init_yaw, pitch_pwm):
	delta_time = 0.1
	accum_error = 0
	last_error = 0
	Kp = 0.135
	Ki = 0.09
	Kd = 0.0036
	count = 0
	print 'In Control Yaw'
	f.write("In Control Yaw\n")
	f.write("Init: %d\n" % init_yaw)

	while cs.ch8in < 1800:	
		print 'While loop'
		# f.write("Input: %d " % cs.yaw)
		error = cs.yaw - init_yaw	
		f.write("%d " % error)
		# Sets max angle the quad will try to correct for, if reached it aborts to user control
		# if abs(error) > 45:
		# 	cs.ch7in = 1900
		# 	print "Control_Yaw Aborted: Exceeded Max Angle"
		# 	f.write("Aborted")

		# # yaw correction function and updates pitch of Q1 
		if abs(error) > 2: 
			accum_error += error * delta_time
			der_error = (error - last_error)/delta_time
			output = (error * Kp) + (accum_error * Ki) + (der_error * Kd)
			last_error = error

			# f.write("Output: %d\n" % output)
			pitch_pwm += -output*0.5 

			if pitch_pwm > Script.GetParam('RC2_MAX'):
				pitch_pwm = Script.GetParam('RC2_MAX')
			elif pitch_pwm < Script.GetParam('RC2_MIN'):
				pitch_pwm = Script.GetParam('RC2_MIN')

		Script.SendRC( 2, pitch_pwm, True)
		f.write("%d \n" % pitch_pwm)		
		Script.Sleep(100)
		Safety_Check()


# ---------------------------- MAIN PROGRAM ---------------------------- #
# Takeoff parameters
save_path = "c:/Users/cnavio/Desktop/Logs/T1_testing/"
file_name = time.strftime("%m-%d-%Y_%H-%M-%S")
complete_path = save_path+file_name+".txt"

f = open(complete_path, "w")

Script.ChangeMode("Stabilize")
print 'Starting Script'
# implement for all channels from 1-9
for chan in range(1,5):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

print 'Initializing 6-9 to False'
for chan in range (6,9):
	Script.SendRC(chan,0,False)
	Script.SendRC(3,Script.GetParam('RC3_MIN'), True)

Start_alt = cs.alt
init_yaw = cs.yaw
pitch_pwm = cs.ch2in # pitch
PWM_in = 1580 # Jonathan's copter. Find throttle value

Looping_Safety(2000)
print 'Copter should start arming'
MAV.doARM(True)

Looping_Safety(2000)
print 'Copter should be armed'				

# Takeoff parameters of left_quad would include this:
# If it's in stabilize, the roll and pitch will level
# out on their own. 
print init_yaw
Script.SendRC(3, PWM_in, True)
Control_Yaw(init_yaw, pitch_pwm)
print 'Exit Control_Yaw'

# The degree of roll initially is very dependent on the pixhawk itself.
# The degree of roll should be taken into consideration pre-flight and
# monitor the movement of the pixhawk. As the pixhawk moves, the roll
# degree changes accordingly. As of now, the angle of degree change will
# be set to 5 before wanting to fix the displacement.

for chan in range(1,9):
	Script.SendRC(chan,0,True)

MAV.doARM(False)
print 'Copter Disarmed'
f.close()
print 'Script Over'
