# Carie Navio
# Mission Planner Script
# Purpose: Bare bones code

# 1 roll
# 2 pitch
# 3 throttle
# 4 yaw
# 5 flight modes
# 6 empty
# 7 autotune (?)
# 8 empty (?)
# 9 epm activation 

# Checks for controller switch to manual
def Safety_Check():
	if cs.ch7in > 1800:
		for chan in range(1,9):
			Script.SendRC(chan,0,True)
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
# implement for all channels from 1-5 
# to control copter flight
for chan in range(1,5):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

# initialize switches for other modes 
# this can be changed per use
# setting to 0 = flight controller
# setting to 1500 = script has control
print 'Initializing 6-14 to False'
for chan in range (6,14):
	Script.SendRC(chan,0,False)
	Script.SendRC(3,Script.GetParam('RC3_MIN'), True)

# safety buffer before and after armed
Looping_Safety(2000)
print 'Copter should start arming'
MAV.doARM(True)
Looping_Safety(2000)
print 'Copter should be armed'				

# INSERT CODE HERE

# disarming copter
MAV.doARM(False)
print 'Copter Disarmed'

# giving all control back to pilot
for chan in range(1,14):
	Script.SendRC(chan,0,False)

print 'Script Over'
