#JacobAlanGoldsberry
#Script for creating a rough tracker for vehicles without GPS
# import numpy as np
# import matplotlib as plt
# fun fact: mission planner does not like the numpy and matplotlib modules.
#Mission planner does not have any python in it.

#please figure out how to account for drifting...

import math
import time
from math import *
import clr
import MissionPlanner
clr.AddReference("MAVLink")
from System import Byte
import MAVLink
from MAVLink import mavlink_command_long_t

#Creating a boundary for the vehicles

X=0
Y=0
phi1 = 0
phi2 = 0

def phicalc(phi): #Finding phi from Omega and accounting for negative degrees

    if phi == Omega1:
        if phi < 0:
            print 'negative Omega1 = %f ' % phi
            phi1 = radians(90) + abs(radians(phi))
            return phi1

        else:
            print 'positive Omega1 = %f ' % phi
            phi1 = radians(90) - radians(phi)
            return phi1
    else:
        if phi < 0:
            print 'negative Omega2 = %f ' % phi
            phi2 = radians(90) - abs(radians(phi))
            return phi2

        else:
            print 'positive Omega2 = %f ' % phi
            phi2 = radians(90) + radians(phi)
            return phi2

def positiongeneralization(phi): #This function will guesstimate where the vehicle could be

#Note that currently time is set as 0.5s due to the speed at which each loop runs
#Future work includes changing this to be based on how long the vehicle is at a
# certain angle
    #simplealgorithim for max distance from zero
    x = 4.9*(cos(phi)/sin(phi))*(0.50)**2

    if phi == phi1: #Creating X
        print 'X distance = %f' % x
        global X
        X = x + oldvalx

    if phi == phi2: #Creating Y
        print 'Y distance = %f' % x
        global Y
        Y = x + oldvaly

# Opening the two files 'potato' and 'broccoli'
path = "C:/Users/jgoldsb1/Desktop/"
file_name = "potato"
file_name2 = "broccoli"
W = open(path+file_name+".txt", "w")
WW = open(path+file_name2+".txt", "w")
# R = open(path+file_name+'.txt', "r")
# RR = open(path+file_name2+'.txt', "r")

#While loop for getting position values and saving to files
count = 0
oldvalx = 0.0
oldvaly = 0.0
while cs.ch3in > Script.GetParam('RC3_MIN') or count < 50:
    Omega1 = cs.roll
    Omega2 = cs.pitch
    phi1 = phicalc(Omega1)
    print 'Finished phicalc1'
    print 'phi1 = %f ' % degrees(phi1)
    phi2 = phicalc(Omega2)
    print 'Finished phicalc2'
    print 'phi2 = %f ' % degrees(phi2)
    positiongeneralization(phi1)
    print 'Finished positiongeneralization1'
    positiongeneralization(phi2)
    print 'Finished positiongeneralization2'

    # Vec = sqrt(X**2 + Y**2)
    W.write("%f \n" % X) #Writing to the files
    WW.write("%f \n" % Y)
    # print 'The Vector is %f ' % Vec

    Script.Sleep(500)
    # Safety for Travelling too far
    if abs(X) > 5 or abs(Y) > 5:
        Script.ChangeMode('Land')
        print 'Safety Safety Safety'
        count = 50
    else:
        count = count + 1
        print "The count is: %f" % count
        print ''
        oldvalx = X
        oldvaly = Y

W.close()
WW.close()

# Create data
#this would work maybe if mission planner wasn't too dumb to
# work with the numpy and matplotlib modules.
#yay

# x = R.read()
# y = RR.read()
# colors = (0,0,0)
# area = np.pi*3
#
# # Plot
# plt.scatter(x, y, s=area, c=colors, alpha=0.5)
# plt.title('Scatter plot pythonspot.com')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()
