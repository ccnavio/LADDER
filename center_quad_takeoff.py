# Mostly Carie Navio / A little Jonathan Markel
# Mission Planner Script
# Purpose: Autonomous throttle update
# THIS DOES NOT INCLUDE THE UNLINKING PORTION

# Safety_Check definition takes no inputs. It reads channel 7,
# which is initially set to low, and waits for a high signal from
# the controller. This will send all channels an input value of 0
# which will relinquish control from the script. The exit() doesn't 
# actually exit. It will create an error from the mission planner side
# but this doesn't do anthing as far the code goes. This can be changed
# but it would mostly be cosmetic.
def Safety_Check():
	if cs.ch7in > 1800:
		for chan in range(1,9):
			Script.SendRC(chan,0,True)
		Script.Sleep(25)
		print 'Safety Override'
		f.write("Safety Override")
		f.close()
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
print 'Copter arming'
#Copter wont arm again if left in althold from previous run
Script.ChangeMode("Stabilize")
Script.Sleep(50)
MAV.doARM(True)
Looping_Safety(2000)

Start_alt = cs.alt
rel_alt = 0

# Switch deadband (THR_DZ) to 10%
# A value of 100 means deadband is 10% above and below 50% 
# throttle (40%-60% throttle will trigger alt hold)
Script.ChangeParam("THR_DZ", 100)

#Max speed the pilot may request, in cm/s from 50 to 500.
Script.ChangeParam("PILOT_VELZ_MAX", 50)

# TAKEOFF
print('Taking off')
Script.ChangeMode("AltHold")
while rel_alt < 2:
	Script.SendRC(3,1900,True)
	rel_alt =  cs.alt - Start_alt
	Safety_Check()

# HOVER
# Hold altitude by throttling to deadband

# Will this run if the values vary?
Script.SendRC(3,1550,True)
print('Hold altitude for 6 sec')
Looping_Safety(6000)
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

print 'Script Over'