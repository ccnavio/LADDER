# Carie Navio / Jonathan Markel
# LADDER Team 2017
# Q3, left side, roll control
# NEEDS TO BE TESTED ON THE COPTER
# PID NEEDS TO BE ADJUSTED

# USER DEFINED FUNCTIONS
import sys,  clr
clr.AddReference("MissionPlanner")
clr.AddReference("MAVLink")
import MAVLink, math, time, MissionPlanner

def Safety_Check(kill):
	if cs.ch7in > 1800 or kill:
		for chan in range(1,5):
			if not Script.SendRC(chan,0,True):
				print 'SAFETY CHECK: Channel %d failed!' % chan
		if not Script.ChangeMode("Stabilize"):
			print 'SAFETY CHECK: Failed to switch to stabilize'
		print 'Safety Check Engaged'
		for chan in range(6,9):
			if not Script.SendRC(chan,0,True):
				print 'SAFETY CHECK: Channel %d failed!' % chan
				kill = False
		sys.exit()
	else:
		return 0

def Looping_Safety(time):
	loop_var = 0
	while loop_var < time/25:
		Safety_Check(kill)
		loop_var = loop_var + 1
		Script.Sleep(25)

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

def Check_Status(rel_alt, kill):
	Safety_Check(kill)
	if cs.climbrate > .75:
		print 'Exceeded max climbrate. Climbrate = %f m/s.' % cs.climbrate
		kill = True
		Safety_Check(kill)

	elif abs(cs.roll) > 25:
		print 'Exceeded max roll. Roll = %f degrees.' % cs.roll
		kill = True
		Safety_Check(kill)

	elif abs(cs.pitch) > 15:
		print 'Exceeded max pitch. Pitch = %f degrees.' % cs.pitch
		kill = True
		Safety_Check(kill)

	elif rel_alt > 2.5:
		print 'Exceeded relative altitude of 2m. Rel_alt = %f m.' % rel_alt
		kill = True
		Safety_Check(kill)

	else:
		return 0

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


def Control_Roll(init_roll, roll_pwm, start_alt, unlinking_alt, rel_alt):
	kill = False
	print 'In Control_Roll'
	Check_Status(rel_alt, kill)
	delta_time = 0.1
	accum_error = 0
	last_error = 0
	check = 0
	rc3_max = Script.GetParam('RC3_MAX')
	rc3_min = Script.GetParam('RC3_MIN')
	start_alt = cs.alt

	#This worked okay but was a little sloppy.

	Kp = 15 # Proportional
	Ki = 15   # Integral
	Kd = 2 # Derivative

	# may want to reset rel_alt before this loop to comp. for barometer fluct.
	while cs.mode == 'Stabilize':
		Check_Status(rel_alt, kill)
		Safety_Check(kill)
		rel_alt = cs.alt - start_alt
		print 'The Relative Altitude is %f ' % rel_alt

		if rel_alt > (unlinking_alt + 1.0):
			print 'Exceeded %fm' % (unlinking_alt + 1.0)
			kill = True
			Safety_Check(kill)

		# if rel_alt > unlinking_alt:
		# 	check += 1
		# 	if check == 15:
		# 		return 0
		# 		print 'Achieved constant alt, exiting control roll'

		error = cs.roll - init_roll

		if abs(error) >= 15:
			print 'Exceeded roll 15 degrees (from within control_roll)'
			kill = True
			Safety_Check(kill)

		elif abs(error) > 1:
			accum_error += error * delta_time
			der_error = (error - last_error)/delta_time
			output = (error * Kp) + (accum_error * Ki) + (der_error * Kd)
			last_error = error
			print error

			roll_pwm = 1460 - output*0.8
			print 'The roll_pwm is %f ' % roll_pwm
			Safety_Check(kill)

		if roll_pwm > rc3_max:
			roll_pwm = rc3_max - 100
			Safety_Check(kill)

		elif roll_pwm < rc3_min:
			roll_pwm = rc3_min + 100
			Safety_Check(kill)

		print 'Throttle input: %f' % roll_pwm
		Script.SendRC( 3, roll_pwm, True)

	Mode_Check(thr_in, kill)
	print 'Mode changed - happily exiting Control_Roll'
	Check_Status(rel_alt, kill)

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

# ONLY CHANGE THESE VARIABLES --------------------------------- #

thr_in = 1460
unlinking_alt = 1.5 # BE SURE TO CHANGE ON ALL 3 VEHICLES

# ------------------------------------------------------------- #

# ************************ MAIN PROGRAM *********************** #

start_alt = cs.alt
init_roll = cs.roll
roll_pwm = thr_in
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

Initialize()

if cs.mode != 'Stabilize':
	print 'Incorrect flight mode. Switch to Stabilize.'
	kill = 1

print 'Arming'
if MAV.doARM(True):
	print 'Armed'
	Check_Status(rel_alt, kill)
	Safety_Check(kill)
elif cs.armed == True:
	print 'Already Armed'
elif cs.armed == False:
	print 'Attempting to manually arm'
	Manual_Arm()

# ------------------------- TAKEOFF --------------------------- #
Check_Status(rel_alt, kill)

print '3 seconds, get ready'
Looping_Safety(3000)
print 'Throttling up to 1300'
Looping_Safety(1000)

if not Script.SendRC(3, 1300, True):
	print 'Failed to send throttle up command'
	kill = True
	Safety_Check(kill)

Looping_Safety(4000)
print 'Starting to control roll'
print 'Throttle mid set to 1460'

Control_Roll(init_roll, roll_pwm, start_alt, unlinking_alt, rel_alt)
Mode_Check(thr_in, kill)

# ------------------------- LANDING --------------------------- #
# wait_to_land = cs.timeInAir
print 'Landing in 7 seconds'
# while (cs.timeInAir - wait_to_land) < 7:
# 	Check_Status(rel_alt, kill)
# 	print (cs.timeInAir - wait_to_land)

Looping_Safety(7000)
print 'Finished Looping_Safety'

if not Script.ChangeMode("Land"):
	print 'Failed to enter landing mode, returning user control'
	kill = True
	Safety_Check(kill)

while cs.landed == False:
	print 'Landing'
	Safety_Check(kill)

for chan in range(1,9):
	if not Script.SendRC(chan,0,True):
		print 'Could not set channel: %d to zero' % chan

# Double check this functionality
if MAV.doARM(False):
	print 'Disarmed'
else:
	print 'Warning! Failed to disarm'
