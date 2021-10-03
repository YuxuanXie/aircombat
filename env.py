# -*- coding: utf-8 -*-
import math
import random
import numpy as np
import copy

"""
The enviroment for aircombat.
"""
class Env():
    def __init__(self, n_agent, n_target, target_for_agents = [0, 1, 2, 3]):
        self.n_agent = n_agent
        self.n_target = n_target
        self.target_for_agents = target_for_agents

        # first agent and first target
        # self.r_position_1 = [4+random.randint(-2,2),4+random.randint(-2,2),30+random.randint(0,2)]
        self.r_position_1 = [-20+random.randint(0,2), 15+random.randint(0,5), 30+random.randint(0,2)]
        self.b_position_1 = [5+random.randint(-2,2), 5+random.randint(-2,2), 0]
        self.v_r_1 = 1
        self.v_b_1 = 0.1
        self.gamma_r_1 = 0
        self.gamma_b_1 = 0
        self.pusin_r_1 = 90
        self.pusin_b_1 = 90+random.randint(-10,10)

        # second agent and second target
        self.r_position_2 = [-25+random.randint(0,2), 15+random.randint(0,5), 30+random.randint(0,2)]
        self.b_position_2 =  [-5+random.randint(-2,2), 5+random.randint(-2,2), 0]
        self.v_r_2 = 1
        self.v_b_2 = 0.1
        self.gamma_r_2 = 0
        self.gamma_b_2 = 0
        self.pusin_r_2 = 90
        self.pusin_b_2 = 90+random.randint(-10,10)

        # third agent and third target
        self.r_position_3 = [-25+random.randint(0,2), -15+random.randint(0,15), 30+random.randint(0,2)]
        #self.b_position_3 = [12 + random.randint(-2, 2), 16 + random.randint(-2, 2), 0]
        self.b_position_3 =  [-5+random.randint(-2,2), -5+random.randint(-2,2), 0]
        self.v_r_3 = 1
        self.v_b_3 = 0.1
        self.gamma_r_3 = 0
        self.gamma_b_3 = 0
        self.pusin_r_3 = 90
        self.pusin_b_3 = 90+random.randint(-10,10)

        # forth agent and forth target
        self.r_position_4 = [-20+random.randint(0,2), -15+random.randint(0,15), 30+random.randint(0,2)]
        self.b_position_4 =  [5+random.randint(-2,2), -5+random.randint(-2,2), 0]
        self.v_r_4 = 1
        self.v_b_4 = 0.1
        self.gamma_r_4 = 0
        self.gamma_b_4 = 0
        self.pusin_r_4 = 90
        self.pusin_b_4 = 90+random.randint(-10,10)


        # universal parameters
        self.d = 1
        self.j = 0
        self.MAX_STEPS = 200
        self.done = False

        self.title = 'normal'
        self.title_1 = 'normal'
        self.title_2 = 'normal'
        self.title_3 = 'normal'
        self.title_4 = 'normal'
        self.reward_golbal = 0

        self.flag_1 = 0
        self.flag_2 = 0
        self.flag_3 = 0
        self.flag_4 = 0

        self.target_flag_1 = 0
        self.target_flag_2 = 0
        self.target_flag_3 = 0
        self.target_flag_4 = 0

    

    def reset(self):
        # universal parameters
        self.d = 1
        self.j = 0
        self.MAX_STEPS = 60
        self.done = False

        self.title = 'normal'
        self.title_1 = 'normal'
        self.title_2 = 'normal'
        self.title_3 = 'normal'
        self.title_4 = 'normal'
        self.reward_global = 0

        # 是否完成任务 完成任务后悬停标记 action 选择为 9
        # which uav complete task
        self.flag_1 = 0
        self.flag_2 = 0
        self.flag_3 = 0
        self.flag_4 = 0

        # which target was gone
        self.target_flag_1 = 0
        self.target_flag_2 = 0
        self.target_flag_3 = 0
        self.target_flag_4 = 0

        taishi1, taishi2, taishi3, taishi4 = self.situation_information()
        return self.r_position_1, self.b_position_1, self.r_position_2, self.b_position_2, self.r_position_3, self.b_position_3,self.r_position_4, self.b_position_4,taishi1, taishi2,taishi3,taishi4
    
    def distance3dimensional(self,R,B):
        distance3D = math.sqrt((R[0] - B[0]) ** 2 + (R[1] - B[1]) ** 2 + (R[2] - B[2]) ** 2)
        return distance3D

    def onetaishilist1(self,x_r_1, y_r_1, z_r_1,v_r_1,gamma_r_1,pusin_r_1,x_b_1, y_b_1, z_b_1,v_b_1, gamma_b_1,pusin_b_1):
        d_1 = math.sqrt((x_r_1 - x_b_1) ** 2 + (y_r_1 - y_b_1) ** 2 + (z_r_1 - z_b_1) ** 2)
        q_r_1 = math.acos(((x_b_1 - x_r_1) * math.cos(gamma_r_1 * (3.141592653 / 180)) * math.sin(pusin_r_1 * (3.141592653 / 180)) + (y_b_1 - y_r_1) * math.cos(gamma_r_1 * (3.141592653 / 180)) * math.cos(pusin_r_1 * (3.141592653 / 180)) + (z_b_1 - z_r_1) * math.sin(gamma_r_1 * (3.141592653 / 180))) / d_1)
        q_r__1 = q_r_1 * (180 / 3.141592653)
        q_b_1 = math.acos(((x_r_1 - x_b_1) * math.cos(gamma_b_1 * (3.141592653 / 180)) * math.sin(pusin_b_1 * (3.141592653 / 180)) + (y_r_1 - y_b_1) * math.cos(gamma_b_1 * (3.141592653 / 180)) * math.cos(pusin_b_1 * (3.141592653 / 180)) + (z_r_1 - z_b_1) * math.sin(gamma_b_1 * (3.141592653 / 180))) / d_1)
        q_b__1 = q_b_1 * (180 / 3.141592653)
        temp_1 = math.cos(gamma_r_1 * (3.141592653 / 180)) * math.sin(pusin_r_1 * (3.141592653 / 180)) * math.cos(gamma_b_1 * (3.141592653 / 180)) * math.sin(pusin_b_1 * (3.141592653 / 180)) + math.cos(gamma_r_1 * (3.141592653 / 180)) * math.cos(pusin_r_1 * (3.141592653 / 180)) * math.cos(gamma_b_1 * (3.141592653 / 180)) * math.cos(pusin_b_1 * (3.141592653 / 180)) + math.sin(gamma_r_1 * (3.141592653 / 180)) * math.sin(gamma_b_1 * (3.141592653 / 180))
        #print(temp_1)
        if temp_1>1:
            temp_1 = 1
        if temp_1 <-1:
            temp_1 = -1
        beta_1 = math.acos(temp_1)
        beta__1 = beta_1 * (180 / 3.141592653)
        delta_h_1 = z_r_1 - z_b_1
        delta_v2_1 = v_r_1 ** 2 - v_b_1 ** 2
        v2_1 = v_r_1 ** 2
        h_1 = z_r_1

        taishi1 = [q_r__1, q_b__1, d_1, beta__1, delta_h_1, delta_v2_1, v2_1, h_1]
        taishi1 = self.normalize(taishi1)
        return  taishi1

    def onetaishilist1_2(self, x_r_1, y_r_1, z_r_1, v_r_1, gamma_r_1, pusin_r_1, x_b_1, y_b_1, z_b_1, v_b_1, gamma_b_1,
                       pusin_b_1):
        d_1 = math.sqrt((x_r_1 - x_b_1) ** 2 + (y_r_1 - y_b_1) ** 2 + (z_r_1 - z_b_1) ** 2)
        q_r_1 = math.acos(((x_b_1 - x_r_1) * math.cos(gamma_r_1 * (3.141592653 / 180)) * math.sin(
            pusin_r_1 * (3.141592653 / 180)) + (y_b_1 - y_r_1) * math.cos(gamma_r_1 * (3.141592653 / 180)) * math.cos(
            pusin_r_1 * (3.141592653 / 180)) + (z_b_1 - z_r_1) * math.sin(gamma_r_1 * (3.141592653 / 180))) / d_1)
        q_r__1 = q_r_1 * (180 / 3.141592653)
        q_b_1 = math.acos(((x_r_1 - x_b_1) * math.cos(gamma_b_1 * (3.141592653 / 180)) * math.sin(
            pusin_b_1 * (3.141592653 / 180)) + (y_r_1 - y_b_1) * math.cos(gamma_b_1 * (3.141592653 / 180)) * math.cos(
            pusin_b_1 * (3.141592653 / 180)) + (z_r_1 - z_b_1) * math.sin(gamma_b_1 * (3.141592653 / 180))) / d_1)
        q_b__1 = q_b_1 * (180 / 3.141592653)
        temp_1 = math.cos(gamma_r_1 * (3.141592653 / 180)) * math.sin(pusin_r_1 * (3.141592653 / 180)) * math.cos(
            gamma_b_1 * (3.141592653 / 180)) * math.sin(pusin_b_1 * (3.141592653 / 180)) + math.cos(
            gamma_r_1 * (3.141592653 / 180)) * math.cos(pusin_r_1 * (3.141592653 / 180)) * math.cos(
            gamma_b_1 * (3.141592653 / 180)) * math.cos(pusin_b_1 * (3.141592653 / 180)) + math.sin(
            gamma_r_1 * (3.141592653 / 180)) * math.sin(gamma_b_1 * (3.141592653 / 180))
        # print(temp_1)
        if temp_1 > 1:
            temp_1 = 1
        if temp_1 < -1:
            temp_1 = -1
        beta_1 = math.acos(temp_1)
        beta__1 = beta_1 * (180 / 3.141592653)
        delta_h_1 = z_r_1 - z_b_1
        delta_v2_1 = v_r_1 ** 2 - v_b_1 ** 2
        v2_1 = v_r_1 ** 2
        h_1 = z_r_1

        taishi1 = [q_r__1, q_b__1, d_1, beta__1, delta_h_1, delta_v2_1, v2_1, h_1]
        return taishi1

    def situation_information(self):
        x_r_1, y_r_1, z_r_1 = self.r_position_1
        x_b_1, y_b_1, z_b_1 = self.b_position_1

        x_r_2, y_r_2, z_r_2 = self.r_position_2
        x_b_2, y_b_2, z_b_2 = self.b_position_2

        x_r_3, y_r_3, z_r_3 = self.r_position_3
        x_b_3, y_b_3, z_b_3 = self.b_position_3

        x_r_4, y_r_4, z_r_4 = self.r_position_4
        x_b_4, y_b_4, z_b_4 = self.b_position_4

        v_r_1 = self.v_r_1
        gamma_r_1 = self.gamma_r_1
        pusin_r_1 = self.pusin_r_1
        v_b_1 = self.v_b_1
        gamma_b_1 = self.gamma_b_1
        pusin_b_1 = self.pusin_b_1

        v_r_2 = self.v_r_2
        gamma_r_2 = self.gamma_r_2
        pusin_r_2 = self.pusin_r_2
        v_b_2 = self.v_b_2
        gamma_b_2 = self.gamma_b_2
        pusin_b_2 = self.pusin_b_2

        v_r_3 = self.v_r_3
        gamma_r_3 = self.gamma_r_3
        pusin_r_3 = self.pusin_r_3
        v_b_3 = self.v_b_3
        gamma_b_3 = self.gamma_b_3
        pusin_b_3 = self.pusin_b_3

        v_r_4 = self.v_r_4
        gamma_r_4 = self.gamma_r_4
        pusin_r_4 = self.pusin_r_4
        v_b_4 = self.v_b_4
        gamma_b_4 = self.gamma_b_4
        pusin_b_4 = self.pusin_b_4

        taishi1to1 = self.onetaishilist1(x_r_1, y_r_1, z_r_1, v_r_1, gamma_r_1, pusin_r_1, x_b_1, y_b_1, z_b_1, v_b_1,
                                         gamma_b_1, pusin_b_1)
        taishi1to2 = self.onetaishilist1(x_r_1, y_r_1, z_r_1, v_r_1, gamma_r_1, pusin_r_1, x_b_2, y_b_2, z_b_2, v_b_2,
                                         gamma_b_2, pusin_b_2)
        taishi1to3 = self.onetaishilist1(x_r_1, y_r_1, z_r_1, v_r_1, gamma_r_1, pusin_r_1, x_b_3, y_b_3, z_b_3, v_b_3,
                                         gamma_b_3, pusin_b_3)
        taishi1to4 = self.onetaishilist1(x_r_1, y_r_1, z_r_1, v_r_1, gamma_r_1, pusin_r_1, x_b_4, y_b_4, z_b_4, v_b_4,
                                         gamma_b_4, pusin_b_4)
        taishi1s = [taishi1to1, taishi1to2, taishi1to3, taishi1to4]
        taishi1 = taishi1s[self.target_for_agents[0]] * 4

        taishi2to1 = self.onetaishilist1(x_r_2, y_r_2, z_r_2, v_r_2, gamma_r_2, pusin_r_2, x_b_1, y_b_1, z_b_1, v_b_1,
                                         gamma_b_1, pusin_b_1)
        taishi2to2 = self.onetaishilist1(x_r_2, y_r_2, z_r_2, v_r_2, gamma_r_2, pusin_r_2, x_b_2, y_b_2, z_b_2, v_b_2,
                                         gamma_b_2, pusin_b_2)
        taishi2to3 = self.onetaishilist1(x_r_2, y_r_2, z_r_2, v_r_2, gamma_r_2, pusin_r_2, x_b_3, y_b_3, z_b_3, v_b_3,
                                         gamma_b_3, pusin_b_3)
        taishi2to4 = self.onetaishilist1(x_r_2, y_r_2, z_r_2, v_r_2, gamma_r_2, pusin_r_2, x_b_4, y_b_4, z_b_4, v_b_4,
                                         gamma_b_4, pusin_b_4)

        taishi2s = [taishi2to1, taishi2to2, taishi2to3, taishi2to4]
        taishi2 = taishi2s[self.target_for_agents[1]] * 4

        taishi3to1 = self.onetaishilist1(x_r_3, y_r_3, z_r_3, v_r_3, gamma_r_3, pusin_r_3, x_b_1, y_b_1, z_b_1, v_b_1,
                                         gamma_b_1, pusin_b_1)
        taishi3to2 = self.onetaishilist1(x_r_3, y_r_3, z_r_3, v_r_3, gamma_r_3, pusin_r_3, x_b_2, y_b_2, z_b_2, v_b_2,
                                         gamma_b_2, pusin_b_2)
        taishi3to3 = self.onetaishilist1(x_r_3, y_r_3, z_r_3, v_r_3, gamma_r_3, pusin_r_3, x_b_3, y_b_3, z_b_3, v_b_3,
                                         gamma_b_3, pusin_b_3)
        taishi3to4 = self.onetaishilist1(x_r_3, y_r_3, z_r_3, v_r_3, gamma_r_3, pusin_r_3, x_b_4, y_b_4, z_b_4, v_b_4,
                                         gamma_b_4, pusin_b_4)
        taishi3s = [taishi3to1, taishi3to2, taishi3to3, taishi3to4]
        taishi3 = taishi3s[self.target_for_agents[2]] * 4

        taishi4to1 = self.onetaishilist1(x_r_4, y_r_4, z_r_4, v_r_4, gamma_r_4, pusin_r_4, x_b_1, y_b_1, z_b_1, v_b_1,
                                         gamma_b_1, pusin_b_1)
        taishi4to2 = self.onetaishilist1(x_r_4, y_r_4, z_r_4, v_r_4, gamma_r_4, pusin_r_4, x_b_2, y_b_2, z_b_2, v_b_2,
                                         gamma_b_2, pusin_b_2)
        taishi4to3 = self.onetaishilist1(x_r_4, y_r_4, z_r_4, v_r_4, gamma_r_4, pusin_r_4, x_b_3, y_b_3, z_b_3, v_b_3,
                                         gamma_b_3, pusin_b_3)
        taishi4to4 = self.onetaishilist1(x_r_4, y_r_4, z_r_4, v_r_4, gamma_r_4, pusin_r_4, x_b_4, y_b_4, z_b_4, v_b_4,
                                         gamma_b_4, pusin_b_4)
        taishi4s = [taishi4to1 + taishi4to2 + taishi4to3 + taishi4to4]
        taishi4 = taishi4s[self.target_for_agents[3]] * 4

        return taishi1, taishi2, taishi3, taishi4,

    def situation_information_2(self):
        x_r_1, y_r_1, z_r_1 = self.r_position_1
        x_b_1, y_b_1, z_b_1 = self.b_position_1

        x_r_2, y_r_2, z_r_2 = self.r_position_2
        x_b_2, y_b_2, z_b_2 = self.b_position_2

        x_r_3, y_r_3, z_r_3 = self.r_position_3
        x_b_3, y_b_3, z_b_3 = self.b_position_3

        x_r_4, y_r_4, z_r_4 = self.r_position_4
        x_b_4, y_b_4, z_b_4 = self.b_position_4

        v_r_1 = self.v_r_1
        gamma_r_1 = self.gamma_r_1
        pusin_r_1 = self.pusin_r_1
        v_b_1 = self.v_b_1
        gamma_b_1 = self.gamma_b_1
        pusin_b_1 = self.pusin_b_1

        v_r_2 = self.v_r_2
        gamma_r_2 = self.gamma_r_2
        pusin_r_2 = self.pusin_r_2
        v_b_2 = self.v_b_2
        gamma_b_2 = self.gamma_b_2
        pusin_b_2 = self.pusin_b_2

        v_r_3 = self.v_r_3
        gamma_r_3 = self.gamma_r_3
        pusin_r_3 = self.pusin_r_3
        v_b_3 = self.v_b_3
        gamma_b_3 = self.gamma_b_3
        pusin_b_3 = self.pusin_b_3

        v_r_4 = self.v_r_4
        gamma_r_4 = self.gamma_r_4
        pusin_r_4 = self.pusin_r_4
        v_b_4 = self.v_b_4
        gamma_b_4 = self.gamma_b_4
        pusin_b_4 = self.pusin_b_4

        taishi1to1 = self.onetaishilist1_2(x_r_1, y_r_1, z_r_1, v_r_1, gamma_r_1, pusin_r_1, x_b_1, y_b_1, z_b_1, v_b_1,
                                         gamma_b_1, pusin_b_1)
        taishi1to2 = self.onetaishilist1_2(x_r_1, y_r_1, z_r_1, v_r_1, gamma_r_1, pusin_r_1, x_b_2, y_b_2, z_b_2, v_b_2,
                                         gamma_b_2, pusin_b_2)
        taishi1to3 = self.onetaishilist1_2(x_r_1, y_r_1, z_r_1, v_r_1, gamma_r_1, pusin_r_1, x_b_3, y_b_3, z_b_3, v_b_3,
                                         gamma_b_3, pusin_b_3)
        taishi1to4 = self.onetaishilist1_2(x_r_1, y_r_1, z_r_1, v_r_1, gamma_r_1, pusin_r_1, x_b_4, y_b_4, z_b_4, v_b_4,
                                         gamma_b_4, pusin_b_4)
        taishi1 = taishi1to1 + taishi1to2 + taishi1to3 + taishi1to4

        taishi2to1 = self.onetaishilist1_2(x_r_2, y_r_2, z_r_2, v_r_2, gamma_r_2, pusin_r_2, x_b_1, y_b_1, z_b_1, v_b_1,
                                         gamma_b_1, pusin_b_1)
        taishi2to2 = self.onetaishilist1_2(x_r_2, y_r_2, z_r_2, v_r_2, gamma_r_2, pusin_r_2, x_b_2, y_b_2, z_b_2, v_b_2,
                                         gamma_b_2, pusin_b_2)
        taishi2to3 = self.onetaishilist1_2(x_r_2, y_r_2, z_r_2, v_r_2, gamma_r_2, pusin_r_2, x_b_3, y_b_3, z_b_3, v_b_3,
                                         gamma_b_3, pusin_b_3)
        taishi2to4 = self.onetaishilist1_2(x_r_2, y_r_2, z_r_2, v_r_2, gamma_r_2, pusin_r_2, x_b_4, y_b_4, z_b_4, v_b_4,
                                         gamma_b_4, pusin_b_4)
        taishi2 = taishi2to1 + taishi2to2 + taishi2to3 + taishi2to4

        taishi3to1 = self.onetaishilist1_2(x_r_3, y_r_3, z_r_3, v_r_3, gamma_r_3, pusin_r_3, x_b_1, y_b_1, z_b_1, v_b_1,
                                         gamma_b_1, pusin_b_1)
        taishi3to2 = self.onetaishilist1_2(x_r_3, y_r_3, z_r_3, v_r_3, gamma_r_3, pusin_r_3, x_b_2, y_b_2, z_b_2, v_b_2,
                                         gamma_b_2, pusin_b_2)
        taishi3to3 = self.onetaishilist1_2(x_r_3, y_r_3, z_r_3, v_r_3, gamma_r_3, pusin_r_3, x_b_3, y_b_3, z_b_3, v_b_3,
                                         gamma_b_3, pusin_b_3)
        taishi3to4 = self.onetaishilist1_2(x_r_3, y_r_3, z_r_3, v_r_3, gamma_r_3, pusin_r_3, x_b_4, y_b_4, z_b_4, v_b_4,
                                         gamma_b_4, pusin_b_4)
        taishi3 = taishi3to1 + taishi3to2 + taishi3to3 + taishi3to4

        taishi4to1 = self.onetaishilist1_2(x_r_4, y_r_4, z_r_4, v_r_4, gamma_r_4, pusin_r_4, x_b_1, y_b_1, z_b_1, v_b_1,
                                         gamma_b_1, pusin_b_1)
        taishi4to2 = self.onetaishilist1_2(x_r_4, y_r_4, z_r_4, v_r_4, gamma_r_4, pusin_r_4, x_b_2, y_b_2, z_b_2, v_b_2,
                                         gamma_b_2, pusin_b_2)
        taishi4to3 = self.onetaishilist1_2(x_r_4, y_r_4, z_r_4, v_r_4, gamma_r_4, pusin_r_4, x_b_3, y_b_3, z_b_3, v_b_3,
                                         gamma_b_3, pusin_b_3)
        taishi4to4 = self.onetaishilist1_2(x_r_4, y_r_4, z_r_4, v_r_4, gamma_r_4, pusin_r_4, x_b_4, y_b_4, z_b_4, v_b_4,
                                         gamma_b_4, pusin_b_4)
        taishi4 = taishi4to1 + taishi4to2 + taishi4to3 + taishi4to4
        return taishi1, taishi2, taishi3, taishi4,

    def step(self, r_action_number_1, r_action_number_2,r_action_number_3,r_action_number_4):
        self.action(r_action_number_1, r_action_number_2,r_action_number_3,r_action_number_4)
        r_position_next_1, b_position_next_1, r_position_next_2, b_position_next_2, r_position_next_3, b_position_next_3, r_position_next_4, b_position_next_4 = self.generate_next_position()
        if self.v_r_1 == 0:
            self.v_r_1 = 1
        if self.v_r_2 == 0:
            self.v_r_2 = 1
        if self.v_r_3 == 0:
            self.v_r_3 = 1
        if self.v_r_4 == 0:
            self.v_r_4 = 1
        state__1_next,state__2_next,state__3_next,state__4_next=self.situation_information()
        state__1, state__2,state__3,state__4 = self.situation_information_2()

        '''评估奖励'''
        if self.flag_1 == 0:
            reward_1 = self.dangeous_1(state__1)
        else:
            reward_1 = 0
        if self.flag_2 == 0:
            reward_2 = self.dangeous_2(state__2)
        else:
            reward_2 = 0
        if self.flag_3 == 0:
            reward_3 = self.dangeous_3(state__3)
        else :
            reward_3 = 0
        if self.flag_4 == 0:
            reward_4 = self.dangeous_4(state__4)
        else:
            reward_4 = 0

        self.j += 1
        self.dangeous_module_2(r_position_next_1,r_position_next_2,r_position_next_3,r_position_next_4)
        self.reward_global = 0 # reward_1 + reward_2 + reward_3 + reward_4

        if self.title_1 =="1crash2" or self.title_1 == "1crash3" or self.title_1 == "1crash4" or self.title_2 == "2crash3" or self.title_2 == "2crash4" or self.title_3 == "3crash4":
            self.done = True
            self.title = self.title_1 + self.title_2 + self.title_3 + self.title_4 + 'crash'
            self.reward_global = -200
        if self.j == self.MAX_STEPS:
            self.done = True
            self.title = self.title_1 + self.title_2+self.title_3 +self.title_4 +'over_step'
            self.reward_global = -100
        if r_position_next_1[0] > 100 or r_position_next_1[0] < -100 \
                or r_position_next_1[1] > 100 or r_position_next_1[1] < -100 \
                or r_position_next_1[2] > 50 or r_position_next_1[2] < 1 \
                or b_position_next_1[0] > 100 or b_position_next_1[0] < -100 \
                or b_position_next_1[1] > 100 or b_position_next_1[1] < -100 \
                or b_position_next_1[2] > 50 or b_position_next_1[2] < 0 \
                or r_position_next_2[0] > 100 or r_position_next_2[0] < -100 \
                or r_position_next_2[1] > 100 or r_position_next_2[1] < -100 \
                or r_position_next_2[2] > 50 or r_position_next_2[2] < 1 \
                or b_position_next_2[0] > 100 or b_position_next_2[0] < -100 \
                or b_position_next_2[1] > 100 or b_position_next_2[1] < -100 \
                or b_position_next_2[2] > 50 or b_position_next_2[2] < 0 \
                or r_position_next_3[0] > 100 or r_position_next_3[0] < -100 \
                or r_position_next_3[1] > 100 or r_position_next_3[1] < -100 \
                or r_position_next_3[2] > 50 or r_position_next_3[2] < 1 \
                or b_position_next_3[0] > 100 or b_position_next_3[0] < -100 \
                or b_position_next_3[1] > 100 or b_position_next_3[1] < -100 \
                or b_position_next_3[2] > 50 or b_position_next_3[2] < 0 \
                or r_position_next_4[0] > 100 or r_position_next_4[0] < -100 \
                or r_position_next_4[1] > 100 or r_position_next_4[1] < -100 \
                or r_position_next_4[2] > 50 or r_position_next_4[2] < 1 \
                or b_position_next_4[0] > 100 or b_position_next_4[0] < -100 \
                or b_position_next_4[1] > 100 or b_position_next_4[1] < -100 \
                or b_position_next_4[2] > 50 or b_position_next_4[2] < 0:
            self.done = True
            self.title = self.title_1 + self.title_2 + self.title_3 + self.title_4 + 'over_range'
            self.reward_global = -200
        if self.title_1 == 'red_1_win' and self.title_2 == 'red_2_win'and self.title_3 == 'red_3_win'and self.title_4 == 'red_4_win':
            self.done = True
            self.title = self.title_1 + self.title_2+ self.title_3+ self.title_4 + 'winner'
            self.reward_global = 500
        return r_position_next_1, b_position_next_1, r_position_next_2, b_position_next_2,r_position_next_3, b_position_next_3,r_position_next_4, b_position_next_4, state__1_next, state__2_next,state__3_next,state__4_next, self.reward_global, self.flag_1,self.flag_2,self.flag_3,self.flag_4,self.done, self.title

    def action(self, choose_1, choose_2, choose_3, choose_4):
        if choose_1 == 0:
            self.gamma_r_1 = self.gamma_r_1 + 5
            self.pusin_r_1 = self.pusin_r_1 + 5
        elif choose_1 == 1:
            self.gamma_r_1 = self.gamma_r_1 + 5
        elif choose_1 == 2:
            self.gamma_r_1 = self.gamma_r_1 + 5
            self.pusin_r_1 = self.pusin_r_1 - 5
        elif choose_1 == 3:
            self.pusin_r_1 = self.pusin_r_1 + 5
        elif choose_1 == 4:
            self.gamma_r_1 = self.gamma_r_1
            self.pusin_r_1 = self.pusin_r_1
        elif choose_1 == 5:
            self.pusin_r_1 = self.pusin_r_1 - 5
        elif choose_1 == 6:
            self.gamma_r_1 = self.gamma_r_1 - 5
            self.pusin_r_1 = self.pusin_r_1 + 5
        elif choose_1 == 7:
            self.gamma_r_1 = self.gamma_r_1 - 5
        elif choose_1 == 8:
            self.gamma_r_1 = self.gamma_r_1 - 5
            self.pusin_r_1 = self.pusin_r_1 - 5
        elif choose_1 ==9:
            self.gamma_r_1 = self.gamma_r_1
            self.pusin_r_1 = self.pusin_r_1
            self.v_r_1 = 0

        choose_1B = random.normalvariate(0, 1)
        if choose_1B < -1:
            self.pusin_b_1 = self.pusin_b_1 - 1
        elif choose_1B > 1:
            self.pusin_b_1 + self.pusin_b_1 + 1
        else:
            self.pusin_b_1 = self.pusin_b_1

        if choose_2 == 0:
            self.gamma_r_2 = self.gamma_r_2 + 5
            self.pusin_r_2 = self.pusin_r_2 + 5
        elif choose_2 == 1:
            self.gamma_r_2 = self.gamma_r_2 + 5
        elif choose_2 == 2:
            self.gamma_r_2 = self.gamma_r_2 + 5
            self.pusin_r_2 = self.pusin_r_2 - 5
        elif choose_2 == 3:
            self.pusin_r_2 = self.pusin_r_2 + 5
        elif choose_2 == 4:
            self.gamma_r_2 = self.gamma_r_2
            self.pusin_r_2 = self.pusin_r_2
        elif choose_2 == 5:
            self.pusin_r_2 = self.pusin_r_2 - 5
        elif choose_2 == 6:
            self.gamma_r_2 = self.gamma_r_2 - 5
            self.pusin_r_2 = self.pusin_r_2 + 5
        elif choose_2 == 7:
            self.gamma_r_2 = self.gamma_r_2 - 5
        elif choose_2 == 8:
            self.gamma_r_2 = self.gamma_r_2 - 5
            self.pusin_r_2 = self.pusin_r_2 - 5
        elif choose_2 == 9:
            self.gamma_r_1 = self.gamma_r_1
            self.pusin_r_1 = self.pusin_r_1
            self.v_r_2 = 0

        choose_2B = random.normalvariate(0, 1)
        if choose_2B < -1:
            self.pusin_b_2 = self.pusin_b_2 - 1
        elif choose_2B > 1:
            self.pusin_b_2 + self.pusin_b_2 + 1
        else:
            self.pusin_b_2 = self.pusin_b_2
            
        if choose_3 == 0:
            self.gamma_r_3 = self.gamma_r_3 + 5
            self.pusin_r_3 = self.pusin_r_3 + 5
        elif choose_3 == 1:
            self.gamma_r_3 = self.gamma_r_3 + 5
        elif choose_3 == 2:
            self.gamma_r_3 = self.gamma_r_3 + 5
            self.pusin_r_3 = self.pusin_r_3 - 5
        elif choose_3 == 3:
            self.pusin_r_3 = self.pusin_r_3 + 5
        elif choose_3 == 4:
            self.gamma_r_3 = self.gamma_r_3
            self.pusin_r_3 = self.pusin_r_3
        elif choose_3 == 5:
            self.pusin_r_3 = self.pusin_r_3 - 5
        elif choose_3 == 6:
            self.gamma_r_3 = self.gamma_r_3 - 5
            self.pusin_r_3 = self.pusin_r_3 + 5
        elif choose_3 == 7:
            self.gamma_r_3 = self.gamma_r_3 - 5
        elif choose_3 == 8:
            self.gamma_r_3 = self.gamma_r_3 - 5
            self.pusin_r_3 = self.pusin_r_3 - 5
        elif choose_3 ==9:
            self.gamma_r_1 = self.gamma_r_1
            self.pusin_r_1 = self.pusin_r_1
            self.v_r_3 = 0

        choose_3B = random.normalvariate(0, 1)
        if choose_3B < -1:
            self.pusin_b_3 = self.pusin_b_3 - 1
        elif choose_3B > 1:
            self.pusin_b_3 + self.pusin_b_3 + 1
        else:
            self.pusin_b_3 = self.pusin_b_3
        
        if choose_4 == 0:
            self.gamma_r_4 = self.gamma_r_4 + 5
            self.pusin_r_4 = self.pusin_r_4 + 5
        elif choose_4 == 1:
            self.gamma_r_4 = self.gamma_r_4 + 5
        elif choose_4 == 2:
            self.gamma_r_4 = self.gamma_r_4 + 5
            self.pusin_r_4 = self.pusin_r_4 - 5
        elif choose_4 == 3:
            self.pusin_r_4 = self.pusin_r_4 + 5
        elif choose_4 == 4:
            self.gamma_r_4 = self.gamma_r_4
            self.pusin_r_4 = self.pusin_r_4
        elif choose_4 == 5:
            self.pusin_r_4 = self.pusin_r_4 - 5
        elif choose_4 == 6:
            self.gamma_r_4 = self.gamma_r_4 - 5
            self.pusin_r_4 = self.pusin_r_4 + 5
        elif choose_4 == 7:
            self.gamma_r_4 = self.gamma_r_4 - 5
        elif choose_4 == 8:
            self.gamma_r_4 = self.gamma_r_4 - 5
            self.pusin_r_4 = self.pusin_r_4 - 5
        elif choose_4 == 9:
            self.gamma_r_1 = self.gamma_r_1
            self.pusin_r_1 = self.pusin_r_1
            self.v_r_4 = 0

        choose_4B = random.normalvariate(0, 1)
        if choose_4B < -1:
            self.pusin_b_4 = self.pusin_b_4 - 1
        elif choose_4B > 1:
            self.pusin_b_4 + self.pusin_b_4 + 1
        else:
            self.pusin_b_4 = self.pusin_b_4

    def generate_next_position(self):

        x_r_1, y_r_1, z_r_1 = self.r_position_1
        x_b_1, y_b_1, z_b_1 = self.b_position_1

        x_r_2, y_r_2, z_r_2 = self.r_position_2
        x_b_2, y_b_2, z_b_2 = self.b_position_2

        x_r_3, y_r_3, z_r_3 = self.r_position_3
        x_b_3, y_b_3, z_b_3 = self.b_position_3

        x_r_4, y_r_4, z_r_4 = self.r_position_4
        x_b_4, y_b_4, z_b_4 = self.b_position_4
        
        v_r_1 = self.v_r_1
        gamma_r_1 = self.gamma_r_1
        pusin_r_1 = self.pusin_r_1

        v_b_1 = self.v_b_1
        gamma_b_1 = self.gamma_b_1
        pusin_b_1 = self.pusin_b_1

        x_r_1_ = v_r_1 * math.cos(gamma_r_1 * (3.141592653 / 180)) * math.sin(pusin_r_1 * (3.141592653 / 180))
        y_r_1_ = v_r_1 * math.cos(gamma_r_1 * (3.141592653 / 180)) * math.cos(pusin_r_1 * (3.141592653 / 180))
        z_r_1_ = v_r_1 * math.sin(gamma_r_1 * (3.141592653 / 180))

        x_b_1_ = v_b_1 * math.cos(gamma_b_1 * (3.141592653 / 180)) * math.sin(pusin_b_1 * (3.141592653 / 180))
        y_b_1_ = v_b_1 * math.cos(gamma_b_1 * (3.141592653 / 180)) * math.cos(pusin_b_1 * (3.141592653 / 180))
        z_b_1_ = v_b_1 * math.sin(gamma_b_1 * (3.141592653 / 180))

        x_r_1_next = x_r_1 + x_r_1_
        y_r_1_next = y_r_1 + y_r_1_
        z_r_1_next = z_r_1 + z_r_1_

        x_b_1_next = x_b_1 + x_b_1_
        y_b_1_next = y_b_1 + y_b_1_
        z_b_1_next = z_b_1 + z_b_1_

        v_r_2 = self.v_r_2
        gamma_r_2 = self.gamma_r_2
        pusin_r_2 = self.pusin_r_2

        v_b_2 = self.v_b_2
        gamma_b_2 = self.gamma_b_2
        pusin_b_2 = self.pusin_b_2

        x_r_2_ = v_r_2 * math.cos(gamma_r_2 * (3.141592653 / 180)) * math.sin(pusin_r_2 * (3.141592653 / 180))
        y_r_2_ = v_r_2 * math.cos(gamma_r_2 * (3.141592653 / 180)) * math.cos(pusin_r_2 * (3.141592653 / 180))
        z_r_2_ = v_r_2 * math.sin(gamma_r_2 * (3.141592653 / 180))

        x_b_2_ = v_b_2 * math.cos(gamma_b_2 * (3.141592653 / 180)) * math.sin(pusin_b_2 * (3.141592653 / 180))
        y_b_2_ = v_b_2 * math.cos(gamma_b_2 * (3.141592653 / 180)) * math.cos(pusin_b_2 * (3.141592653 / 180))
        z_b_2_ = v_b_2 * math.sin(gamma_b_2 * (3.141592653 / 180))

        x_r_2_next = x_r_2 + x_r_2_
        y_r_2_next = y_r_2 + y_r_2_
        z_r_2_next = z_r_2 + z_r_2_

        x_b_2_next = x_b_2 + x_b_2_
        y_b_2_next = y_b_2 + y_b_2_
        z_b_2_next = z_b_2 + z_b_2_
        
        # third
        v_r_3 = self.v_r_3
        gamma_r_3 = self.gamma_r_3
        pusin_r_3 = self.pusin_r_3

        v_b_3 = self.v_b_3
        gamma_b_3 = self.gamma_b_3
        pusin_b_3 = self.pusin_b_3

        x_r_3_ = v_r_3 * math.cos(gamma_r_3 * (3.141592653 / 180)) * math.sin(pusin_r_3 * (3.141592653 / 180))
        y_r_3_ = v_r_3 * math.cos(gamma_r_3 * (3.141592653 / 180)) * math.cos(pusin_r_3 * (3.141592653 / 180))
        z_r_3_ = v_r_3 * math.sin(gamma_r_3 * (3.141592653 / 180))

        x_b_3_ = v_b_3 * math.cos(gamma_b_3 * (3.141592653 / 180)) * math.sin(pusin_b_3 * (3.141592653 / 180))
        y_b_3_ = v_b_3 * math.cos(gamma_b_3 * (3.141592653 / 180)) * math.cos(pusin_b_3 * (3.141592653 / 180))
        z_b_3_ = v_b_3 * math.sin(gamma_b_3 * (3.141592653 / 180))

        x_r_3_next = x_r_3 + x_r_3_
        y_r_3_next = y_r_3 + y_r_3_
        z_r_3_next = z_r_3 + z_r_3_

        x_b_3_next = x_b_3 + x_b_3_
        y_b_3_next = y_b_3 + y_b_3_
        z_b_3_next = z_b_3 + z_b_3_
        
        #forth
        v_r_4 = self.v_r_4
        gamma_r_4 = self.gamma_r_4
        pusin_r_4 = self.pusin_r_4

        v_b_4 = self.v_b_4
        gamma_b_4 = self.gamma_b_4
        pusin_b_4 = self.pusin_b_4

        x_r_4_ = v_r_4 * math.cos(gamma_r_4 * (3.141592653 / 180)) * math.sin(pusin_r_4 * (3.141592653 / 180))
        y_r_4_ = v_r_4 * math.cos(gamma_r_4 * (3.141592653 / 180)) * math.cos(pusin_r_4 * (3.141592653 / 180))
        z_r_4_ = v_r_4 * math.sin(gamma_r_4 * (3.141592653 / 180))

        x_b_4_ = v_b_4 * math.cos(gamma_b_4 * (3.141592653 / 180)) * math.sin(pusin_b_4 * (3.141592653 / 180))
        y_b_4_ = v_b_4 * math.cos(gamma_b_4 * (3.141592653 / 180)) * math.cos(pusin_b_4 * (3.141592653 / 180))
        z_b_4_ = v_b_4 * math.sin(gamma_b_4 * (3.141592653 / 180))

        x_r_4_next = x_r_4 + x_r_4_
        y_r_4_next = y_r_4 + y_r_4_
        z_r_4_next = z_r_4 + z_r_4_

        x_b_4_next = x_b_4 + x_b_4_
        y_b_4_next = y_b_4 + y_b_4_
        z_b_4_next = z_b_4 + z_b_4_


        position_r_next_1 = [x_r_1_next, y_r_1_next, z_r_1_next]
        position_b_next_1 = [x_b_1_next, y_b_1_next, z_b_1_next]

        position_r_next_2 = [x_r_2_next, y_r_2_next, z_r_2_next]
        position_b_next_2 = [x_b_2_next, y_b_2_next, z_b_2_next]

        position_r_next_3 = [x_r_3_next, y_r_3_next, z_r_3_next]
        position_b_next_3 = [x_b_3_next, y_b_3_next, z_b_3_next]
        
        position_r_next_4 = [x_r_4_next, y_r_4_next, z_r_4_next]
        position_b_next_4 = [x_b_4_next, y_b_4_next, z_b_4_next]
        
        self.r_position_1 = [x_r_1_next, y_r_1_next, z_r_1_next]
        self.b_position_1 = [x_b_1_next, y_b_1_next, z_b_1_next]

        self.r_position_2 = [x_r_2_next, y_r_2_next, z_r_2_next]
        self.b_position_2 = [x_b_2_next, y_b_2_next, z_b_2_next]

        self.r_position_3 = [x_r_3_next, y_r_3_next, z_r_3_next]
        self.b_position_3 = [x_b_3_next, y_b_3_next, z_b_3_next]

        self.r_position_4 = [x_r_4_next, y_r_4_next, z_r_4_next]
        self.b_position_4 = [x_b_4_next, y_b_4_next, z_b_4_next]
        
        return position_r_next_1, position_b_next_1, position_r_next_2, position_b_next_2, position_r_next_3, position_b_next_3, position_r_next_4, position_b_next_4

    def dangeous(self, taishi):
        q_r_, q_b_, d, beta_, delta_h, delta_v2, v2, h = taishi[0:8]
        weight = 0.8
        R1 = 0
        if d < 20:
            if q_r_ < 30 and q_b_ > 30:
                R1 = 65
            elif q_b_ < 30:
                R1 = -50
        elif h < 0 or h > 40:
            R1 = -50
        else:
            R1 = 0
        s1 = (abs(q_r_) * 3.141592653 / 180 + abs(q_b_) * 3.141592653 / 180) / 2 * 3.141592653
        if d > 20:
            s2 = 1
        else:
            s2 = 0.5
        if delta_h > 20:
            s3 = 0.1
        else:
            s3 = 0.5 - (delta_h / 40)
        s = 0.2 * s1 + 0.6 * s2 + 0.2 * s3
        R = weight * R1 - (1 - weight) * s * 10
        return R

    def dangeous_1(self, taishi):
        q_r_, q_b_, d, beta_, delta_h, delta_v2, v2, h = taishi[0:8]
        weight = 0.8
        R1 = 0
        if d < 20:
            if q_r_ < 30 and q_b_ > 30:
                R1 = 65
                self.flag_1 = 1
                self.title_1 = 'red_1_win'
            elif q_b_ < 30:
                R1 = -50
        elif h < 0 or h > 40:
            R1 = -50
        else:
            R1 = 0
        s1 = (abs(q_r_) * 3.141592653 / 180 + abs(q_b_) * 3.141592653 / 180) / 2 * 3.141592653
        if d > 20:
            s2 = 1
        else:
            s2 = 0.5
        if delta_h > 20:
            s3 = 0.1
        else:
            s3 = 0.5 - (delta_h / 40)
        s = 0.2 * s1 + 0.6 * s2 + 0.2 * s3
        R = weight * R1 - (1 - weight) * s * 10
        return R

    def dangeous_2(self, taishi):
        q_r_, q_b_, d, beta_, delta_h, delta_v2, v2, h = taishi[8:16]
        weight = 0.8
        R1 = 0
        if d < 20:
            if q_r_ < 30 and q_b_ > 30:
                R1 = 65
                self.flag_2 = 1
                self.title_2 = 'red_2_win'
            elif q_b_ < 30:
                R1 = -50
        elif h < 0 or h > 40:
            R1 = -50
        else:
            R1 = 0
        s1 = (abs(q_r_) * 3.141592653 / 180 + abs(q_b_) * 3.141592653 / 180) / 2 * 3.141592653
        if d > 20:
            s2 = 1
        else:
            s2 = 0.5
        if delta_h > 20:
            s3 = 0.1
        else:
            s3 = 0.5 - (delta_h / 40)
        s = 0.2 * s1 + 0.6 * s2 + 0.2 * s3
        R = weight * R1 - (1 - weight) * s * 10
        return R

    def dangeous_3(self, taishi):
        q_r_, q_b_, d, beta_, delta_h, delta_v2, v2, h = taishi[16:24]
        weight = 0.8
        R1 = 0
        if d < 20:
            if q_r_ < 30 and q_b_ > 30:
                R1 = 65
                self.flag_3 = 1
                self.title_3 = 'red_3_win'
            elif q_b_ < 30:
                R1 = -50
        elif h < 0 or h > 40:
            R1 = -50
        else:
            R1 = 0
        s1 = (abs(q_r_) * 3.141592653 / 180 + abs(q_b_) * 3.141592653 / 180) / 2 * 3.141592653
        if d > 20:
            s2 = 1
        else:
            s2 = 0.5
        if delta_h > 20:
            s3 = 0.1
        else:
            s3 = 0.5 - (delta_h / 40)
        s = 0.2 * s1 + 0.6 * s2 + 0.2 * s3
        R = weight * R1 - (1 - weight) * s * 10
        return R

    def dangeous_4(self, taishi):
        q_r_, q_b_, d, beta_, delta_h, delta_v2, v2, h = taishi[-8:]
        weight = 0.8
        R1 = 0
        if d < 20:
            if q_r_ < 30 and q_b_ > 30:
                R1 = 65
                self.flag_4 = 1
                self.title_4 = 'red_4_win'
            elif q_b_ < 30:
                R1 = -50
        elif h < 0 or h > 40:
            R1 = -50
        else:
            R1 = 0
        s1 = (abs(q_r_) * 3.141592653 / 180 + abs(q_b_) * 3.141592653 / 180) / 2 * 3.141592653
        if d > 20:
            s2 = 1
        else:
            s2 = 0.5
        if delta_h > 20:
            s3 = 0.1
        else:
            s3 = 0.5 - (delta_h / 40)
        s = 0.2 * s1 + 0.6 * s2 + 0.2 * s3
        R = weight * R1 - (1 - weight) * s * 10
        return R

    def dangeous1_modle_2(self, r_positon1,r_positon2,r_position3,r_position4):
        distance3D1 = self.distance3dimensional(r_positon1,r_positon2)
        distance3D2 = self.distance3dimensional(r_positon1,r_position3)
        distance3D3 = self.distance3dimensional(r_positon1,r_position4)
        if distance3D1 < 0.5:
            self.title_1 = "1crash2"
            self.title_2 = "2crash1"
        if distance3D2 < 0.5:
            self.title_1 = "1crash3"
            self.title_3 = "3crash1"
        if distance3D3 < 0.5:
            self.title_1 = "1crash4"
            self.title_4 = "4crash1"

    def dangeous2_modle_2(self, r_positon2, r_positon3, r_position4):
        distance3D1 = self.distance3dimensional(r_positon2, r_positon3)
        distance3D2 = self.distance3dimensional(r_positon2, r_position4)
        if distance3D1 < 0.5:
            self.title_2 = "2crash3"
            self.title_3 = "3crash2"
        if distance3D2 < 0.5:
            self.title_2 = "2crash4"
            self.title_4 = "4crash2"

    def dangeous3_modle_2(self, r_positon3, r_position4):
        distance3D1 = self.distance3dimensional(r_positon3, r_position4)
        if distance3D1 < 0.5:
            self.title_3 = "3crash4"
            self.title_4 = "4crash3"

    def dangeous_module_2(self,r_position_next_1, r_position_next_2, r_position_next_3, r_position_next_4):
        self.dangeous1_modle_2(r_position_next_1,r_position_next_2,r_position_next_3,r_position_next_4)
        self.dangeous2_modle_2(r_position_next_2,r_position_next_3,r_position_next_4)
        self.dangeous3_modle_2(r_position_next_3,r_position_next_4)


    def action_b(self, action_b):
        v_b_1_ = action_b[0]
        gamma_b_1 = action_b[1]
        pusin_b_1 = action_b[2]
        action_b = [v_b_1_, gamma_b_1, pusin_b_1]
        return action_b

    def normalize(self, taishi):
        taishi[0] = (taishi[0])/180
        taishi[1] = (taishi[0])/180
        taishi[2] = (taishi[2]-1)/(math.sqrt(80900)-1)
        taishi[3] =  (taishi[3])/180
        taishi[4] = (taishi[4]-1)/49
        taishi[5] = taishi[5]
        taishi[6] = taishi[6]
        taishi[7] = (taishi[7]-1)/49
        return taishi
    def unnormalize(self,taishi):
        taishi[0] = (taishi[0]) * 180
        taishi[1] = (taishi[0]) * 180
        taishi[2] = (taishi[2] * (math.sqrt(80900) - 1))+1
        taishi[3] = (taishi[3]) * 180
        taishi[4] = (taishi[4] * 49)+1
        taishi[5] = taishi[5]
        taishi[6] = taishi[6]
        taishi[7] = (taishi[7] * 49) +1



    def distribution_target(self):
        return []



    def threat_degree_to_ground_matrix_calculation(self):
        threat_degree_to_ground = np.zeros((4,4))
        # Fisrt factors: air combat capability matrix calculation
        toground_combat_capability = np.zeros((4, 4))
        for i in range(4):
            for j in range(4):
                if i == 0:
                    toground_combat_capability[i][j] = self.Ground_combat_capability_r_1
                elif i == 1:
                    toground_combat_capability[i][j] = self.Ground_combat_capability_r_2
                elif i == 2:
                    toground_combat_capability[i][j] = self.Ground_combat_capability_r_3
                elif i == 3:
                    toground_combat_capability[i][j] = self.Ground_combat_capability_r_4
        #print(toground_combat_capability)
        # second factor :Speed comparison calculation
        Speed_comparison_calculation = np.zeros((4,4))
        vt_list = [self.v_r_1,self.v_r_2,self.v_r_3,self.v_r_4]
        vi_list = [self.v_b_1,self.v_b_2,self.v_b_3,self.v_b_4]
        for i in range(4):
            for j in range(4):
                Speed_comparison_calculation[i][j] = self.calculate_speed_comparison(vt_list[i],vi_list[j])
        #print(Speed_comparison_calculation)
        # third facotr: angle comparison calculation
        Angle_comparison_calculation = np.zeros((4, 4))
        r_position_list = [self.r_position_1,self.r_position_2,self.r_position_3,self.r_position_4]
        b_position_list = [self.b_position_1,self.b_position_2,self.b_position_3,self.b_position_4]
        gamma_r_list = [self.gamma_r_1,self.gamma_r_2,self.gamma_r_3,self.gamma_r_4]
        pusin_r_list = [self.pusin_r_1,self.pusin_r_2,self.pusin_r_3,self.pusin_r_4]
        for i in range(4):
            for j in range(4):
                Angle_comparison_calculation[i][j] = self.calculate_angle_comparison(r_position_list[i],gamma_r_list[i],pusin_r_list[i],b_position_list[j])
        #print(Angle_comparison_calculation)
        # forth factor
        r_height_list = [self.r_position_1[2],self.r_position_2[2],self.r_position_3[2],self.r_position_4[2]]
        height_comparison_calculation = np.zeros((4, 4))
        for i in range(4):
            for j in range(4):
                height_comparison_calculation[i][j] = self.calculate_height_comparison(r_height_list[i])
        #print(height_comparison_calculation)
        for i in range(4):
            for j in range(4):
                threat_degree_to_ground = 0.284*toground_combat_capability[i][j] +0.175*Speed_comparison_calculation[i][j] + 0.485*Angle_comparison_calculation[i][j] +0.056*height_comparison_calculation[i][j]
        return threat_degree_to_ground
    def calculate_speed_comparison(self,vt,vi):
        if vt < 0.6 * vi:
            return 0.1
        elif vt <= 1.5  * vi:
            return -0.5 + vt/vi
        else:
            return 1.0
    def calculate_angle_comparison(self, r_positon, gamma_r,pusin_r,b_position):
        # entry angle calculate
        x_r_1, y_r_1, z_r_1 = r_positon
        x_b_1, y_b_1, z_b_1 = b_position
        gamma_r_1 = gamma_r
        pusin_r_1 = pusin_r
        d_1 = math.sqrt((x_r_1 - x_b_1) ** 2 + (y_r_1 - y_b_1) ** 2 + (z_r_1 - z_b_1) ** 2)
        q_r_1 = math.acos(((x_b_1 - x_r_1) * math.cos(gamma_r_1 * (3.141592653 / 180)) * math.sin(
            pusin_r_1 * (3.141592653 / 180)) + (y_b_1 - y_r_1) * math.cos(gamma_r_1 * (3.141592653 / 180)) * math.cos(
            pusin_r_1 * (3.141592653 / 180)) + (z_b_1 - z_r_1) * math.sin(gamma_r_1 * (3.141592653 / 180))) / d_1)
        if q_r_1 >= 90  and q_r_1 <= 90 :
            return 1 - (q_r_1/90)**2
        else:
            return 0
    def calculate_height_comparison(self,height):
        if height < 10:
            return 1
        else:
            return math.e**((10 - height)/500)

    def calculate_distance(self,):
        distance_matrix = np.zeros((4,4))
        x_r_1, y_r_1, z_r_1 = self.r_position_1
        x_b_1, y_b_1, z_b_1 = self.b_position_1

        x_r_2, y_r_2, z_r_2 = self.r_position_2
        x_b_2, y_b_2, z_b_2 = self.b_position_2

        x_r_3, y_r_3, z_r_3 = self.r_position_3
        x_b_3, y_b_3, z_b_3 = self.b_position_3

        x_r_4, y_r_4, z_r_4 = self.r_position_4
        x_b_4, y_b_4, z_b_4 = self.b_position_4

        distance_matrix[0][0] = distance(x_r_1,y_r_1,z_r_1,x_b_1,y_b_1,z_b_1)
        distance_matrix[0][1] = distance(x_r_1,y_r_1,z_r_1,x_b_2,y_b_2,z_b_2)
        distance_matrix[0][2] = distance(x_r_1,y_r_1,z_r_1,x_b_3,y_b_3,z_b_3)
        distance_matrix[0][3] = distance(x_r_1,y_r_1,z_r_1,x_b_4,y_b_4,z_b_4)

        distance_matrix[1][0] = distance(x_r_2,y_r_2,z_r_2,x_b_1,y_b_1,z_b_1)
        distance_matrix[1][1] = distance(x_r_2,y_r_2,z_r_2,x_b_2,y_b_2,z_b_2)
        distance_matrix[1][2] = distance(x_r_2,y_r_2,z_r_2,x_b_3,y_b_3,z_b_3)
        distance_matrix[1][3] = distance(x_r_2,y_r_2,z_r_2,x_b_4,y_b_4,z_b_4)

        distance_matrix[2][0] = distance(x_r_3,y_r_3,z_r_3,x_b_1,y_b_1,z_b_1)
        distance_matrix[2][1] = distance(x_r_3,y_r_3,z_r_3,x_b_2,y_b_2,z_b_2)
        distance_matrix[2][2] = distance(x_r_3,y_r_3,z_r_3,x_b_3,y_b_3,z_b_3)
        distance_matrix[2][3] = distance(x_r_3,y_r_3,z_r_3,x_b_4,y_b_4,z_b_4)

        distance_matrix[3][0] = distance(x_r_4,y_r_4,z_r_4,x_b_1,y_b_1,z_b_1)
        distance_matrix[3][1] = distance(x_r_4,y_r_4,z_r_4,x_b_2,y_b_2,z_b_2)
        distance_matrix[3][2] = distance(x_r_4,y_r_4,z_r_4,x_b_3,y_b_3,z_b_3)
        distance_matrix[3][3] = distance(x_r_4,y_r_4,z_r_4,x_b_4,y_b_4,z_b_4)

        return  distance_matrix





def distance(x_r_1,y_r_1,z_r_1,x_b_1,y_b_1,z_b_1):
    d = math.sqrt((x_r_1 - x_b_1) ** 2 + (y_r_1 - y_b_1) ** 2 + (z_r_1 - z_b_1) ** 2)
    return d

if __name__ == '__main__':
    env = Env(4,4)
    env.reset()
    env.step(1,1,1,1)
    a = env.distribution_target()


