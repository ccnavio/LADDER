# Carie Navio
# Mission Planner Script
# Purpose: Hover script linked slave
# THIS IS TESTING ON A QUAD

# 1 roll
# 2 pitch
# 3 throttle
# 4 yaw
# 5 flight modes
# 6 empty
# 7 autotune (?)
# 8 empty (?)
# 9 epm activation 

def Safety_Check():
	if cs.ch7in > 1800:
		for chan in range(1,9):
			Script.SendRC(chan,0,True)

		# Returns power back to the pilot 
		Script.Sleep(50)
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

# start from much lower PWM, the SITL only goes up when
# the PWM is above 1500

print 'Starting takeoff'
Script.SendRC(3,1250,True)
while cs.alt < 2:
	cs.verticalspeed = 0.4					# while altitude is less than (m)?
	Safety_Check()
	Script.Sleep(50)

print 'Copter slowing to 4 m'
Script.SendRC(3,1200,True)
while cs.alt < 4:
	cs.verticalspeed = 0.25
	Safety_Check()
	Script.Sleep(50)

print 'Copter slowing to 5 m'
while cs.alt < 5:
	cs.verticalspeed = 0.1
	Safety_Check()
	Script.Sleep(50)
											# it will maintain just under 5 m / 16 ft 
print 'AltHold copter'
Script.SendRC(5,1400,True)					# This should be AltHold

# Make sure we've stopped rising
print 'Maintain position 3s'
Looping_Safety(3000)

# Unlinking will last for 2 seconds
# EPM ON CHANNEL 9
print 'Wait for unlinking 2s'
#cs.ch9out = 1800
Looping_Safety(2000)
#cs.ch9out = 0

# This will last 3 seconds
print 'Maintain position 3s'
Looping_Safety(3000)

print 'Finished AltHold'
Script.ChangeMode("Stabilize")				# Return to stabilize mode
Script.SendRC(3,1100,True)
while cs.alt > 0.2:
	Safety_Check()
	Script.Sleep(50)

MAV.doARM(False)
print 'Copter Disarmed'

for chan in range(1,9):
	Script.SendRC(chan,0,False)

print 'Script Over'
