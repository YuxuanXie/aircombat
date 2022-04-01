import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
import random
import copy
from torch.autograd import Variable

class Agent(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.embed_dim = 256
        self.agent_network = nn.Sequential(nn.Linear(self.input_dim, self.embed_dim),
                                nn.Tanh(),
                                nn.Linear(self.embed_dim, self.output_dim))
    def forward(self, state):
        state = Variable(torch.FloatTensor(state))
        qs = self.agent_network(state)
        return qs

class Mixer(nn.Module):
    def __init__(self, global_state_dim, agent_num):
        super().__init__()
        self.gs_dim = global_state_dim
        self.agent_num = agent_num
        self.embed_dim = 32

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
    def __init__(self, input_dim, output_dim, agent_num, epsilon_min=0.01):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.agent_num = agent_num
        
        self.epsilon = 1.0
        self.epsilon_decay = 5e-6
        self.epsilon_min = epsilon_min
        self.agent_networks = []

        # for i in range(self.agent_num): 
        for i in range(1):
            self.agent_networks.append(Agent(self.input_dim, self.output_dim))

    def act(self, obs, epsilon_greedy=True):
        self.epsilon = max(self.epsilon_min, self.epsilon-self.epsilon_decay)
        if epsilon_greedy and random.random() < self.epsilon:
            return [random.randrange(0, 9) for _ in range(self.agent_num)]
        actions = []
        for s in obs:
            qs = self.agent_networks[0](s)
            action = torch.argmax(qs, dim=-1).item()
            actions.append(action)
        
        return actions
    
    def forward(self, obs):

        qs = []
        for i in range(self.agent_num):
            qs.append(self.agent_networks[0](obs[:,i]))
        qs = torch.stack(qs, dim=1)

        return qs

    def load_state_dicts(self, states):
        for i in range(len(self.agent_networks)):
            self.agent_networks[i].load_state_dict(states[i])
    
    def state_dicts(self):
        return [each.state_dict() for each in self.agent_networks]


class Memory:
    def __init__(self, size):
        self.size = size
        self.memory = []
        self.index = 0
    
    def push(self, transition):
        if len(self.memory) < self.size:
            self.memory.append(transition)
        else:
            self.index = self.index % self.size
            self.memory[self.index] = transition
            self.index += 1

    def sample(self, bs):
        if len(self.memory) < bs:
            return None
        else:
            return random.sample(self.memory, bs)




class QMIX:
    def __init__(self, input_dim, output_dim, agent_num, args):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.agent_num = agent_num
        self.lr = args["lr"]
        self.batch_size = args["batch_size"]
        self.gamma = args["gamma"]

        self.memory = Memory(args["memory_size"])

        self.mac = MAController(self.input_dim, self.output_dim, self.agent_num, epsilon_min=args["epsilon_min"])
        self.mixer = Mixer(self.agent_num * self.input_dim, self.agent_num)

        self.target_mac = copy.deepcopy(self.mac)
        self.target_mixer = copy.deepcopy(self.mixer)

        self.params = list(self.mixer.parameters())
        for agent in self.mac.agent_networks:
            self.params += list(agent.parameters())

        self.optimiser = Adam(params=self.params, lr=self.lr)
        self.update_steps = 0
        self.grad_norm_clip = 20

        self.target_udate_frequency = 1000

    def learn(self):

        sampled_transitions = self.memory.sample(self.batch_size)
        if not sampled_transitions:
            return 0.0

        states = []
        actions = []
        rewards = []
        next_states = []
        dones = []
        next_available_action = []

        for each in sampled_transitions:
            states.append(each[0])
            actions.append(each[1])
            rewards.append(each[2])
            next_states.append(each[3])
            dones.append(each[4])
            next_available_action.append(each[5])

        states = Variable(torch.FloatTensor(torch.stack(states, dim=0)))
        actions = torch.stack(actions, dim=0)
        rewards = torch.FloatTensor(torch.stack(rewards, dim=0)).view(self.batch_size, 1)
        next_states = Variable(torch.FloatTensor(torch.stack(next_states, dim=0)))
        dones = torch.FloatTensor(torch.stack(dones, dim=0)).view(self.batch_size, 1)
        next_available_action = torch.stack(next_available_action, dim=0)

        mac_out = self.mac.forward(states)
        gs = states.reshape(self.batch_size, 1, self.agent_num*self.input_dim)
        chosen_q_value = torch.gather(mac_out, dim=2, index=torch.unsqueeze(actions, dim=-1))
        q_tot = self.mixer(chosen_q_value, gs)

        mac_out_next = self.mac.forward(next_states).detach()
        mac_out_next[next_available_action == 0] = -9e10

        max_action = torch.argmax(mac_out_next, dim=-1)
        mac_out_next_tatget = self.target_mac.forward(next_states)
        mac_out_next_max = torch.gather(mac_out_next_tatget, dim=2, index=torch.unsqueeze(max_action, dim=-1))


        gs_next = next_states.reshape(self.batch_size, 1, self.agent_num*self.input_dim)
        q_tot_next_target = self.target_mixer(mac_out_next_max, gs_next)
        target = rewards + self.gamma * (1-dones) * q_tot_next_target

        loss = (q_tot - target.detach())**2
        loss = loss.mean()

        self.optimiser.zero_grad()
        loss.backward()
        grad_norm = torch.nn.utils.clip_grad_norm_(self.params, self.grad_norm_clip)
        self.optimiser.step()

        self.update_steps += 1
        if self.update_steps % self.target_udate_frequency == 0:
            # TODO: Need to check if mac includes the list of agents
            print("Update target network!")
            self.target_mac.load_state_dicts(self.mac.state_dicts())
            self.target_mixer.load_state_dict(self.mixer.state_dict())
        
        return loss.item()


        

