

import math
import numpy as np
import random



class CloudpickleWrapper():
    def __init__(self, x):
        self.x = x
    
    def __getstate__(self):
        import cloudpickle
        return cloudpickle.dumps(self.x)
    
    def __setstate__(self, ob):
        import pickle
        self.x = pickle.loads(ob)

def worker(conn, menu_creator):

    app = QApplication(sys.argv)
    menu = menu_creator.x(conn=conn)
    menu.show()
    app.exec_()




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

def generate_pos(num_agents):
    pos = []
    target_pos = []

    random_size = 3
    hight_random_size = 0

    pos.append([-20+random.randint(0,2), 15+random.randint(0,5), 30+random.randint(0,2)])
    pos.append([-25 + random.randint(0, 2), 15 + random.randint(0, 5), 30 + random.randint(0, 2)])
    pos.append([-15 + random.randint(0, 2), 15 + random.randint(0, 5), 30 + random.randint(0, 2)])
    pos.append([-10 + random.randint(0, 2), 15 + random.randint(0, 15), 30 + random.randint(0, 2)])

    for _ in range(num_agents):
        if random.random() < 1.0:
            b_position = [5 + random.randint(-random_size, random_size),5 + random.randint(-random_size, random_size), 0 + random.randint(-hight_random_size, hight_random_size)]
        else:
            b_position = [5 + random.randint(-random_size, random_size),5 + random.randint(-random_size, random_size),  30 + random.randint(0, 2)]

        target_pos.append(b_position)

    return pos, target_pos

def generate_pos_per_scene(num_agents, in_air, mix=False):
    pos = []
    target_pos = []

    random_size = 3
    hight_random_size = 0

    pos.append([-20+random.randint(0,2), 15+random.randint(0,5), 30+random.randint(0,2)])
    pos.append([-25 + random.randint(0, 2), 15 + random.randint(0, 5), 30 + random.randint(0, 2)])
    pos.append([-15 + random.randint(0, 2), 15 + random.randint(0, 5), 30 + random.randint(0, 2)])
    pos.append([-10 + random.randint(0, 2), 15 + random.randint(0, 15), 30 + random.randint(0, 2)])


    if mix :
        for _ in range(num_agents):
            if random.random() < 0.2:
                b_position = [5 + random.randint(-random_size, random_size),5 + random.randint(-random_size, random_size), 0 + random.randint(-hight_random_size, hight_random_size)]
            else:
                b_position = [5 + random.randint(-random_size, random_size),5 + random.randint(-random_size, random_size),  30 + random.randint(0, 2)]

            target_pos.append(b_position)
    else:

        for _ in range(num_agents):
            if in_air == False:
                b_position = [5 + random.randint(-random_size, random_size),5 + random.randint(-random_size, random_size), 0 + random.randint(-hight_random_size, hight_random_size)]
            else:
                b_position = [5 + random.randint(-random_size, random_size),5 + random.randint(-random_size, random_size),  30 + random.randint(0, 2)]

            target_pos.append(b_position)

    return pos, target_pos
    