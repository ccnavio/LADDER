# Carie Navio
# Mission Planner Script
# Version 1
# Purpose: Waypoint script testing
# Master copter

print 'Start Script'

# implement for all channels from 1-9
for chan in range(1,9):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

#wait for 5 seconds
Script.Sleep(5000)

# 1 roll
# 2 pitch
# 3 throttle
# 4 yaw
# 5 flight modes
# 6 empty
# 7 autotune (?)
# 8 empty (?)
# 9 epm activation 

print 'Copter should start arming'
MAV.doARM(True) 							# Runs correctly in simulation
print 'Copter should be armed'

# Can have it wait for a signal to be sent from the RPI GS to the RPI on this 
# PIXHAWK and THEN it can start taking off
# Throttle PWM values will change for our specific copter

print 'Copter starting throttle'
Script.SendRC(3, 1700, True)				# Continue to throttle until alt is achieved
Script.SendRC(3, 1600, True)
while cs.alt < 5:
	print cs.alt							# while altitude is less than (m)?
	Script.Sleep(50)

print 'Copter slowing to 10 m'
Script.SendRC(3, 1550, True)
while cs.alt < 10:
	print cs.alt
	Script.Sleep(50)

print 'AltHold copter'
Script.SendRC(3, 1500, True)				# Slighly holds alt
Script.SendRC(5, 1400, True)				# This should be AltHold
Script.Sleep(5000)
print 'Finnished AltHold'

Script.SendRC(3, 1370, True)
while cs.alt > 0.5:
	print cs.alt
	Script.Sleep(50)

MAV.doARM(False)

print 'Copter Disarmed'