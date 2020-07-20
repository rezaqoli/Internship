#My 3d graph

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import cv2

'''


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Grab some test data.
X, Y, Z = axes3d.get_test_data(0.05)
X=X[0]
Y=Y[0]

# Plot a basic wireframe.
ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

plt.show()
print(X,"\n")
print(Y,"\n")
print(Z,"\n")
print (type(X),type(Y),type(Z))
print(X.shape,Y.shape,Z.shape)
input()
figure = plt.figure()
axis = figure.add_subplot(111, projection = '3d')
'''

fig = plt.figure()
axis = fig.add_subplot(111, projection='3d')


img = np.zeros((100,100))
for i in range(100):
    for j in range(100):
        if i==j:
            img[i,j]=1



#cv2.imshow("A",img)
#cv2.waitKey(0)
points = np.argwhere(img)
y = points[:,0]
x = points[:,1]

#print(type(x),x.shape)
#x = [0,0,0,0,0,0,0,0,0,0]
#y = [5,6,7,8,2,5,6,3,7,2]
#z = np.array([[1,2,6,3,2,7,3,3,7,2],[1,2,6,3,2,7,3,3,7,2]])
X=np.zeros(100,100)
Y=np.zeros(100,100)
for i in range(100):
        X[i]=x
        Y[i]=x

z= [0]
z=np.array([z,z])


axis.plot_wireframe(x, y, z)

axis.set_xlabel('x-axis')
axis.set_ylabel('y-axis')
axis.set_zlabel('z-axis')

plt.show()