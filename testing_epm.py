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

print 'Initializing 6-8 to False'
for chan in range (6,8):
	Script.SendRC(chan,0,False)
	Script.SendRC(3,Script.GetParam('RC3_MIN'), True)

print 'Initializing 9'
Script.SendRC(9,1500,False)
Script.SendRC(9,Script.SendRC('RC9_MIN'), True)

Looping_Safety(2000)
print 'Copter should start arming'
MAV.doARM(True)

print 'Maintain position 1s'
Looping_Safety(1000)

# EPM ON CHANNEL 9
print 'Wait for unlinking 2s'
Script.SendRC(9,Script.GetParam('RC9_MAX'),True)
print Script.GetParam('RC9_MAX')

Looping_Safety(2000)

Script.SendRC(9,Script.GetParam('RC9_MIN'),True)
print Script.GetParam('RC9_MIN')

print 'Maintain position 1s'
Looping_Safety(1000)

for chan in range(1,14):
	Script.SendRC(chan,0,True)

print 'Done'