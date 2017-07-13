# Carie Navio
# Mission Planner Script
# Purpose: Autonomous throttle update
# THIS DOES NOT INCLUDE THE UNLINKING PORTION

import time

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

# NOTE: Can change this alt depending where 0 is
# This needs a little more modification possibly.
def Landing(PWM_in, Start_alt):
	PWM_in = PWM_in - 25
	while cs.alt - Start_alt > 0.1:
		# while PWM_in > 1400:
		Script.SendRC(3, PWM_in, True)
		cs.verticalspeed = -0.2
		if cs.verticalspeed < -0.25:
			PWM_in = PWM_in + 1
		else:
			Looping_Safety(100)
			PWM_in = PWM_in - 1
		Safety_Check()
		f.write("%d\n" % PWM_in)			##	

def Landing_Auto(Start_alt):
	Script.ChangeParam("LAND_SPEED", 30)
	Script.ChangeMode("Land")
	print 'Landing'
	while cs.alt > Start_alt:
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

# In this version of the code, the startup altitude does not have to be 0. It 
# will call from what that height is and basically set that height to zero, so 
# if the copters are not at the same altitude, they should still fly approximately 
# the same height from their given cs.alt. 
def Takeoff(PWM_in, wanted_h, Start_alt):
	print 'Taking off'
	f.write("Taking off\n")						##
	while cs.alt - Start_alt < .25:
		Script.SendRC(3, PWM_in, True)
		if cs.verticalspeed < 0.2:
			Looping_Safety(100)
			PWM_in = PWM_in + 1
		Safety_Check()
		f.write("%d\n" % PWM_in)				##

	print 'Climb 2/3 of wanted height'
	f.write("Climb 2/3 of wanted height\n")		##
	while cs.alt - Start_alt < wanted_h*2/3.0:
		cs.verticalspeed = 0.2
		Script.SendRC(3, PWM_in, True)
		if cs.verticalspeed > wanted_h*2/30.0 + 0.1:
			PWM_in = PWM_in - 1
			print '1. Decreasing PWM'
		Safety_Check()
		f.write("%d\n" % PWM_in)				##

	print 'Slowing down'
	f.write("Slowing down\n")					##
	check_slowdown = check_speedup = 0
	cs.verticalspeed = 0.15
	while cs.alt - Start_alt < wanted_h:
		Script.SendRC(3, PWM_in, True)
		if cs.verticalspeed > 0.25:
			check_slowdown = check_slowdown + 1
			if check_slowdown == 10:
				PWM_in = PWM_in - 1
				check_slowdown = 0
			print check_slowdown
			print '2. Decreasing PWM'
		elif cs.verticalspeed < 0.1 and cs.alt-Start_alt < wanted_h-0.5:		 
			check_speedup = check_speedup + 1
			if check_speedup == 150:					
				PWM_in = PWM_in + 10
				print '2. Inceasing PWM'
				check_speedup = 0
			print check_speedup
		Safety_Check()
		f.write("%d\n" % PWM_in)				##
	Safety_Check()

# --------------------------------- MAIN PROGRAM --------------------------------- #
save_path = "c:/Users/cnavio/Desktop/Logs/update_throttle/"
file_name = time.strftime("%m-%d-%Y_%H-%M-%S")
complete_path = save_path+file_name+".txt"
print complete_path
f = open(complete_path, "w")

print 'Starting Script update_throttle'
f.write("Starting Script update_throttle\n")	##

PWM_in = Start_alt = 0

Start_alt = cs.alt
print Start_alt
f.write("Start_alt %d\n" % Start_alt)			##

Script.ChangeMode("Stabilize")
for chan in range(1,5):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

print 'Initializing 6-14 to False'
for chan in range (6,14):
	Script.SendRC(chan,0,False)
	Script.SendRC(3,Script.GetParam('RC3_MIN'), True)

print 'Copter arming'
f.write("Copter arming\n")						##
MAV.doARM(True)
Looping_Safety(2000)
PWM_in = 1500

# 3m = about 10ft
Takeoff(PWM_in, 2, Start_alt)

Script.SendRC(5,1400,True)
print 'PosHold copter'
f.write("PosHolding\n")							##
print PWM_in
f.write("%d\n" % PWM_in)						##
Looping_Safety(5000)

print 'Starting to Land'
f.write("Starting to Land\n")

# Script.SendRC(5, 1800, True)

# Landing(PWM_in, Start_alt)

Landing_Auto(Start_alt)

print 'Copter disarmed'
f.write("Copter disarmed\n")					##
MAV.doARM(False)

for chan in range(1,9):
	Script.SendRC(chan,0,True)

print 'Done'
f.close()										##