# Carie Navio / Jonathan Markel
# LADDER Team 2017
# Q1, right side, yaw control
# NEEDS TO BE TESTED ON THE COPTER
# PID NEEDS TO BE ADJUSTED

import sys, clr
clr.AddReference("MissionPlanner")
clr.AddReference("MAVLink")
import MAVLink, math, time, MissionPlanner

# This function will return all control back to the safety
# pilot if radiso channel 7 is flipped over a certain value
def Safety_Check(kill):
	if (cs.ch7in > 1800) or kill:
		for chan in range(1,5):
			if not Script.SendRC(chan,0,True):
				print 'SAFETY CHECK: Channel %d failed!' % chan
		if not Script.ChangeMode("Stabilize"):
			print 'SAFETY CHECK: Failed to switch to stabilize'
		print 'Safety Check Engaged'
		for chan in range(6,9):
			if not Script.SendRC(chan,0,True):
				print 'SAFETY CHECK: Channel %d failed!' % chan
		sys.exit()
	else:
		return 0

# This function replaces the Script.Sleep function. It allows
# the safety pilot to regain control if while the copter is waiting
# for x amount of time and something happens during testing.
def Looping_Safety(time):
	loop_var = 0
	while loop_var < time/25:
		Safety_Check(kill)
		loop_var = loop_var + 1
		Script.Sleep(25)

# This function initializes all necessary RC channels. 1-5 are over-written
# by the script while channel 6-9 is not. What ever channel is the safety
# switch cannot have the PWM value over 0, or else you will not regain 
# control of the copter even if you flip the switch.
def Initialize():
	print 'Initializing RC channels'
	for chan in range(1,5):
	    if not Script.SendRC(chan,1500,False):
			print 'Could NOT send 1500 to channel: %d' % chan
	    if not Script.SendRC(3,Script.GetParam('RC3_MIN'),True):
			print 'Could NOT send minimum value to channel: %d' % chan

	for chan in range (6,9):
		if not Script.SendRC(chan,0,False):
			print 'Could NOT set channel: %d to zero' % chan

# This function checks certain parameters in which we see is the safest
# environment for our copters to fly in. The values may change depending
# on which copter/axis of control you are assigned to. If any of the
# values exceed the safety, the safety pilot will automatically regain control
# of its copter. 
def Check_Status(rel_alt, kill, start_alt):
	Safety_Check(kill)
	if cs.climbrate > .75:
		print 'Exceeded max climbrate. Climbrate = %f m/s.' % cs.climbrate
		Safety_Check(True)

	elif abs(cs.roll) > 15:
		print 'Exceeded max roll. Roll = %f degrees.' % cs.roll
		Safety_Check(True)

	elif abs(cs.pitch) > 15:
		print 'Exceeded max pitch. Pitch = %f degrees.' % cs.pitch
		Safety_Check(True)

	elif rel_alt > 2.5:
		print 'Exceeded relative altitude of 2m. Rel_alt = %f m.' % rel_alt
		Safety_Check(True)

	else:
		kill = False
		return 0

# This function occurs right after the signal from the pi has been sent to
# change the mode in which the two quadcopters are in. This will exit the PID
# loop but we need to ensure that the mode was correctly changed since we 
# might have issues with commands sending but not getting received. 
def Mode_Check(thr_in, kill):
	if cs.mode == 'AltHold':
		Safety_Check(kill)
		print cs.mode
		if cs.ch3in > 1700 or cs.ch3in < 1400:
			if not Script.SendRC(3, thr_in, True):
				print 'Thr in failed - see Mode_Check'
				kill = True
				Safety_Check(kill)
	else:
		print 'ALERT: NOT IN ALTHOLD'
		kill = True
		Safety_Check(kill)

def Control_Yaw(init_yaw, pitch_pwm, start_alt, unlinking_alt, rel_alt, thr_in):
	print 'In Control_Yaw'
	kill = False
	start_alt = cs.alt
	mid_pitch = pitch_pwm
	Check_Status(rel_alt, kill, start_alt)
	rc_2_min = Script.GetParam('RC2_MIN')
	rc_2_max = Script.GetParam('RC2_MAX')
	delta_time = 0.1
	accum_error = 0
	last_error = 0

	Kp = 5  # Proportional
	Ki = 2  # Integral
	Kd = 2  # Derivative

	while cs.mode == 'Stabilize':
		Check_Status(rel_alt, kill, start_alt)
		rel_alt = cs.alt - start_alt

		if rel_alt > (unlinking_alt + 0.5):
			print 'Exceeded %fm' % (unlinking_alt + 0.3)
			kill = True
			Safety_Check(kill)

	 	error = (180/math.pi)* math.asin(math.sin((cs.yaw - init_yaw)*(math.pi/180)))
		print "Error: %d" % error
		print 'Relative altitude %f' % rel_alt
		Check_Status(rel_alt, kill, start_alt)

		if abs(error) >= 60:
			print 'Exceeded 45 degrees yaw'
			kill = True
			Safety_Check(kill)

		elif abs(error) > 1:
			accum_error += error * delta_time
			der_error = (error - last_error)/delta_time
			output = (error * Kp) + (accum_error * Ki) + (der_error * Kd)
			last_error = error

			pitch_pwm = mid_pitch - output*0.5

		Check_Status(rel_alt, kill, start_alt)

		if pitch_pwm > rc_2_max:
			pitch_pwm = rc_2_max - 50
		elif pitch_pwm < rc_2_min:
			pitch_pwm = rc_2_min + 10

		print 'CH2 In: %d' % pitch_pwm
		if not Script.SendRC( 2, pitch_pwm, True):
			print 'Channel 2 input failed to send'

	Mode_Check(thr_in, kill)
	print 'Mode changed - happily exiting Control_Yaw'
	Check_Status(rel_alt, kill, start_alt)

