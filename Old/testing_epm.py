# Mostly Carie Navio / A little Jonathan Markel
# Mission Planner Script
# Purpose: Autonomous throttle update
# THIS DOES NOT INCLUDE THE UNLINKING PORTION

import clr
clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MAVLink")
import MAVLink

# Safety_Check definition takes no inputs. It reads channel 7,
# which is initially set to low, and waits for a high signal from
# the controller. This will send all channels an input value of 0
# which will relinquish control from the script. The exit() doesn't 
# actually exit. It will create an error from the mission planner side
# but this doesn't do anthing as far the code goes. This can be changed
# but it would mostly be cosmetic.
def Safety_Check():
	if cs.ch7in > 1800:
		Script.ChangeMode("Stabilize")
		# Script.ChangeParam("RC8_FUNCTION", 1)
		Script.ChangeParam("RC9_FUNCTION", 1)
		Script.ChangeParam("RC10_FUNCTION", 1)
		for chan in range(1,9):
			Script.SendRC(chan,0,True)
		Script.Sleep(25)
		print 'Safety Override'
		exit()
	else:
		return 0

# Looping_Safety defition takes one input, time which is given
# in milliseconds. The function replaces the Script.Sleep function
# while still allowing the user to regain control of the copter 
# even if the script is not doing anything. 
def Looping_Safety(time):
	loop_var = 0
	while_var = 0
	while_var = time/50
	while loop_var < while_var:
		Safety_Check()
		Script.Sleep(50)
		loop_var = loop_var + 1
	print 'End looping safety'

#--------------------------------------------------------------------------------------------
print 'Starting Script'
# implement for all channels from 1-9

Script.ChangeMode("Stabilize")

for chan in range(1,5):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

print 'Initializing 6-9 to False'
for chan in range (6,9):
	Script.SendRC(chan,0,False)
	Script.SendRC(3,Script.GetParam('RC3_MIN'), True)

# Script.ChangeParam("RC8_FUNCTION", 0)
Script.ChangeParam("RC9_FUNCTION", 0)
Script.ChangeParam("RC10_FUNCTION", 0)

print 'Copter arming'
Looping_Safety(1000)

MAV.doARM(True)

print 'Starting'
Looping_Safety(1000)
Script.SendRC(3, 1200, True)
# HOVER
# Hold altitude by throttling to deadband

print 'Unlinking'

# Looping_Safety(1000)
# Script.SendRC(8, Script.GetParam('RC8_MAX'), True)
# MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 9, Script.GetParam('RC9_MIN'), 0, 0, 0, 0, 0) # Stops button
# MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 10, Script.GetParam('RC10_MIN'), 0, 0, 0, 0, 0) # Stops button
# Looping_Safety(2500)
# MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 9, 1500, 0, 0, 0, 0, 0) # returns to neut
# MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 10, 1500, 0, 0, 0, 0, 0) # returns to neut
# Script.SendRC(8, Script.GetParam('RC8_MIN'), True)
# print 'Unlinking complete'
# # LANDING
# LAND_SPEED = descending speed in cm/s from 30 - 200.
# If descending from above 10m modify the WPNAV_SPEED_DN parameter
Looping_Safety(2000)
# LANDING
# LAND_SPEED = descending speed in cm/s from 30 - 200.
# If descending from above 10m modify the WPNAV_SPEED_DN parameter

# Script.ChangeParam("LAND_SPEED", 30)
# Script.ChangeMode("Land")
# print 'Landing'
# while cs.alt > Start_alt:
# 	Safety_Check()

while cs.landed == False:
	Script.SendRC(3, 1200, True)
	Safety_Check()

for chan in range(1,9):
	Script.SendRC(chan,0,True)

# Script.ChangeParam("RC8_FUNCTION", 1)
Script.ChangeParam("RC9_FUNCTION", 1)
Script.ChangeParam("RC10_FUNCTION", 1)

print 'Copter Disarming'
MAV.doARM(False)
print 'Script Over'
