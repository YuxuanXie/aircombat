'''input_8 ->output_9'''
#import os
#os.environ["CUDA_DEVICE_ORDER"] = 'PCI_BUS_ID'
#os.environ["CUDA_VISIBLE_DEVICES"]= "-1"
from brain import DeepQNetwork
from  painter0 import Painter
import tensorflow as tf
from enviroment2 import Env
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from savetrajectory import  trajectorysave
RL = DeepQNetwork(n_actions=9,
                  n_features=8,
                  learning_rate=0.01, e_greedy=0.95,
                  replace_target_iter=100, memory_size=2000,
                  e_greedy_increment=0.0001,)
RL.addw_b_test_2()
total_steps = 0
ax1 = plt.axes(projection='3d')
for i_episode in range(10000000):

    '''初始化位置'''
    env =Env(4,4)
    r_position, b_position, r_position_2, b_position_2,r_position_3, b_position_3, r_position_4, b_position_4,situation_information, situation_information_2,situation_information_3,situation_information_4 = env.reset()
    done_all = False
    done_1 = 0
    done_2 = 0
    done_3 = 0
    done_4 = 0
    '''保存状态信息进行绘图 r,b,'''
    X = []
    Y = []
    Z = []
    X_B = []
    Y_B = []
    Z_B = []
    x_r = r_position[0]
    y_r = r_position[1]
    z_r = r_position[2]
    X.append(x_r)
    Y.append(y_r)
    Z.append(z_r)
    x_b = b_position[0]
    y_b = b_position[1]
    z_b = b_position[2]
    X_B.append(x_b)
    Y_B.append(y_b)
    Z_B.append(z_b)

    X_2 = []
    Y_2 = []
    Z_2 = []
    X_B_2 = []
    Y_B_2 = []
    Z_B_2 = []
    x_r_2 = r_position_2[0]
    y_r_2 = r_position_2[1]
    z_r_2 = r_position_2[2]
    X_2.append(x_r_2)
    Y_2.append(y_r_2)
    Z_2.append(z_r_2)
    x_b_2 = b_position_2[0]
    y_b_2 = b_position_2[1]
    z_b_2 = b_position_2[2]
    X_B_2.append(x_b_2)
    Y_B_2.append(y_b_2)
    Z_B_2.append(z_b_2)

    X_3 = []
    Y_3 = []
    Z_3 = []
    X_B_3 = []
    Y_B_3 = []
    Z_B_3 = []
    x_r_3 = r_position_3[0]
    y_r_3 = r_position_3[1]
    z_r_3 = r_position_3[2]
    X_3.append(x_r_3)
    Y_3.append(y_r_3)
    Z_3.append(z_r_3)
    x_b_3 = b_position_3[0]
    y_b_3 = b_position_3[1]
    z_b_3 = b_position_3[2]
    X_B_3.append(x_b_3)
    Y_B_3.append(y_b_3)
    Z_B_3.append(z_b_3)

    X_4 = []
    Y_4 = []
    Z_4 = []
    X_B_4 = []
    Y_B_4 = []
    Z_B_4 = []
    x_r_4 = r_position_4[0]
    y_r_4 = r_position_4[1]
    z_r_4 = r_position_4[2]
    X_4.append(x_r_4)
    Y_4.append(y_r_4)
    Z_4.append(z_r_4)
    x_b_4 = b_position_4[0]
    y_b_4 = b_position_4[1]
    z_b_4 = b_position_4[2]
    X_B_4.append(x_b_4)
    Y_B_4.append(y_b_4)
    Z_B_4.append(z_b_4)
    '''总奖励'''
    ep_r = 0.0
    ep_r_2 = 0.0
    ep_r_3 = 0.0
    ep_r_4 = 0.0
    while True:

        '''求解s,a,s_,reward,done_all,info'''
        #print ("s:",r_position,b_position)
        state = np.array(situation_information)
        state_2 = np.array(situation_information_2)
        state_3 = np.array(situation_information_3)
        state_4 = np.array(situation_information_4)
        #print(state)
        r_action_number = RL.choose_action(state)
        r_action_number_2 = RL.choose_action(state_2)
        r_action_number_3 = RL.choose_action(state_3)
        r_action_number_4 = RL.choose_action(state_4)
        #print (r_action_number)
        '''绘图：r_,b_ ********** state_,reward,done_all,title '''
        r_position_next,b_position_next, r_position_next_2, b_position_next_2,r_position_next_3, b_position_next_3, r_position_next_4, b_position_next_4,situation_information_next, situation_information_next_2, situation_information_next_3,situation_information_next_4,reward,reward_2,reward_3,reward_4,flag_1,flag_2,flag_3,flag_4, done_all,title = env.step(r_action_number,r_action_number_2,r_action_number_3,r_action_number_4)
        done_1 += flag_1
        done_2 += flag_2
        done_3 += flag_3
        done_4 += flag_4
        #print ("s+:",r_position_next,b_position_next)
        '''绘图'''
        X.append(r_position_next[0])
        Y.append(r_position_next[1])
        Z.append(r_position_next[2])
        X_B.append((b_position_next[0]))
        Y_B.append((b_position_next[1]))
        Z_B.append(b_position_next[2])
        X_2.append(r_position_next_2[0])
        Y_2.append(r_position_next_2[1])
        Z_2.append(r_position_next_2[2])
        X_B_2.append((b_position_next_2[0]))
        Y_B_2.append((b_position_next_2[1]))
        Z_B_2.append(b_position_next_2[2])
        X_3.append(r_position_next_3[0])
        Y_3.append(r_position_next_3[1])
        Z_3.append(r_position_next_3[2])
        X_B_3.append((b_position_next_3[0]))
        Y_B_3.append((b_position_next_3[1]))
        Z_B_3.append(b_position_next_3[2])
        X_4.append(r_position_next_4[0])
        Y_4.append(r_position_next_4[1])
        Z_4.append(r_position_next_4[2])
        X_B_4.append((b_position_next_4[0]))
        Y_B_4.append((b_position_next_4[1]))
        Z_B_4.append(b_position_next_4[2])


        if done_1 < 2:
            RL.store_transition(situation_information,r_action_number,reward,situation_information_next)
        if done_2 < 2:
            RL.store_transition(situation_information_2, r_action_number_2, reward_2, situation_information_next_2)
        if done_3 < 2:
            RL.store_transition(situation_information_3, r_action_number_3, reward_3, situation_information_next_3)
        if done_2 < 2:
            RL.store_transition(situation_information_4, r_action_number_4, reward_4, situation_information_next_4)

        situation_information = situation_information_next
        situation_information_2 = situation_information_next_2
        situation_information_3 = situation_information_next_3
        situation_information_4 = situation_information_next_4
        if done_1 < 2:
            ep_r += reward
        if done_2<2:
            ep_r_2 += reward_2
        if done_3<2:
            ep_r_3 += reward_3
        if done_4 < 2:
            ep_r_4 += reward_4

        if total_steps > 1000:
            RL.learn()

        if done_all:
            if i_episode %1000 ==0 and i_episode!=0:
                #with g1.as_default():
                #    RL.storew_b_test(i_episode)
                print ("model saved")
                RL.storevariable_2()

                print("******")
                print(X)
                print(Y)
                print(Z)
                print("******")
                print(X_B)
                print(Y_B)
                print(Z_B)
                #trajectorysave(X,Y,Z,i_episode,title)
                #trajectorysave(X_B, Y_B, Z_B, i_episode, "bluetra")
                #painter = Painter(X, Y, Z, X_B, Y_B, Z_B)
                #painter.plotfigure(i_episode)
                #painter.plotfigure(i_episode,title,ep_r)
                print ("over")
                print(title)
                ax1.set_xlim(-30, 50)
                ax1.set_ylim(-30, 50)
                ax1.set_zlim(0, 50)
                #x0 = np.arange(9, 11, 0.1)
                #y0= np.arange(9,11,0.1)
                # ??????
                #x1 , y1 = np.meshgrid(x0, y0)
                # ??Z????
                #z1 = x1*y1*0+20
                #ax1.plot_surface(x1, y1, z1, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))
                #ax1.scatter3D(X, Y, Z, c='r')
                #u =np.linspace(0,2*np.pi,1000)
                #v =np.linspace(0,2*np.pi,1000)
                #x = b_position_next[0] + 20 * np.outer(np.cos(u), np.sin(v))
                #y = b_position_next[1] + 20 * np.outer(np.sin(u), np.sin(v))
                #z = b_position_next[2] + 20 * np.outer(np.ones(np.size(u)), np.cos(v))
                #ax1.plot_surface(x, y, z, cmap=plt.get_cmap('rainbow'))
                ax1.plot3D(X, Y, Z, 'red')
                ax1.plot3D(X_2, Y_2, Z_2, 'red')
                ax1.plot3D(X_3, Y_3, Z_3, 'red')
                ax1.plot3D(X_4, Y_4, Z_4, 'red')
                ax1.plot3D(X_B, Y_B, Z_B,'blue')
                ax1.plot3D(X_B_2, Y_B_2, Z_B_2,'blue')
                ax1.plot3D(X_B_3, Y_B_3, Z_B_3, 'blue')
                ax1.plot3D(X_B_4, Y_B_4, Z_B_4, 'blue')
                ax1.scatter3D(X_B, Y_B, Z_B, c='b')
                ax1.scatter3D(X_B_2, Y_B_2, Z_B_2, c='b')
                ax1.scatter3D(X_B_3, Y_B_3, Z_B_3, c='b')
                ax1.scatter3D(X_B_4, Y_B_4, Z_B_4, c='b')
                plt.savefig("{}{}.png".format(i_episode,title), dpi=300)
                #plt.savefig("{}{}{:.2f}{:.2f}{}{}{}{}{}{}.png".format(i_episode, title, ep_r,ep_r_2, '**', X_B[0], '_', Y_B[0], '_', Z_B[0]), dpi=300)
                plt.cla()
            break
        total_steps += 1
