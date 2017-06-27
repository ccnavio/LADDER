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
# 7 Safety_check
# 8 empty 
# 9 epm activation 

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

# NOTE: Can change this alt depending where 0 is
# This needs a little more modification possibly.
def Landing(PWM_in):
	while cs.alt > 0.1:
		Script.SendRC(3, PWM_in, True)
		cs.verticalspeed = -0.2
		while PWM_in > 1350:
			if cs.verticalspeed < -0.25:
				PWM_in = PWM_in + 1
			elif cs.verticalspeed >= -0.2:
				Looping_Safety(100)
				PWM_in = PWM_in - 1 
		Safety_Check()

# The Takeoff defition takes two values: PWM_in and wanted_h.
# PWM_in is predefined in the setup, currently set to 1400 but
# subject to change if physical needs better meet other requirements.
# Curently, this code is optimized for the height of 3m, getting 
# about 0.1 above 3m. wanted_h can be changed but has proved to be off
# significantly more when the value is less than 3 and at 4, it 
# yields a value of approx. 4.14m.

# Currently, the max the PWM_in can be initially is 1600 because it 
# shouldnt' take more than 1600 to start takeoff. But this can be changed
# or deleted entirely. This is more for safety.

# Elif while loop takes in the check value because the copter might Over
# correct and not continue to rise. Through testing this has proved to be
# be an issue and has been mitigated through the use of the check which will 
# slowly increase the PWM_in value when it reads that we have not yet met the
# height we wanted. 
def Takeoff(PWM_in, wanted_h):
	print 'Taking off'
	while cs.alt < .25:
		cs.verticalspeed = 0.3
		Script.SendRC(3, PWM_in, True)
		if PWM_in < 1600:
			Looping_Safety(100)
			PWM_in = PWM_in + 1
		Safety_Check()

	print 'Climb 2/3 height'
	while cs.alt < wanted_h*2/3.0:
		cs.verticalspeed = 0.2
		Script.SendRC(3, PWM_in, True)
		if cs.verticalspeed > wanted_h*2/30.0 + 0.1:
			PWM_in = PWM_in - 1
			print 'decreasing PWM'
		Safety_Check()

	print 'Slowing down'
	check = 0
	cs.verticalspeed = 0.1
	while cs.alt < wanted_h:
		Script.SendRC(3, PWM_in, True)
		if cs.verticalspeed > 0.2:
			Looping_Safety(100)
			PWM_in = PWM_in - 1
			print 'decreasing PWM'
		elif check == 150:		 
			check = 0					
			PWM_in = PWM_in + 10
			print 'inceasing PWM'
		check = check + 1
		Safety_Check()
	Safety_Check()

# --------------------------------- MAIN PROGRAM --------------------------------- #
print 'Starting Script'
# implement for all channels from 1-9
PWM_in = 0

for chan in range(1,5):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

print 'Initializing 6-?? to False'
for chan in range (6,14):
	Script.SendRC(chan,0,False)
	Script.SendRC(3,Script.GetParam('RC3_MIN'), True)

print 'Copter arming'
MAV.doARM(True)
Looping_Safety(2000)
PWM_in = 1400

Script.SendRC(5,1200,True)					# This should be Loiter

# 3m = about 10ft
Takeoff(PWM_in, 3)

Script.SendRC(5,1400,True)
print 'PosHold copter'
print PWM_in
Looping_Safety(5000)

print 'Starting to Land'
print PWM_in
Landing(PWM_in)

print 'Copter disarmed'
MAV.doARM(False)

for chan in range(1,9):
	Script.SendRC(chan,0,True)

print 'Done'
