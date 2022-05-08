# 导入 socket、sys 模块
import os
import csv
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
from runner import run_one_episode
import torch
from qmix import QMIX
from mcqmix import MCQMIX
from torch.utils.tensorboard import SummaryWriter

logdir = './tblog/' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
infodir = logdir.replace("tblog", "log/info")
os.mkdir(infodir)
modeldir = logdir.replace("tblog", "log/model")

writer = SummaryWriter(log_dir=logdir)

args = {
    "lr" : 5e-5,
    "batch_size" : 4096*8,
    "gamma" : 0.95,
    "kl_coef": 0.02,
    "memory_size" : 2000000,
    "epsilon_min" : 0.05,
    "num_mixers" : 2,
    "cuda" : True,
    "test_inertval" : 1000,
    "test_nepisode" : 32,
}


# QMIX
alg = MCQMIX(32, 10, 4, args)

total_steps = 0
win_rate = []

for i_episode in range(int(1e7)):

    steps, ep_r, title = run_one_episode(args, alg)
    total_steps += steps

    for _ in range(2):
        # Learn
        loss = alg.learn()

    if "winner" in title:
        win_rate.append(1.0)
    else:
        win_rate.append(0.0)

    if i_episode % 50 == 0 and i_episode != 0:
        reward = sum(ep_r)/len(ep_r)
        print("episode = {}, total steps = {}, episilin = {}, previous episode steps = {}, reward = {}, title = {}".format(i_episode, total_steps, alg.mac.epsilon, steps, reward, title))
        # # writer.add_scalar(f"Info/{tag}", value, step)
        writer.add_scalar(f"Info/train_episode", i_episode, total_steps)
        writer.add_scalar(f"Info/train_reward_1", ep_r[0], total_steps)
        writer.add_scalar(f"Info/train_reward_2", ep_r[1], total_steps)
        writer.add_scalar(f"Info/train_reward_3", ep_r[2], total_steps)
        writer.add_scalar(f"Info/train_reward_4", ep_r[3], total_steps)
        writer.add_scalar(f"Info/train_loss", loss, total_steps)
        writer.add_scalar(f"Info/train_epsilon", alg.mac.epsilon, total_steps)
        writer.add_scalar(f"Info/train_global_reward", reward, total_steps)
        writer.add_scalar(f"Info/train_win_rate", sum(win_rate)/len(win_rate), total_steps)

        win_rate = []

    if i_episode % args["test_inertval"] == 0:
        win_rate_test = []
        for test_episode in range(args["test_nepisode"]):
            _, ep_r, title = run_one_episode(args, alg, epsilon_greedy=False)
            reward = sum(ep_r)/len(ep_r)
            if "winner" in title:
                win_rate_test.append(1.0)
            else:
                win_rate_test.append(0.0)
            writer.add_scalar(f"Info/test_reward_1", ep_r[0], total_steps)
            writer.add_scalar(f"Info/test_reward_2", ep_r[1], total_steps)
            writer.add_scalar(f"Info/test_reward_3", ep_r[2], total_steps)
            writer.add_scalar(f"Info/test_reward_4", ep_r[3], total_steps)
            writer.add_scalar(f"Info/test_global_reward", reward, total_steps)
        print("test {} episode, win rate is  = {}".format(args["test_nepisode"],  sum(win_rate_test)/len(win_rate_test)))
        writer.add_scalar(f"Info/test_win_rate", sum(win_rate_test)/len(win_rate_test), total_steps)