def Manual_Arm():
	yaw_center = cs.ch4in
	Script.SendRC(3,992,True)
	Script.SendRC(4,2015,True)
	Looping_Safety(5000)
	if cs.armed == False:
		print 'Manual arm failed'
		print 'Check safety switch or reboot pixhawk'
		kill = True
		Safety_Check(kill)
	else:
		Script.SendRC(4,yaw_center,True)
		while cs.ch4in != yaw_center:
			Looping_Safety(50)
			print 'Yaw not aligned, please wait'

# ************************ MAIN PROGRAM *********************** #
pitch_pwm = cs.ch2in
start_alt = cs.alt
init_yaw = cs.yaw
kill = False
rel_alt = cs.alt - start_alt

# A value of 100 means deadband is 10% above and below 50%
if not Script.ChangeParam("THR_DZ", 100):
	print 'Deadband parameter change failed, aborting'
	kill = True
	Safety_Check(kill)
# Max speed the pilot may request, in cm/s from 50 to 500.
if not Script.ChangeParam("PILOT_VELZ_MAX", 50):
	print 'Max vel. parameter change failed, aborting'
	kill = True
	Safety_Check(kill)
# Descending speed in Land mode in cm/s from 30-200
if not Script.ChangeParam("LAND_SPEED", 30):
	print 'Landing speed parameter change failed, aborting'
	kill = True
	Safety_Check(kill)

# ONLY CHANGE THESE VARIABLES --------------------------------- #

thr_in = 1615
unlinking_alt = 1.5 # BE SURE TO CHANGE ON ALL 3 VEHICLES

# ------------------------------------------------------------- #
Initialize()

if cs.mode != 'Stabilize':
	print 'Incorrect flight mode. Switch to Stabilize.'
	kill = 1

print 'Arming'
if MAV.doARM(True):
	print 'Armed'
	Check_Status(rel_alt, kill, start_alt)
	Safety_Check(kill)
elif cs.armed == True:
	print 'Already Armed'
elif cs.armed == False:
	print 'Attempting to manually arm'
	Manual_Arm()

# ------------------------- TAKEOFF --------------------------- #
Check_Status(rel_alt, kill, start_alt)

print '3 seconds, get ready'
Looping_Safety(3000)
print 'Throttling up to 1580'
Looping_Safety(1000)

if not Script.SendRC(3, thr_in, True):
	print 'Failed to send throttle up command'
	kill = True
	Safety_Check(kill)

#Preventing error buildup in the PID tuner
rel_alt = cs.alt - start_alt
while rel_alt < 0.2 and cs.climbrate < 0.15:
	print 'bloop'
	rel_alt = cs.alt - start_alt
	Looping_Safety(100)
	Safety_Check(kill)
	print 'rel_alt is = %f ' % rel_alt
	print 'The climbrate is = %f ' % cs.climbrate

Control_Yaw(init_yaw, pitch_pwm, start_alt, unlinking_alt, rel_alt, thr_in)
Mode_Check(thr_in, kill)

#Rolling To The Right After Unlinking
if cs.mode == 'AltHold':
    Script.SendRC(1,1249,True)

    while cs.groundspeed < 0.4:
        Safety_Check(kill)
        print 'Vehicle rolling left'
        print 'GroundSpeed is %f' % cs.groundspeed

    Script.SendRC(1,1504,True)
    print 'Finished rolling, proceeding to land'

print 'Landing in 7 seconds'
Looping_Safety(7000)
print 'Finished Looping safety'

# ------------------------- LANDING --------------------------- #

if not Script.ChangeMode("Land"):
	print 'Failed to enter landing mode, returning user control'
	Safety_Check(True)

final_mode = cs.mode
if final_mode != 'Land':
	print 'Not in land mode'
	Script.ChangeMode("Land")

while cs.landed == False:
	print 'Landing'
	Safety_Check(kill)

for chan in range(1,9):
	Check_Status(rel_alt, kill, start_alt)
	if not Script.SendRC(chan,0,True):
		print 'Could not set channel: %d to zero' % chan

if MAV.doARM(False):
	print 'Disarmed'
else:
	print 'Warning! Failed to disarm'
