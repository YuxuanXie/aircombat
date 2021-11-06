# 导入 socket、sys 模块
import os
os.environ["CUDA_DEVICE_ORDER"] = 'PCI_BUS_ID'
os.environ["CUDA_VISIBLE_DEVICES"]= "-1"
import socket
import sys
import numpy as np
import struct
from brain import DeepQNetwork
import tensorflow as tf
from env import Env
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import random
from datetime import datetime
from util import generate_pos

logdir = './tblog/' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
infodir = logdir.replace("tblog", "log/info")
os.mkdir(infodir)
modeldir = logdir.replace("tblog", "log/model")
ax1 = plt.axes(projection='3d')

g = [tf.Graph() for _ in range(4)]
RL = [None]*4
for i in range(4):
    with g[i].as_default():
        RL[i] = DeepQNetwork(n_actions=10,
                      n_features=32,
                      learning_rate=1e-4, e_greedy=0.99,
                      replace_target_iter=600, memory_size=int(1e5),
                      e_greedy_decrement=1e-5,
                      batch_size=128)
        RL[i].load_model(f'./log/model/2021-11-04-19-01-00/480000_agent{i}.ckpt')
total_steps = 0
ax1 = plt.axes(projection='3d')


winner_count = 0

for i_episode in range(int(1e2)):
    pos, target_pos = generate_pos(4)

    # pos = [[-19, 20, 32], [-24, 19, 32], [-15, 15, 32], [-8, 20, 31]]
    # target_pos = [[8, 2, 4], [4, 6, 13], [3, 2, 20], [7, 2, 6]]
    # print(f"target_pos = {target_pos}")
    # print(f"pos = {pos}")
    
    # target_for_agents = [0,1,2,3]
    # random.shuffle(target_for_agents)
    # assigned_target_Pos = []
    # for each in target_for_agents:
    #     assigned_target_Pos.append(target_pos[each])

    env = Env(4, 4, pos=pos, target_Pos=target_pos, move=[False]*4 )
    # env = Env(4, 4, pos=pos, target_Pos=target_pos)
    r_position, b_position, r_position_2, b_position_2, r_position_3, b_position_3, r_position_4, b_position_4, situation_information, situation_information_2, situation_information_3, situation_information_4 = env.reset()
    done_all = False
    done_1 = 0
    done_2 = 0
    done_3 = 0
    done_4 = 0
    '''保存状态信息进行绘图 r,b,'''

    actionlist1 = []
    actionlist2 = []
    actionlist3 = []
    actionlist4 = []

    total_reward1 = []
    total_reward2 = []
    total_reward3 = []
    total_reward4 = []

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
    state = np.array(situation_information,dtype=np.float32)
    state_2 = np.array(situation_information_2,dtype=np.float32)
    send = np.concatenate((state, state_2), axis=0)
    # print(send)
    steps = 0
    title = ''
    loss = 0
    ignore = [0 for _ in range(4)]
    if_training = False

    while not done_all:
        steps += 1
        # data = [0, 0, 1,1,1,1]
        state = np.array(situation_information, dtype=np.float32)
        state_2 = np.array(situation_information_2, dtype=np.float32)
        state_3 = np.array(situation_information_3)
        state_4 = np.array(situation_information_4)

        # import pdb; pdb.set_trace()
        # print(state)

        with g[0].as_default():
            if done_1 == 0:
                action = RL[0].choose_action(state, training=if_training)
            else:
                action = 9
                ignore[0] = 1
        with g[1].as_default():
            if done_2 == 0:
                action_2 = RL[1].choose_action(state_2, training=if_training)
            else:
                action_2 = 9
                ignore[1] = 1
        with g[2].as_default():
            if done_3 == 0:
                r_action_number_3 = RL[2].choose_action(state_3, training=if_training)
            else:
                r_action_number_3 = 9
                ignore[2] = 1
        with g[3].as_default():
            if done_4 == 0:
                r_action_number_4 = RL[3].choose_action(state_4, training=if_training)
            else:
                r_action_number_4 = 9
                ignore[3] = 1

        r_position_next, b_position_next, r_position_next_2, b_position_next_2, r_position_next_3, b_position_next_3, r_position_next_4, b_position_next_4, situation_information_next, situation_information_next_2, situation_information_next_3, situation_information_next_4, rewards, done_1, done_2, done_3, done_4, done_all, title = env.step(action, action_2, r_action_number_3, r_action_number_4)

        actionlist1.append(action)
        actionlist2.append(action_2)
        actionlist3.append(r_action_number_3)
        actionlist4.append(r_action_number_4)
        total_reward1.append(rewards[0])
        total_reward2.append(rewards[1])
        total_reward3.append(rewards[2])
        total_reward4.append(rewards[3])

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

        situation_information = situation_information_next
        situation_information_2 = situation_information_next_2
        situation_information_3 = situation_information_next_3
        situation_information_4 = situation_information_next_4

        ep_r += rewards[0]
        ep_r_2 += rewards[1]
        ep_r_3 += rewards[2]
        ep_r_4 += rewards[3]

        if done_all:
            total_steps += steps
            print("episode = {}, total steps = {}, episilin = {}, previous episode steps = {}, reward = {}, title = {}".format(i_episode, total_steps, RL[0].epsilon, steps, (ep_r + ep_r_2 + ep_r_3 + ep_r_4)/4.0, title))
            winner_count += 1 if 'winner' in title else 0
            if i_episode % 100 ==0 and i_episode!=0:
                print('**************** check point *****************')
                print(b_position)
                print(b_position_2)
                print(b_position_3)
                print(b_position_4)
                print('******')
                print(i_episode)
                print(ep_r)
                print(X)
                print(Y)
                print(Z)
                print(actionlist1)
                print(total_reward1)
                print("******")
                print(ep_r_2)
                print(X_2)
                print(Y_2)
                print(Z_2)
                print(actionlist2)
                print(total_reward2)
                print("****")
                print(ep_r_3)
                print(X_3)
                print(Y_3)
                print(Z_3)
                print(actionlist3)
                print(total_reward3)
                print("****")
                print(ep_r_4)
                print(X_4)
                print(X_4)
                print(X_4)
                print(actionlist4)
                print(total_reward4)
                print("******")
                print(X_B)
                print(Y_B)
                print(Z_B)
                # trajectorysave(X,Y,Z,i_episode,title)
                # trajectorysave(X_B, Y_B, Z_B, i_episode, "bluetra")
                # painter = Painter(X, Y, Z, X_B, Y_B, Z_B)
                # painter.plotfigure(i_episode)
                # painter.plotfigure(i_episode,title,ep_r)
                print("over")
                print(title)
                ax1.set_xlim(-100, 100)
                ax1.set_ylim(-100, 100)
                ax1.set_zlim(0, 50)
                # x0 = np.arange(9, 11, 0.1)
                # y0= np.arange(9,11,0.1)
                # ??????
                # x1 , y1 = np.meshgrid(x0, y0)
                # ??Z????
                # z1 = x1*y1*0+20
                # ax1.plot_surface(x1, y1, z1, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))
                # ax1.scatter3D(X, Y, Z, c='r')
                # u =np.linspace(0,2*np.pi,1000)
                # v =np.linspace(0,2*np.pi,1000)
                # x = b_position_next[0] + 20 * np.outer(np.cos(u), np.sin(v))
                # y = b_position_next[1] + 20 * np.outer(np.sin(u), np.sin(v))
                # z = b_position_next[2] + 20 * np.outer(np.ones(np.size(u)), np.cos(v))
                # ax1.plot_surface(x, y, z, cmap=plt.get_cmap('rainbow'))
                ax1.plot3D(X, Y, Z, 'red')
                ax1.plot3D(X_2, Y_2, Z_2, 'red')
                ax1.plot3D(X_3, Y_3, Z_3, 'red')
                ax1.plot3D(X_4, Y_4, Z_4, 'red')
                ax1.plot3D(X_B, Y_B, Z_B, 'blue')
                ax1.plot3D(X_B_2, Y_B_2, Z_B_2, 'blue')
                ax1.plot3D(X_B_3, Y_B_3, Z_B_3, 'blue')
                ax1.plot3D(X_B_4, Y_B_4, Z_B_4, 'blue')
                ax1.scatter3D(X_B, Y_B, Z_B, c='b')
                ax1.scatter3D(X_B_2, Y_B_2, Z_B_2, c='b')
                ax1.scatter3D(X_B_3, Y_B_3, Z_B_3, c='b')
                ax1.scatter3D(X_B_4, Y_B_4, Z_B_4, c='b')
                plt.savefig( infodir + "/{}{}{}{}{}{}{}{}{}.png".format(i_episode, title, ep_r, '_', ep_r_2, '_', ep_r_3, '_', ep_r_4), dpi=300)
                # plt.savefig("{}{}{:.2f}{:.2f}{}{}{}{}{}{}.png".format(i_episode, title, ep_r,ep_r_2, '**', X_B[0], '_', Y_B[0], '_', Z_B[0]), dpi=300)
                plt.cla()

                f = open( infodir + '/{}.csv'.format(i_episode), 'w',encoding='utf-8',newline='' "")

                csv_writer = csv.writer(f)
                csv_writer.writerow(["time/s", "uavid", "x","y","z","target_id","x","y","z"])
                for i in range(len(X)):
                    csv_writer.writerow([i,"1",X[i]*100,Y[i]*100,Z[i]*100,"1",X_B[i]*100,Y_B[i]*100,Z_B[i]*100])
                for i in range(len(X_2)):
                    csv_writer.writerow([i,"2",X_2[i]*100,Y_2[i]*100,Z_2[i]*100,"2",X_B_2[i]*100,Y_B_2[i]*100,Z_B_2[i]*100])
                for i in range(len(X_3)):
                    csv_writer.writerow([i,"3",X_3[i]*100,Y_3[i]*100,Z_3[i]*100,"3",X_B_3[i]*100,Y_B_3[i]*100,Z_B_3[i]*100])
                for i in range(len(X_4)):
                    csv_writer.writerow([i, "4", X_4[i] * 100, Y_4[i] * 100, Z_4[i] * 100, "4", X_B_4[i] * 100, Y_B_4[i] * 100,Z_B_4[i] * 100])
                f.close()
                break

print(f"win rate = {winner_count / 100}")
