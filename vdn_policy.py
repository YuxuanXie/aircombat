import numpy as np
import tensorflow as tf


class VDN:
    def __init__(
            self,
            n_actions,
            n_features,
            n_agents = 4,
            learning_rate=0.01,
            reward_decay=0.9,
            e_greedy=0.9,
            replace_target_iter = 300,
            memory_size = 500,
            batch_size = 32,
            e_greedy_increment = None,
            output_graph = False,
            ):
        self.n_actions = n_actions
        self.n_features = n_features
        self.n_agents = n_agents
        self.lr = learning_rate
        self.gamma = reward_decay



