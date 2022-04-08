from env import Env
from util import generate_pos
import numpy as np
import torch


def run_one_episode(args, alg, epsilon_greedy=True):
    pos, target_pos = generate_pos(4)
    env = Env(4, 4, pos=pos, target_Pos=target_pos)
    _, _, _, _, _, _, _, _, situation_information, situation_information_2, situation_information_3, situation_information_4 = env.reset()
    done_all = False
    done_1 = 0
    done_2 = 0
    done_3 = 0
    done_4 = 0
    steps = 0

    '''总奖励'''
    ep_r = [0]*4

    while not done_all:
        steps += 1
        # data = [0, 0, 1,1,1,1]
        state = np.array(situation_information, dtype=np.float32)
        state_2 = np.array(situation_information_2, dtype=np.float32)
        state_3 = np.array(situation_information_3)
        state_4 = np.array(situation_information_4)

        if args["cuda"]:
            state = torch.FloatTensor(state).cuda()
            state_2 = torch.FloatTensor(state_2).cuda()
            state_3 = torch.FloatTensor(state_3).cuda()
            state_4 = torch.FloatTensor(state_4).cuda()
        else:
            state = torch.FloatTensor(state)
            state_2 = torch.FloatTensor(state_2)
            state_3 = torch.FloatTensor(state_3)
            state_4 = torch.FloatTensor(state_4)

        actions = alg.mac.act([state, state_2, state_3, state_4], epsilon_greedy=epsilon_greedy)
        dones = [done_1, done_2, done_3, done_4]

        for i in range(4):
            if dones[i] == 1:
                actions[i] = 9

        _, _, _, _, _, _, _, _, situation_information_next, situation_information_next_2, situation_information_next_3, situation_information_next_4, rewards, done_1, done_2, done_3, done_4, done_all, title = env.step(actions[0], actions[1], actions[2], actions[3])


        reward = sum(rewards) / len(rewards)
        available_action = []
        for each in dones:
            if each:
                available_action.append([0]*9+[1])
            else:
                available_action.append([1]*10)

        if epsilon_greedy:
            alg.memory.push([
                torch.from_numpy(np.array([situation_information, situation_information_2, situation_information_3, situation_information_4], dtype=np.single)), 
                torch.from_numpy(np.array(actions, dtype=np.int64)),
                torch.from_numpy(np.array(reward, dtype=np.single)),
                torch.from_numpy(np.array([situation_information_next, situation_information_next_2, situation_information_next_3, situation_information_next_4], dtype=np.single)),
                torch.from_numpy(np.array(done_all, dtype=np.single)),
                torch.from_numpy(np.array(available_action, dtype=np.single)),
            ])

        situation_information = situation_information_next
        situation_information_2 = situation_information_next_2
        situation_information_3 = situation_information_next_3
        situation_information_4 = situation_information_next_4

        ep_r = [ ep_r[i] + rewards[i] for i in range(4)]

    return steps, ep_r, title

