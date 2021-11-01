# 导入 socket、sys 模块
import os
os.environ["CUDA_DEVICE_ORDER"] = 'PCI_BUS_ID'
os.environ["CUDA_VISIBLE_DEVICES"]= "-1"
import socket
import sys
import numpy as np
import struct
from env import Env
import time
from menu import Menu, QApplication

app = QApplication(sys.argv)
menu = Menu()
menu.show()
app.exec_()

pos = menu.pos
target_pos = menu.target_pos
threaten = menu.threaten
move = menu.move
value = menu.value

send = []
for each in pos:
    send += each
for each in target_pos:
    send += each
send += threaten + value

print("length = ", len(send))
send = np.array(send, dtype=np.float32)

# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 8088

# 绑定端口号
serversocket.bind(("192.168.0.5", port))
# 设置最大连接数，超过后排队
serversocket.listen(5)
print(sys.byteorder)


# 建立客户端连接
clientsocket, addr = serversocket.accept()
print("连接地址: %s" % str(addr))

clientsocket.send(send)
print(send)


recvdata = clientsocket.recv(16)
recvdata = struct.unpack('4f', recvdata)
n_target = np.array(recvdata, dtype=np.int32).tolist()
print(n_target)


env = Env(4, 4, pos=pos, target_Pos=target_pos, target_for_agents=n_target, move=move)
r_position, b_position, r_position_2, b_position_2, r_position_3, b_position_3, r_position_4, b_position_4, situation_information, situation_information_2, situation_information_3, situation_information_4 = env.reset()
done_all = False
done_1 = 0
done_2 = 0
done_3 = 0
done_4 = 0

'''总奖励'''
ep_r = 0.0
ep_r_2 = 0.0
ep_r_3 = 0.0
ep_r_4 = 0.0
state = np.array(situation_information,dtype=np.float32)
state_2 = np.array(situation_information_2,dtype=np.float32)
state_3 = np.array(situation_information_3,dtype=np.float32)
state_4 = np.array(situation_information_4,dtype=np.float32)

send = situation_information + situation_information_2 + situation_information_3 + situation_information_4 + [done_1, done_2, done_3, done_4, done_all]
print("length = ", len(send))
send = np.array(send, dtype=np.float32)
clientsocket.send(send)
print(send)

steps = 0
title = ''
loss = 0
ignore = [0 for _ in range(4)]
previous_time = time.time()
time_used = []



while not done_all:

    recvdata = clientsocket.recv(16)
    recvdata = struct.unpack('4f', recvdata)
    data = np.array(recvdata, dtype=np.int32)
    # data = [0, 0, 1,1,1,1]

    print(data)
    print( '-' * 20 + f' step={steps}  time={time.time()-previous_time}' + '-'*20)
    time_used.append(time.time()-previous_time)
    previous_time = time.time()

    action   = data[0] if done_1 == 0 else 9
    action_2 = data[1] if done_2 == 0 else 9
    r_action_number_3 = data[2] if done_3 == 0 else 9
    r_action_number_4 = data[3] if done_4 == 0 else 9

    steps += 1
    # data = [0, 0, 1,1,1,1]
    state = np.array(situation_information, dtype=np.float32)
    state_2 = np.array(situation_information_2, dtype=np.float32)
    state_3 = np.array(situation_information_3)
    state_4 = np.array(situation_information_4)


    r_position_next, b_position_next, r_position_next_2, b_position_next_2, r_position_next_3, b_position_next_3, r_position_next_4, b_position_next_4, situation_information_next, situation_information_next_2, situation_information_next_3, situation_information_next_4, rewards, done_1, done_2, done_3, done_4, done_all, title = env.step(action, action_2, r_action_number_3, r_action_number_4)

    situation_information = situation_information_next
    situation_information_2 = situation_information_next_2
    situation_information_3 = situation_information_next_3
    situation_information_4 = situation_information_next_4

    ep_r += rewards[0]
    ep_r_2 += rewards[1]
    ep_r_3 += rewards[2]
    ep_r_4 += rewards[3]


    send = situation_information + situation_information_2 + situation_information_3 + situation_information_4 + [done_1, done_2, done_3, done_4, done_all]
    send = np.array(send, dtype=np.float32)
    print(send)
    clientsocket.send(send)

    if done_all:
        print(sum(time_used)/len(time_used))
        print(" previous episode steps = {}, reward = {}, title = {}".format( steps, (ep_r + ep_r_2 + ep_r_3 + ep_r_4)/4.0, title))

