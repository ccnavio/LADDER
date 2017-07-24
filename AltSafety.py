#Altitude Safety Function for LADDER
import time
import math
import clr
import MissionPlanner
clr.AddReference("MAVLink")
from System import Byte
import MAVLink
from MAVLink import mavlink_command_long_t

#Functions
#These two functions are the only things required for the safety check. Everything after the functions is superfluous. 
def AltitudeCheck(Altin):
    Alt1 = abs(Altin)
    print Alt1
    print Alt0
    DAlta = Alt1 - abs(Alt0)
    AltActual = 0.0 + DAlta
    print AltActual
    return AltActual

def SafeCheck(Altitude):
    count = 0
    CountTime = 9 #Number of times before getting into the safety loop
    # print 'Throttle min: %d ' % Script.GetParam('RC3_MIN')
    # print 'Current Throttle: %d ' % cs.ch3in
    # print 'While loop comparison is %d ' % cs.ch3in > Script.GetParam('RC3_MIN')
    while AltActual < 0.40 and cs.ch3in > Script.GetParam('RC3_MIN'):
        print 'In while loop'
        if count > CountTime and AltActual < 0.25:
            Script.SendRC(3,Script.GetParam('RC3_MIN'),True)
            print ' '
            print 'Safety Safety Safety'
            print ' '

            Script.Sleep(1000)
            Script.SendRC(4,Script.GetParam('RC4_MIN'),True)
            Script.Sleep(2000)
            Script.SendRC(4,YawCenter,True)
            if cs.ch4in == Script.GetParam('RC4_MIN') and cs.ch3in == Script.GetParam('RC3_MIN'):
                print '         Motors OFF'
                Script.Sleep(1000)
                print '         Disarmed'

        else:
            Script.Sleep(100)
            count = count + 1
            print count

    if AltActual > 0.25:
        print "Safe"

#Start of the script
#Everything past this point is just to prove that the code works
print 'Start Script'
Alt0 = cs.alt
AltActual = 0

for chan in range(1,9):
    Script.SendRC(chan,1500,False)
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

YawCenter = Script.GetParam('RC4') #Creating a center stick command for CH4
Script.Sleep(1000)

Script.ChangeMode("Stabilize") #Chaning to stabilize mode
print 'Stabilize'

Script.SendRC(4,Script.GetParam('RC4_MAX'),True) #Arm
Script.Sleep(2000)
print 'Motors Armed'

Script.SendRC(4,YawCenter,True)

Script.Sleep(2000)

Script.SendRC(3,1460,True)
Script.Sleep(4000)

print 'Starting Alt check'
Script.Sleep(2000)
AltActual = AltitudeCheck(cs.alt)

print 'Starting safety check'
Script.Sleep(2000)
SafeCheck(AltActual)

Script.Sleep(5000)

#Ending it
if cs.ch3in > Script.GetParam('RC3_MIN'):
    print 'Throttle down'
    Script.SendRC(3,Script.GetParam('RC3_MIN'),True)
    Script.Sleep(2000)
    print 'Disarm'
    Script.SendRC(4,Script.GetParam('RC4_MIN'),True)
    Script.Sleep(3000)
    Script.SendRC(4,YawCenter,True)
    print 'Finished!'
else:
    print ' '
    print 'Finished'
