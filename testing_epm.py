# Carie Navio
# Mission Planner Script
# Purpose: Waypoint script testing
# THIS DOES NOT INCLUDE THE UNLINKING PORTION

# 1 roll
# 2 pitch
# 3 throttle
# 4 yaw
# 5 flight modes
# 6 empty
# 7 autotune (?)
# 8 empty (?)
# 9 epm activation 

# safety switch on radio 7
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

print 'Maintain position 3s'
Looping_Safety(3000)

# Unlinking will last for 2 seconds
# EPM ON CHANNEL 9
print 'Wait for unlinking 2s'
cs.ch9out = 1800
Looping_Safety(2000)
cs.ch9out = 0

# This will last 3 seconds
print 'Maintain position 3s'
Looping_Safety(3000)

print 'Done'