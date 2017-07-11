# Carie Navio
# Mission Planner Script
# Purpose: LEFT SIDE QUAD, Q1

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
# NOTE!!!!!!!!!!!!!!!!!
# Can't use stabilize, consider using alt_hold or loiter
# Takeoff parameters
init_roll = roll_count = 0
print "Initial roll: %d" % cs.roll
print "PWM_in: %d" % PWM_in
init_roll = cs.roll

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

Looping_Safety(2000) b bnm, 
print 'Copter should be armed'				


# NOT WRITTEN YET









# Takeoff parameters of left_quad would include this:
# If it's in stabilize, the roll and pitch will level
# out on their own. 

PWM_in = Rolling_Check(PWM_in, init_roll)

# The degree of roll initially is very dependent on the pixhawk itself.
# The degree of roll should be taken into consideration pre-flight and
# monitor the movement of the pixhawk. As the pixhawk moves, the roll
# degree changes accordingly. As of now, the angle of degree change will
# be set to 5 before wanting to fix the displacement.

MAV.doARM(False)
print 'Copter Disarmed'

for chan in range(1,9):
	Script.SendRC(chan,0,True)

print 'Script Over'
