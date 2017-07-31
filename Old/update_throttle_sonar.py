# Carie Navio
# Mission Planner Script
# Purpose: Autonomous throttle update
# THIS DOES NOT INCLUDE THE UNLINKING PORTION

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

def Takeoff(PWM_in, wanted_h, Start_alt):
	print 'Taking off'
	while cs.sonarrange - Start_alt < .25:
		Script.SendRC(3, PWM_in, True)
		if cs.verticalspeed < 0.2:
			Looping_Safety(100)
			PWM_in = PWM_in + 1
		Safety_Check()

	print 'Climb 2/3 of wanted height'
	while cs.sonarrange - Start_alt < wanted_h*2/3.0:
		cs.verticalspeed = 0.2
		Script.SendRC(3, PWM_in, True)
		if cs.verticalspeed > wanted_h*2/30.0 + 0.1:
			PWM_in = PWM_in - 1
			print 'decreasing PWM'
		Safety_Check()

	print 'Slowing down'
	check_slowdown = check_speedup = 0
	cs.verticalspeed = 0.15
	while cs.sonarrange - Start_alt < wanted_h:
		Script.SendRC(3, PWM_in, True)
		if cs.verticalspeed > 0.25:
			check_slowdown = check_slowdown + 1
			if check_slowdown == 10:
				PWM_in = PWM_in - 1
				check_slowdown = 0
			print check_slowdown
			print '2. Decreasing PWM'
		elif cs.verticalspeed < 0.1 and cs.sonarrange-Start_alt < wanted_h-0.5:		 
			check_speedup = check_speedup + 1
			if check_speedup == 150:					
				PWM_in = PWM_in + 10
				print '2. Inceasing PWM'
				check_speedup = 0
			print check_speedup
		Safety_Check()
	Safety_Check()

# --------------------------------- MAIN PROGRAM --------------------------------- #
print 'Starting Script'
# implement for all channels from 1-9
PWM_in = Start_alt = 0

Start_alt = cs.sonarrange
print Start_alt

for chan in range(1,5):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

print 'Initializing 6-14 to False'
for chan in range (6,14):
	Script.SendRC(chan,0,False)
	Script.SendRC(3,Script.GetParam('RC3_MIN'), True)

print 'Copter arming'
MAV.doARM(True)
Looping_Safety(2000)
PWM_in = 1500

# 3m = about 10ft
Takeoff(PWM_in, 2, Start_alt)

Script.SendRC(5,1400,True)
print 'PosHold copter'
print PWM_in
Looping_Safety(5000)

Script.ChangeParam("LAND_SPEED", 30)
Script.ChangeMode("Land")
print 'Landing'
while cs.alt > Start_alt:
	Safety_Check()

for chan in range(1,9):
	Script.SendRC(chan,0,True)

print 'Copter disarmed'
MAV.doARM(False)

print 'Script Over'
