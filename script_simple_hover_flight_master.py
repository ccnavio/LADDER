# Carie Navio
# Mission Planner Script
# Purpose: Hover script linked master
# THIS IS TESTING ON A QUAD
# Used for Quad 1
# Need to start in Loiter

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

print 'Starting takeoff'
Script.SendRC(3,1675,True)					# 1680 - 1700/1715
while cs.sonarrange < 0.50:
	print cs.sonarrange
	cs.verticalspeed = 0.1					# while altitude is less than (m)?
	Safety_Check()
	#Script.Sleep(50)

# print 'Copter slowing to 4 m'
# while cs.sonarrange < 1.5:
# 	print cs.sonarrange
# 	cs.verticalspeed = 0.1
# 	Safety_Check()
	#Script.Sleep(50)

# print 'Copter slowing to 5 m'
# while cs.alt < 3:
# 	cs.verticalspeed = 0.1
# 	Safety_Check()
# 	Script.Sleep(50)
# ------------------------------------------#
											# it will maintain just under 5 m / 16 ft 
print 'AltHold copter'
Script.SendRC(5,1400,True)					# This should be AltHold

# Make sure we've stopped rising
print 'Maintain position 3s'
Looping_Safety(1000)

# EPM ON CHANNEL 9
print 'Copter disconnect EPM'
# MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 9, Script.GetParam('RC9_MAX'), 0, 0, 0, 0, 0) # Starts button
MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 9, Script.GetParam('RC9_MIN'), 0, 0, 0, 0, 0) # Stops button
Looping_Safety(500)
MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 9, 1500, 0, 0, 0, 0, 0) # returns to neut

# This will last 3 seconds
# print 'Maintain position 3s'
# Looping_Safety(1000)

print 'Finished AltHold'
Script.ChangeMode("Stabilize")				# Return to stabilize mode
Script.SendRC(3,1675,True)					# 1575		
while cs.sonarrange > 0.05:
	Safety_Check()
	Script.Sleep(50)

MAV.doARM(False)
print 'Copter Disarmed'

for chan in range(1,9):
	Script.SendRC(chan,0,True)

print 'Script Over'

# ------------------------------------
# Script.ChangeParam('RC9_FUNCTION', 0) #disables user control to allow auto

# print 'Engaging EPM'
# MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 9, Script.GetParam('RC9_MAX'), 0, 0, 0, 0, 0) #engages
# MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 9, 1500, 0, 0, 0, 0, 0) # switch at neutral
# Script.Sleep(5000)

# print 'Disengaging EPM'
# MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 9, Script.GetParam('RC9_MIN'), 0, 0, 0, 0, 0) 
# MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 9, 1500, 0, 0, 0, 0, 0) # switch at neutral
# Script.Sleep(5000)

# Script.ChangeParam('RC9_FUNCTION', 1) #should return user control
# ------------------------------------