import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
import random
import copy
from torch.autograd import Variable

from qmix import Mixer, MAController, Memory


class MultipleMixer(nn.Module):
    def __init__(self, global_state_dim, agent_num, num_mixers=2):
        super().__init__()
        self.gs_dim = global_state_dim
        self.agent_num = agent_num
        self.num_mixers = num_mixers
        self.embed_dim = 32

        self.mixers = [ Mixer(self.gs_dim, self.agent_num) for i in range(self.num_mixers)]

        self.choiceNet = nn.Sequential(nn.Linear(self.gs_dim, self.embed_dim),
                        nn.ReLU(),
                        nn.Linear(self.embed_dim, self.num_mixers))

    def forward(self, qs, gs):
        q_tots = []
        for mixer in self.mixers:
            q_tots.append(mixer.forward(qs, gs))
        q_tots_val = torch.cat(q_tots, dim=-1)

        q_tots_w = 1.0 / (torch.abs(q_tots_val) + 1e-9)
        # softmax
        weights = nn.functional.softmax(q_tots_w, dim=-1).detach()

        # choice network
        weights_cn = self.choiceNet(gs)
        weights_cn = nn.functional.softmax(weights_cn, dim=-1).squeeze()

        # gumbel softmax
        # weights = th.nn.functional.gumbel_softmax(q_tots_w, tau=1, hard=False, eps=1e-10, dim=-1)
        q_tot = torch.sum(weights_cn * q_tots_val, dim=-1, keepdim=True)

        return q_tot.reshape(-1, 1), weights_cn, weights
    
    def load_state_dicts(self, states):
        for i in range(self.num_mixers):
            self.mixers[i].load_state_dict(states[i])
    
    def state_dicts(self):
        return [each.state_dict() for each in self.mixers]
    
    def use_cuda(self):
        self.choiceNet.cuda()
        for mixer in self.mixers:
            mixer.cuda()


class MCQMIX:
    def __init__(self, input_dim, output_dim, agent_num, args):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.agent_num = agent_num
        self.lr = args["lr"]
        self.batch_size = args["batch_size"]
        self.gamma = args["gamma"]
        self.klcoef = args["kl_coef"]
        self.args = args

        self.memory = Memory(args["memory_size"])

        self.mac = MAController(self.input_dim, self.output_dim, self.agent_num, epsilon_min=args["epsilon_min"])
        self.mixer = MultipleMixer(self.agent_num * self.input_dim, self.agent_num, num_mixers=args["num_mixers"])

        self.target_mac = copy.deepcopy(self.mac)
        self.target_mixer = copy.deepcopy(self.mixer)

        self.params = []
        for each in self.mixer.mixers:
            self.params += list(each.parameters())
        for agent in self.mac.agent_networks:
            self.params += list(agent.parameters())

        self.optimiser = Adam(params=self.params, lr=self.lr)
        self.update_steps = 0
        self.grad_norm_clip = 20

        self.target_udate_frequency = 1000

        if args["cuda"]:
            self.mac.use_cuda()
            self.mixer.use_cuda()
            self.target_mac.use_cuda()
            self.target_mixer.use_cuda()
    
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

        if self.args["cuda"]:
            states = states.cuda()
            actions = actions.cuda()
            rewards = rewards.cuda()
            next_states = next_states.cuda()
            dones = dones.cuda()
            next_available_action = next_available_action.cuda()

        mac_out = self.mac.forward(states)
        gs = states.reshape(self.batch_size, 1, self.agent_num*self.input_dim)
        chosen_q_value = torch.gather(mac_out, dim=2, index=torch.unsqueeze(actions, dim=-1))
        q_tot, weights_cn, weights = self.mixer(chosen_q_value, gs)

        mac_out_next = self.mac.forward(next_states).detach()
        mac_out_next[next_available_action == 0] = -9e10

        max_action = torch.argmax(mac_out_next, dim=-1)
        mac_out_next_tatget= self.target_mac.forward(next_states)
        mac_out_next_max = torch.gather(mac_out_next_tatget, dim=2, index=torch.unsqueeze(max_action, dim=-1))


        gs_next = next_states.reshape(self.batch_size, 1, self.agent_num*self.input_dim)
        q_tot_next_target, _, _ = self.target_mixer(mac_out_next_max, gs_next)
        target = rewards + self.gamma * (1-dones) * q_tot_next_target

        # Soft plus to make it stabler
        kl_loss = F.kl_div(weights_cn, weights)
        kl_loss = torch.log(1 + torch.exp(kl_loss))

        

        loss = (q_tot - target.detach())**2
        loss = loss.mean() + self.klcoef * kl_loss

        self.optimiser.zero_grad()
        loss.backward()
        grad_norm = torch.nn.utils.clip_grad_norm_(self.params, self.grad_norm_clip)
        self.optimiser.step()

        self.update_steps += 1
        if self.update_steps % self.target_udate_frequency == 0:
            # TODO: Need to check if mac includes the list of agents
            print("Update target network!")
            self.target_mac.load_state_dicts(self.mac.state_dicts())
            self.target_mixer.load_state_dicts(self.mixer.state_dicts())
        
        return loss.item()