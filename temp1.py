from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
r = 10

ax = plt.axes(projection='3d')


q = 0.5  # defines upper starting point of the spherical segment
p = 0.8  # defines ending point of the spherical segment as ratio
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(q, p * np.pi, p * 100)
x = r * np.outer(np.cos(u), np.sin(v))
y = r * np.outer(np.sin(u), np.sin(v))
z = r * np.outer(np.ones(np.size(u)), np.cos(v))
if z>0:

ax.plot_surface(x, y, z, color='b')





