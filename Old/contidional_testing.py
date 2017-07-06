# Carie Navio
# Mission Planner Script
# Purpose: Waypoint script testing
# THIS DOES NOT INCLUDE THE UNLINKING PORTION

import clr
clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MAVLink")
import MAVLink

def Safety_Check():
	if cs.ch7in > 1800:
		for chan in range(1,9):
			Script.SendRC(chan,0,True)
		Script.Sleep(25)
		print 'Safety Override'
		exit()
	else:
		return 0

def Looping_Safety(time):
	loop_var = 0
	while_var = 0
	while_var = time/50
	while loop_var < while_var:
		Safety_Check()
		Script.Sleep(50)
		loop_var = loop_var + 1
	print 'End Safety Loop'

# --------------------------------- MAIN PROGRAM --------------------------------- #
print 'Starting Script'
# implement for all channels from 1-9
for chan in range(1,5):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

print 'Initializing 6-9 to False'
for chan in range (6,9):
	Script.SendRC(chan,0,False)
	Script.SendRC(3,Script.GetParam('RC3_MIN'), True)

Looping_Safety(2000)
print 'Copter should start arming'
MAV.doARM(True)

Looping_Safety(2000)
print 'Copter should be armed'	
# When initialized, the copter is set to Stabilize
# Throttle PWM values will change for our specific copter

# start from much lower PWM, the SITL only goes up when
# the PWM is above 1500

print 'Starting takeoff'
# rate in cm/sec, 0,0,0,0,0, target alt

while cs.alt < 2:
	MAV.doCommand(MAVLink.MAV_CMD.CONDITION_CHANGE_ALT, 20, 0, 0, 0, 0, 0, 20) 

print 'Done takeoff'
# Make sure copter is stable before sending into althold
print 'PosHold copter'
Script.SendRC(5,1400,True)					# This should be PosHold
print 'Sleeping 5s'
Looping_Safety(2000)

print 'Finished AltHold'

# Fix this shit
Script.SendRC(3,1400,True)
while cs.alt > 0.1:
	Safety_Check()
	Script.Sleep(50)

MAV.doARM(False)
print 'Copter Disarmed'

for chan in range(1,9):
	Script.SendRC(chan,0,True)
# --------------------------------------------- #
print 'Script Over'
