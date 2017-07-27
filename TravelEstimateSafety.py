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
file_name3 = "asparagus"
W = open(path+file_name+".txt", "w")
WW = open(path+file_name2+".txt", "w")
Z = open(path+file_name3+'.txt', "w")
# R = open(path+file_name+'.txt', "r")
# RR = open(path+file_name2+'.txt', "r")

#While loop for getting position values and saving to files
count = 0
oldvalx = 0.0
oldvaly = 0.0
z0 = cs.alt
if z0 < 0:
    z0 = 0

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

    z = cs.alt
    if z < 0:
        z = 0
        print 'The new value of z is %f ' % z
        Z.write("%f \n" % z)
    else:
        z = z - z0
        print 'The value of z is %f ' % z
        Z.write("%f \n" % z)

    # Vec = sqrt(X**2 + Y**2)
    W.write("%f \n" % X) #Writing to the files
    WW.write("%f \n" % Y)
    # print 'The Vector is %f ' % Vec

    Script.Sleep(500)
    # Safety for Travelling too far
    if abs(X) > 10 or abs(Y) > 10:
        Script.ChangeMode('Land')
        print 'Safety Safety Safety'
        count = 50
    else:
        count = count + 1
        print "\nThe count is: %f" % count
        print ''
        oldvalx = X
        oldvaly = Y

W.close()
WW.close()
Z.close()

# # Create and plot data in three dimensions
# #This would work if mission planner was using native python but nope
# #JacobAlanGoldsberry
# #Work with matplotlib
# #Plotting X,Y, and Z coordinates in 3 dimensions
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
#
# #Create Data
#
# print x
# print len(w)
# print y
# print len(y)
# print z
# print len(z)
#
# #3D plot
# 
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
#
# for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
#
#     ax.plot(x, y, z, c=c, marker=m)
#
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')
#
# plt.show()
