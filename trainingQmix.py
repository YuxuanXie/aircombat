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

import logging
from sacred import Experiment
from os.path import dirname, abspath
from sacred.observers import FileStorageObserver
from sacred.utils import apply_backspaces_and_linefeeds

ex = Experiment()
ex.logger = logging.getLogger('my_custom_logger')
ex.captured_out_filter = apply_backspaces_and_linefeeds
results_path = os.path.join(dirname(abspath(__file__)), "results")
file_obs_path = os.path.join(results_path, "sacred")
ex.observers.append(FileStorageObserver.create(results_path))


logdir = './tblog/' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
infodir = logdir.replace("tblog", "log/info")
os.mkdir(infodir)
modeldir = logdir.replace("tblog", "log/model")
writer = SummaryWriter(log_dir=logdir)

@ex.config
def config():
    args = {
        "lr" : 5e-5,
        "batch_size" : 4096,
        "gamma" : 0.95,
        "kl_coef": 0.02,
        "memory_size" : 1000000,
        "epsilon_min" : 0.05,
        "num_mixers" : 2,
        "cuda" : False,
        "test_inertval" : 1000,
        "test_nepisode" : 32,
    }



@ex.main
def run(_run):
    # QMIX
    args = config()['args']
    alg = MCQMIX(32, 10, 4, args)

    total_steps = 0
    win_rate = []

    for i_episode in range(int(1e7)):

        steps, ep_r, title = run_one_episode(args, alg)
        total_steps += steps

        for _ in range(10):
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
            writer.add_scalar(f"Info/train_global_reward", reward, reward)
            writer.add_scalar(f"Info/train_win_rate", sum(win_rate)/len(win_rate), total_steps)
            _run.log_scalar(f"train_global_reward", reward, step=total_steps)

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

            _run.log_scalar(f"test_win_rate", sum(win_rate_test)/len(win_rate_test), step=total_steps)


if __name__ == "__main__":

    ex.run_commandline()