# Carie Navio
# Mission Planner Script
# Purpose: Waypoint script testing
# THIS DOES NOT INCLUDE THE UNLINKING PORTION

# This will remain pretty much untouched because we know how it works
# so if we run into issues, this program will help determine if they
# are code based, or hardware based.

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
Script.SendRC(3,1550,True)
while cs.alt < 1:
	cs.verticalspeed = 0.30					# while altitude is less than (m)?
	Safety_Check()
	Script.Sleep(50)

print 'Copter slowing to 4 m'
Script.SendRC(3,1500,True)
while cs.alt < 2:
	cs.verticalspeed = 0.20
	Safety_Check()
	Script.Sleep(50)

print 'Copter slowing to 5 m'
while cs.alt < 4:
	cs.verticalspeed = 0.1
	Safety_Check()
	Script.Sleep(50)

# it will maintain just under 5 m / 16 ft 
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
