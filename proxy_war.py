
import sys, clr
clr.AddReference("MissionPlanner")
clr.AddReference("MAVLink")
import MAVLink, math, time, MissionPlanner

for chan in range(1,5):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

print 'Initializing 6-9 to False'
for chan in range (6,9):
	Script.SendRC(chan,0,False)
	Script.SendRC(3,Script.GetParam('RC3_MIN'), True)
	
if MAV.doARM(True):
	print 'Arming successful'
else:
	print 'Arming unsuccessful'
