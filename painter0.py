import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
class Painter():
    def __init__(self,X,Y,Z,X_B,Y_B,Z_B):
        self.x = np.array(X)
        self.y = np.array(Y)
        self.z = np.array(Z)
        self.x_b = np.array(X_B)
        self.y_b = np.array(Y_B)
        self.z_b = np.array(Z_B)
        self.redline = np.vstack((self.x,self.y,self.z))
        self.blueline = np.vstack((self.x_b, self.y_b, self.z_b))
        self.data = [self.redline,self.blueline]

    def plotfigure(self,title):
        #plt.ion()
        fig  = plt.figure()
        ax = p3.Axes3D(fig)
        lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in self.data]
        ax.set_xlim(-30, 50)
        ax.set_xlabel('X')
        ax.set_ylim(-30, 50)
        ax.set_ylabel('Y')
        ax.set_zlim(0, 50)
        ax.set_zlabel('Z')
        ax.legend(handles=[lines[0],lines[1]],labels=['uav','target'],loc = 'upper right')
        line_anti = animation.FuncAnimation(fig, self.update_lines, len(self.x), fargs=(self.data, lines), interval=50, blit=False)
        line_anti.save('{}.gif'.format(title), writer='imagemagick')

        #plt.pause(5)  # 显示秒数
        #plt.close()
        #plt.show()

    def update_lines(self,num, data, lines):
        for line, data in zip(lines, data):
            # NOTE: there is no .set_data() for 3 dim data...
            line.set_data(data[0:2, :num])
            # print(data[0:2, :num])
            line.set_3d_properties(data[2, :num])
        return lines
