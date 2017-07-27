# Carie Navio / Jonathan Markel
# LADDER Team 2017
# Q2, hexacopter, center
# NEEDS TO BE SITL TESTED

# USER DEFINED FUNCTIONS
import sys, clr
clr.AddReference("MissionPlanner")
clr.AddReference("MAVLink")
import MAVLink, math, time, MissionPlanner

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
	if cs.climbrate > .60:
		print 'Exceeded max climbrate. Climbrate = %f m/s.' % cs.climbrate
		kill = True
		Safety_Check(kill)

	elif abs(cs.roll) > 15:
		print 'Exceeded max roll. Roll = %f degrees.' % cs.roll
		kill = True
		Safety_Check(kill)

	elif abs(cs.pitch) > 15:
		print 'Exceeded max pitch. Pitch = %f degrees.' % cs.pitch
		kill = True
		Safety_Check(kill)

	elif rel_alt > 2:
		print 'Exceeded relative altitude of 2m. Rel_alt = %f m.' % rel_alt
		kill = True
		Safety_Check(kill)

	else:
		return 0
	
## FOR QUADACOPTERS
# def Mode_Check():
# 	if cs.mode == 'AltHold':
# 		Safety_Check(kill)
# 		print cs.mode
# 		if cs.ch3in > 1700 or cs.ch3in < 1400:
# 			if not Script.SendRC(3, thr_in, True):
# 				print 'Thr in failed - see Mode_Check'
# 				kill = True
# 				Safety_Check(kill)
# 	else:
# 		print 'ALERT: NOT IN ALTHOLD'
# 		kill = True
# 		Safety_Check(kill)

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
		Script.SendRC(4,yawcenter,True)
		while cs.ch4in != yaw_center:
			Looping_Safety(50)
			print 'Yaw not aligned, please wait'

# ************************ MAIN PROGRAM *********************** #
rel_alt = cs.alt - start_alt
pitch_pwm = cs.ch2in
start_alt = cs.alt
init_yaw = cs.yaw
kill = False
rc9_min = Script.GetParam('RC9_MIN')
rc10_min = Script.GetParam('RC10_MIN')

# Handing over EPM control to the script
Script.ChangeParam("RC9_FUNCTION", 0)
Script.ChangeParam("RC10_FUNCTION", 0)

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

thr_in = 1650
unlinking_alt = 1.0 # BE SURE TO CHANGE ON ALL 3 VEHICLES

# ------------------------------------------------------------- #

Initialize()

if cs.mode != 'AltHold':
	print 'Incorrect flight mode. Switch to AltHold.'
	kill = 1 
	Safety_Check(kill)

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

print 'Waiting 3 seconds before throttling up to 1650'
Looping_Safety(2000)
print 'Throttling up'
Looping_Safety(1000)

if not Script.SendRC(3, thr_in, True):
	print 'Failed to send throttle up command'
	kill = True
	Safety_Check(kill)

while rel_alt < unlinking_alt:
	print 'Relative altitude: %f' % rel_alt
	Check_Status(rel_alt, kill)

# --------------------- HOVER & UNLINK ------------------------ #
if not Script.SendRC(3,1500,True):
	print 'HOVER FAILED'
	kill = 1
	Safety_Check(kill)

hover_start = cs.timeInAir
print 'Hovering for 3 seconds'
while (cs.timeInAir - hover_start) < 3:
	Check_Status(rel_alt, kill)

# ADD DUMMY SET SERVO COMMAND TO TRIGGER ALTHOLD IN QUADS
# Looping_Safety(2000)
# Disengage EPM
unlink_start = cs.timeInAir
MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 9, rc9_min, 0, 0, 0, 0, 0)
MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 10, rc10_min, 0, 0, 0, 0, 0)
print 'Unlinked'
print 'Hold for 3 seconds'
while (cs.timeInAir - unlink_start) < 3:
	Check_Status(rel_alt, kill)

# Return to neutral
MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 9, 1500, 0, 0, 0, 0, 0)
MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 10, 1500, 0, 0, 0, 0, 0)
print 'EPM switch returned to neutral'

# ---------------------- CLOCKWISE TURN ---------------------- #
Check_Status(rel_alt, kill)
init_yaw = cs.yaw 
delta_yaw = 0
yaw_in_neut = cs.ch4in
print 'Initiating 60 degree CW turn'
# Check is cs.turnrate would be useful here for safety checking
while delta_yaw < 30:
	delta_yaw = (180/math.pi)* math.asin(math.sin((cs.yaw - init_yaw)*(math.pi/180)))
	print 'Delta Yaw = %f degrees' % delta_yaw
	Script.SendRC(4, yaw_in_neut + 50,True)
	Check_Status(rel_alt, kill)
print 'Slowing turn rate by 50%'
while delta_yaw < 60:
	delta_yaw = (180/math.pi)* math.asin(math.sin((cs.yaw - init_yaw)*(math.pi/180)))
	print 'Delta Yaw = %f degrees' % delta_yaw
	Script.SendRC(4, yaw_in_neut + 25,True)
	Check_Status(rel_alt, kill)
print 'Turn complete'
# ------------------------- LANDING --------------------------- #
print 'Switching to Land mode'

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