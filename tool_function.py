from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


ax1 = plt.axes(projection='3d')
b_position = [10,10,0]
u =np.linspace(0,np.pi,1000)
v =np.linspace(0,2*np.pi,1000)
x = b_position[0] + 20*np.outer(np.cos(u),np.sin(v))
y = b_position[1] +20*np.outer(np.sin(u),np.sin(v))
z = b_position[2] +20*np.outer(np.ones(np.size(u)),np.cos(v))
ax1.plot_surface(x, y, z, cmap=plt.get_cmap('rainbow'),alpha = 0.2)
plt.show()