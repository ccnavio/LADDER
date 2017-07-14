# Mostly Carie Navio / A little Jonathan Markel
# Mission Planner Script
# Purpose: Autonomous throttle and unlinking

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

#--------------------------------------------------------------------------------------------
print 'Starting Script'
# implement for all channels from 1-9
for chan in range(1,5):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

print 'Initializing 6-9 to False'
for chan in range (6,9):
	Script.SendRC(chan,0,False)
	Script.SendRC(3,Script.GetParam('RC3_MIN'), True)

Script.ChangeParam("RC9_FUNCTION", 0)
Script.ChangeParam("RC10_FUNCTION", 0)

Script.ChangeMode("Stabilize")
Script.Sleep(50)

print 'Copter arming'
#Copter wont arm again if left in althold from previous run
MAV.doARM(True)
Looping_Safety(2000)

Start_alt = cs.alt
rel_alt = 0

# Switch deadband (THR_DZ) to 10%
# A value of 100 means deadband is 10% above and below 50% 
# throttle (40%-60% throttle will trigger alt hold)
Script.ChangeParam("THR_DZ", 100)

#Max speed the pilot may request, in cm/s from 50 to 500.
Script.ChangeParam("PILOT_VELZ_MAX", 30)

# TAKEOFF
print('Taking off')
Script.ChangeMode("AltHold")
while rel_alt < 1.5:
	Script.SendRC(3,1900,True)
	rel_alt =  cs.alt - Start_alt
	Safety_Check()

# HOVER
# Hold altitude by throttling to deadband
Script.SendRC(3,1550,True)
print('Unlinking')

Looping_Safety(2000)
# MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 9, Script.GetParam('RC9_MAX'), 0, 0, 0, 0, 0) # Starts button
MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 9, Script.GetParam('RC9_MIN'), 0, 0, 0, 0, 0) # Stops button
MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 10, Script.GetParam('RC10_MIN'), 0, 0, 0, 0, 0) # Stops button
Looping_Safety(2000)
MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 9, 1500, 0, 0, 0, 0, 0) # returns to neut
MAV.doCommand(MAVLink.MAV_CMD.DO_SET_SERVO, 10, 1500, 0, 0, 0, 0, 0) # returns to neut
Looping_Safety(1000)

# LANDING
# LAND_SPEED = descending speed in cm/s from 30 - 200.
# If descending from above 10m modify the WPNAV_SPEED_DN parameter

Script.ChangeParam("LAND_SPEED", 30)
Script.ChangeMode("Land")
print 'Landing'
while cs.alt > Start_alt:
	Safety_Check()

for chan in range(1,9):
	Script.SendRC(chan,0,True)

Script.ChangeParam("RC9_FUNCTION", 1)
Script.ChangeParam("RC10_FUNCTION", 1)

MAV.doARM(False)
print 'Copter Disarmed'
print 'Script Over'
