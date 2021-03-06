

from enviroment import distance
import math
import numpy as np 

"""
To assign each agent a target based on the threaten value and attack value of the target

pos : num_agents x 3
target : num_targets x 3
threaten : num_targets x 1
value : num_target x 1
"""
def assign_target(pos, target_pos, threaten, value):
    assert(len(pos) == len(target_pos), "Num_agents should be equal to num_targets")
    num_agents = len(pos)
    weights = np.argsort([t + v for t,v in zip(threaten, value)]) 
    target_for_agents = [-1]*num_agents

    for target in reversed(weights):
        min_dis = 1e7
        best_agent = -1
        for agent in range(num_agents):
            if target_for_agents[agent] != -1:
                continue
            else:
                dis = math.sqrt(sum([(n-m)**2 for n,m in zip(pos[agent], target_pos[target])]))
                if  dis < min_dis:
                    min_dis = dis
                    best_agent = agent
        target_for_agents[best_agent] = target
        
    return target_for_agents




    