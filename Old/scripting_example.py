print 'Start Script'

# implement for all channels from 1-9
for chan in range(1,9):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

#wait for 5 seconds
Script.Sleep(5000)

# while the current latitude is 0, we have not 
# yet acheived a GPS lock
# while cs.lat == 0:
#     print 'Waiting for GPS'
#     Script.Sleep(1000)

# 1 roll
# 2 pitch
# 3 throttle
# 4 yaw
# 5 flight mode
# 6 empty
# 7 autotune (?)
# 8 empty (?)
# 9 epm activation 

# Once GPS is received
print 'Got GPS'
Script.SendRC(3,1000,False)					# throttle
Script.SendRC(4,2000,True) 					# yawwwww
cs.messages.Clear()
Script.WaitFor('ARMING MOTORS',30000) 		# wait for 30 seconds for motors to arm
Script.SendRC(4,1500,True)
print 'Motors Armed!'
Script.SendRC(3,1700,True)

# while cs.alt < 50:
#    Script.Sleep(50)

Script.SendRC(5,2000,True) 					# acro
Script.SendRC(1,2000,False) 				# roll
Script.SendRC(3,1370,True) 					# throttle

# while cs.roll > -45: 						# top half 0 - 180
#    Script.Sleep(5)

# while cs.roll < -45: 						# -180 - -45
#    Script.Sleep(5)

Script.SendRC(5,1500,False) 				# stabilize
Script.SendRC(1,1500,True) 					# level roll
Script.Sleep(2000) 							# 2 sec to stabilize
Script.SendRC(3,1300,True) 					# throttle back to land
thro = 1350 								# will descend

# while cs.alt > 0.1:
#    Script.Sleep(300)

Script.SendRC(3,1000,False)
Script.SendRC(4,1000,True)
Script.WaitFor('DISARMING MOTORS',30000)
Script.SendRC(4,1500,True)

print 'Roll complete'