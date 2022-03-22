import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
import random
import copy

class Agent(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.embed_dim = 128
        self.agent_network = nn.Sequential(nn.Linear(self.input_dim, self.embed_dim),
                                nn.ReLU(),
                                nn.Linear(self.embed_dim, self.output_dim))
    def forward(self, state):
        qs = self.agent_network(state)
        return qs

class Mixer(nn.Module):
    def __init__(self, global_state_dim, agent_num):
        super().__init__()
        self.gs_dim = global_state_dim
        self.agent_num = agent_num
        self.embed_dim = 128

        self.hyper_w1 = nn.Sequential(
                                    nn.Linear(self.gs_dim, self.embed_dim),
                                    nn.ReLU(),
                                    nn.Linear(self.embed_dim, self.embed_dim*self.agent_num))

        self.hyper_b1 = nn.Linear(self.gs_dim, self.embed_dim)

        self.hyper_w2 = nn.Sequential(
                                    nn.Linear(self.gs_dim, self.embed_dim),
                                    nn.ReLU(),
                                    nn.Linear(self.embed_dim, self.embed_dim))
        
        self.hyper_b2 = nn.Sequential(
                                    nn.Linear(self.gs_dim, self.embed_dim),
                                    nn.ReLU(),
                                    nn.Linear(self.embed_dim, 1))  

    def forward(self, qs, gs):
        qs = qs.reshape(-1, 1, self.agent_num)
        
        w1 = torch.abs(self.hyper_w1(gs))
        b1 = self.hyper_b1(gs)
        w1 = w1.view(-1, self.agent_num, self.embed_dim)
        b1 = b1.view(-1, 1, self.embed_dim)

        hidden = F.elu(torch.bmm(qs, w1) + b1)

        w2 = torch.abs(self.hyper_w2(gs))
        b2 = self.hyper_b2(gs)

        w2 = w2.view(-1, self.embed_dim, 1)
        b2 = b2.view(-1, 1, 1)

        tot_q = torch.bmm(hidden, w2) + b2

        return tot_q.reshape(-1, 1)


class MAController:
    def __init__(self, input_dim, output_dim, agent_num):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.agent_num = agent_num
        
        self.epsilon = 1.0
        self.epsilon_decay = 1e-4
        self.epsilon_min = 0.05
        self.agent_networks = []

        for i in range(self.agent_num):
            self.agent_networks.append(Agent(self.input_dim, self.output_dim))

    def act(self, obs):
        self.epsilon = max(self.epsilon_min, self.epsilon-self.epsilon_decay)
        if random.random() < self.epsilon:
            return [random.randrange(0, 9) for _ in range(self.agent_num)]
        actions = []
        for s, net in zip(obs, self.agent_networks):
            qs = net(s)
            action = torch.argmax(qs, dim=-1).item()
            actions.append(action)
        
        return actions
    
    def forward(self, obs):
        qs = []
        for i in range(self.agent_num):
            qs.append(self.agent_networks[i](obs[:,i]))
        qs = torch.stack(qs, dim=1)

        return qs


class Memory:
    def __init__(self, size):
        self.size = size
        self.memory = [None for _ in range(self.size)]
        self.index = 0
    
    def push(self, transition):
        self.index = self.index % self.size
        self.memory[self.index] = transition
        self.index += 1



class QMIX:
    def __init__(self, input_dim, output_dim, agent_num):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.agent_num = agent_num
        self.lr = 1e-3
        self.batch_size = 256
        self.gamma = 0.99

        self.memory = Memory(50000)
        self.mac = MAController(self.input_dim, self.output_dim, self.agent_num)
        self.mixer = Mixer(self.agent_num * self.input_dim, self.agent_num)

        self.target_mac = copy.deepcopy(self.mac)
        self.target_mixer = copy.deepcopy(self.mixer)

        self.params = self.mixer.parameters()
        for agent in self.mac.agent_networks:
            self.params += agent.params()

        self.optimiser = Adam(params=self.params, lr=self.lr)
        self.update_steps = 0

        self.target_udate_frequency = 200

    def learn(self):
        if self.memory[-1] == None:
            return None
        
        sampled_transitions = random.sample(self.memory, self.batch_size)

        states = sampled_transitions[:, 0]
        actions = sampled_transitions[:, 1]
        reward = sampled_transitions[:, 2]
        next_states = sampled_transitions[:, 3]
        done = sampled_transitions[:, 4]

        mac_out = self.mac.forward(states)
        gs = sampled_transitions[:,0]
        q_tot = self.mixer(mac_out, gs)

        mac_out_next = self.mac.forward(next_states)
        max_action = torch.argmax(mac_out_next, dim=-1)
        mac_out_next_tatget = self.target_mac(next_states)
        mac_out_next_max = torch.gather(mac_out_next_tatget, -1, max_action)

        gs_next = next_states
        q_tot_next_target = self.target_mixer(mac_out_next_max, gs_next)
        target = reward + self.gamma * (1-done) * q_tot_next_target

        loss = (q_tot - target.detach())**2
        loss = loss.mean()

        self.optimiser.zero_grad()
        loss.backward()
        self.optimiser.step()

        self.update_steps += 1
        if self.update_steps % self.target_udate_frequency == 0:
            # TODO: Need to check if mac includes the list of agents
            self.target_mac.load_state_dict(self.mac.state_dict())
            self.target_mixer.load_state_dict(self.mixer.state_dict())


        

