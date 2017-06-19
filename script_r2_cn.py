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

print 'Copter starting throttle'
Script.SendRC(3, 1900, False)
Script.SendRC(3, 1300, True)				# Minimal throttle to enable takeoff
Script.SendRC(5, 1400, True)				# This should be Stabilize

while cs.alt < 10:							# while altitude is less than 3 (m)?
	Script.Sleep(50)

print 'Stabilizing copter'
Script.SendRC(3, 1370, True)