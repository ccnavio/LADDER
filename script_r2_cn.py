# Carie Navio
# Mission Planner Script
# Version 2
# Purpose: Waypoint script testing
# Slave copter

print 'Start Script'

# Implement for all channels from 1-9
for chan in range(1,9):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

# Wait for 5 seconds
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
Script.SendRC(3, 1500, True)				# Continue to throttle until alt is achieved
Script.SendRC(3, 1550, True)
while cs.alt < 2:
	print cs.alt
	cs.verticalspeed = 0.5							# while altitude is less than (m)?
	Script.Sleep(50)

print 'Copter slowing to 4 m'
Script.SendRC(3, 1550, True)
while cs.alt < 4:
	print cs.alt
	cs.verticalspeed = 0.25
	Script.Sleep(50)

print 'Copter slowing to 5 m'
while cs.alt < 5:
	print cs.alt
	cs.verticalspeed = 0.1

cs.mode = 'AUTO'
print cs.wp_dist 
Script.Sleep(2000)

# it will maintain jsut under 6 m / 19 ft 

print 'AltHold copter'
Script.SendRC(3, 1500, True)				# Slighly holds alt
Script.SendRC(5, 1400, True)				# This should be AltHold
Script.Sleep(5000)
print 'Finnished AltHold'

print MAV.getWPCount()

Script.SendRC(3, 1370, True)
while cs.alt > 0.2:
	print cs.alt
	Script.Sleep(50)

MAV.doARM(False)

print 'Copter Disarmed'