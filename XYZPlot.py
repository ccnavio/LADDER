#Work with matplotlib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Create Data
path = "C:/Users/jgoldsb1/Desktop/"
file_name = "potato"
file_name2 = "broccoli"
R = open(path+file_name+'.txt', "r")
RR = open(path+file_name2+'.txt', "r")
z = R.readlines()
z = [x.strip() for x in z]
y = RR.readlines()
y = [x.strip() for x in y]

print z
print y

# colors = (1,0,0)
# area = np.pi*3

# Plot
# plt.scatter(z, y, s=area, c=colors, alpha=0.5)
# plt.axis([-10, 10, -10, 10])
# plt.grid(True)
# plt.title('Estimated travel from zero')
# plt.xlabel('x (meters)')
# plt.ylabel('y (meters)')
# plt.show()

#Scatterplot code from matplotlib
def randrange(n, vmin, vmax):
    '''
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    '''
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = 100

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    xs = randrange(n, 23, 32)
    ys = randrange(n, 0, 100)
    zs = randrange(n, zlow, zhigh)
    ax.scatter(xs, ys, zs, c=c, marker=m)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
