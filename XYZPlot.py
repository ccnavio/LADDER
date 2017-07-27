#JacobAlanGoldsberry
#Work with matplotlib
#Plotting X,Y, and Z coordinates in 3 dimensions
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# def strip(c):
#     c = [x.strip() for x in c]

#Create Data
path = "C:/Users/jgoldsb1/Desktop/"
file_name = "potato"
file_name2 = "broccoli"
file_name3 = "asparagus"
R = open(path+file_name+'.txt', "r")
RR = open(path+file_name2+'.txt', "r")
RRR = open(path+file_name3+'.txt', "r")
w = R.readlines()
w = [float(x.strip()) for x in w]
y = RR.readlines()
y = [float(x.strip()) for x in y]
z = RRR.readlines()
z = [float(x.strip()) for x in z]

print w
print len(w)
print y
print len(y)
print z
print len(z)

#3D plot

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:

    ax.plot(w, y, z, c=c, marker=m)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
