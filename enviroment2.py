import math
import random


class Env():
    def __init__(self, n_agent, n_target):
        self.n_agent = n_agent
        self.n_target = n_target

        # first agent and first target
        # self.r_position_1 = [4+random.randint(-2,2),4+random.randint(-2,2),30+random.randint(0,2)]
        self.r_position_1 = [4, 4, 30]
        self.b_position_1 = [12+random.randint(-3,3), 16+random.randint(-3,3), 0]
        self.v_r_1 = 1
        self.v_b_1 = 0.02
        self.gamma_r_1 = 0
        self.gamma_b_1 = 0
        self.pusin_r_1 = 0
        self.pusin_b_1 = 0

        self.active_r_1 = [self.v_r_1, self.gamma_r_1, self.pusin_r_1]
        self.active_b_1 = [self.v_b_1, self.gamma_b_1, self.pusin_b_1]

        # second agent and second target
        self.r_position_2 = [4, 28, 30]
        self.b_position_2 = [12+random.randint(-3,3), 16+random.randint(-3,3), 0]
        self.v_r_2 = 1
        self.v_b_2 = 0.02
        self.gamma_r_2 = 0
        self.gamma_b_2 = 0
        self.pusin_r_2 = 180
        self.pusin_b_2 = 180

        self.active_r_2 = [self.v_r_2, self.gamma_r_2, self.pusin_r_2]
        self.active_b_2 = [self.v_b_2, self.gamma_b_2, self.pusin_b_2]

        # third agent and third target
        self.r_position_3 = [20, 4, 30]
        self.b_position_3 =[12+random.randint(-3,3), 16+random.randint(-3,3), 0]
        self.v_r_3 = 1
        self.v_b_3 = 0.02
        self.gamma_r_3 = 0
        self.gamma_b_3 = 0
        self.pusin_r_3 = 0
        self.pusin_b_3 = 0

        self.active_r_3 = [self.v_r_3, self.gamma_r_3, self.pusin_r_3]
        self.active_b_3 = [self.v_b_3, self.gamma_b_3, self.pusin_b_3]

        # forth agent and forth target
        self.r_position_4 = [20, 28, 30]
        self.b_position_4 = [12+random.randint(-3,3), 16+random.randint(-3,3), 0]
        self.v_r_4 = 1
        self.v_b_4 = 0.02
        self.gamma_r_4 = 0
        self.gamma_b_4 = 0
        self.pusin_r_4 = 180
        self.pusin_b_4 = 180

        self.active_r_4 = [self.v_r_4, self.gamma_r_4, self.pusin_r_4]
        self.active_b_4 = [self.v_b_4, self.gamma_b_4, self.pusin_b_4]

        # universal parameters
        self.d = 1
        self.j = 0
        self.MAX_STEPS = 100
        self.done = False

        self.title = 'normal'
        self.title_1 = 'normal_first'
        self.title_2 = 'normal_second'
        self.title_3 = 'normal_third'
        self.title_4 = 'normal_forth'

    def reset(self):
        self.r_position_1 = [4, 4, 30]
        self.b_position_1 = [12+random.randint(-3,3), 16+random.randint(-3,3), 0]
        self.v_r_1 = 1
        self.v_b_1 = 0
        self.gamma_r_1 = 0
        self.gamma_b_1 = 0
        self.pusin_r_1 = 0
        self.pusin_b_1 = 0

        self.active_r_1 = [self.v_r_1, self.gamma_r_1, self.pusin_r_1]
        self.active_b_1 = [self.v_b_1, self.gamma_b_1, self.pusin_b_1]

        # second agent and second target
        self.r_position_2 = [4, 28, 30]
        self.b_position_2 = [12+random.randint(-3,3), 16+random.randint(-3,3), 0]
        self.v_r_2 = 1
        self.v_b_2 = 0
        self.gamma_r_2 = 0
        self.gamma_b_2 = 0
        self.pusin_r_2 = 180
        self.pusin_b_2 = 180

        self.active_r_2 = [self.v_r_2, self.gamma_r_2, self.pusin_r_2]
        self.active_b_2 = [self.v_b_2, self.gamma_b_2, self.pusin_b_2]

        # third agent and third target
        self.r_position_3 = [20, 4, 30]
        self.b_position_3 = [12+random.randint(-3,3), 16+random.randint(-3,3), 0]
        self.v_r_3 = 1
        self.v_b_3 = 0.02
        self.gamma_r_3 = 0
        self.gamma_b_3 = 0
        self.pusin_r_3 = 0
        self.pusin_b_3 = 0

        self.active_r_3 = [self.v_r_3, self.gamma_r_3, self.pusin_r_3]
        self.active_b_3 = [self.v_b_3, self.gamma_b_3, self.pusin_b_3]

        # forth agent and forth target
        self.r_position_4 = [20, 28, 30]
        self.b_position_4 = [12+random.randint(-3,3), 16+random.randint(-3,3), 0]
        self.v_r_4 = 1
        self.v_b_4 = 0.02
        self.gamma_r_4 = 0
        self.gamma_b_4 = 0
        self.pusin_r_4 = 180
        self.pusin_b_4 = 180

        self.active_r_4 = [self.v_r_4, self.gamma_r_4, self.pusin_r_4]
        self.active_b_4 = [self.v_b_4, self.gamma_b_4, self.pusin_b_4]

        # universal parameters
        self.d = 1
        self.j = 0
        self.MAX_STEPS = 100
        self.done = False

        self.title = 'normal'
        self.title_1 = 'normal_first'
        self.title_2 = 'normal_second'
        self.title_3 = 'normal_third'
        self.title_4 = 'normal_forth'

        taishi1, taishi2, taishi3, taishi4 = self.situation_information()
        return self.r_position_1, self.b_position_1, self.r_position_2, self.b_position_2, self.r_position_3, self.b_position_3, self.r_position_4, self.b_position_4, taishi1, taishi2, taishi3, taishi4

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

        v_r_2 = self.v_r_2
        gamma_r_2 = self.gamma_r_2
        pusin_r_2 = self.pusin_r_2
        v_b_2 = self.v_b_2
        gamma_b_2 = self.gamma_b_2
        pusin_b_2 = self.pusin_b_2

        d_2 = math.sqrt((x_r_2 - x_b_2) ** 2 + (y_r_2 - y_b_2) ** 2 + (z_r_2 - z_b_2) ** 2)
        q_r_2 = math.acos(((x_b_2 - x_r_2) * math.cos(gamma_r_2 * (3.141592653 / 180)) * math.sin(
            pusin_r_2 * (3.141592653 / 180)) + (y_b_2 - y_r_2) * math.cos(gamma_r_2 * (3.141592653 / 180)) * math.cos(
            pusin_r_2 * (3.141592653 / 180)) + (z_b_2 - z_r_2) * math.sin(gamma_r_2 * (3.141592653 / 180))) / d_2)
        q_r__2 = q_r_2 * (180 / 3.141592653)
        q_b_2 = math.acos(((x_r_2 - x_b_2) * math.cos(gamma_b_2 * (3.141592653 / 180)) * math.sin(
            pusin_b_2 * (3.141592653 / 180)) + (y_r_2 - y_b_2) * math.cos(gamma_b_2 * (3.141592653 / 180)) * math.cos(
            pusin_b_2 * (3.141592653 / 180)) + (z_r_2 - z_b_2) * math.sin(gamma_b_2 * (3.141592653 / 180))) / d_2)
        q_b__2 = q_b_2 * (180 / 3.141592653)
        temp_2 = math.cos(gamma_r_2 * (3.141592653 / 180)) * math.sin(pusin_r_2 * (3.141592653 / 180)) * math.cos(
            gamma_b_2 * (3.141592653 / 180)) * math.sin(pusin_b_2 * (3.141592653 / 180)) + math.cos(
            gamma_r_2 * (3.141592653 / 180)) * math.cos(pusin_r_2 * (3.141592653 / 180)) * math.cos(
            gamma_b_2 * (3.141592653 / 180)) * math.cos(pusin_b_2 * (3.141592653 / 180)) + math.sin(
            gamma_r_2 * (3.141592653 / 180)) * math.sin(gamma_b_2 * (3.141592653 / 180))
        # print(temp_2)
        if temp_2 > 1:
            temp_2 = 1
        if temp_2 < -1:
            temp_2 = -1
        beta_2 = math.acos(temp_2)
        beta__2 = beta_2 * (180 / 3.141592653)
        delta_h_2 = z_r_2 - z_b_2
        delta_v2_2 = v_r_2 ** 2 - v_b_2 ** 2
        v2_2 = v_r_2 ** 2
        h_2 = z_r_2

        v_r_3 = self.v_r_3
        gamma_r_3 = self.gamma_r_3
        pusin_r_3 = self.pusin_r_3
        v_b_3 = self.v_b_3
        gamma_b_3 = self.gamma_b_3
        pusin_b_3 = self.pusin_b_3

        d_3 = math.sqrt((x_r_3 - x_b_3) ** 2 + (y_r_3 - y_b_3) ** 2 + (z_r_3 - z_b_3) ** 2)
        q_r_3 = math.acos(((x_b_3 - x_r_3) * math.cos(gamma_r_3 * (3.141592653 / 180)) * math.sin(
            pusin_r_3 * (3.141592653 / 180)) + (y_b_3 - y_r_3) * math.cos(gamma_r_3 * (3.141592653 / 180)) * math.cos(
            pusin_r_3 * (3.141592653 / 180)) + (z_b_3 - z_r_3) * math.sin(gamma_r_3 * (3.141592653 / 180))) / d_3)
        q_r__3 = q_r_3 * (180 / 3.141592653)
        q_b_3 = math.acos(((x_r_3 - x_b_3) * math.cos(gamma_b_3 * (3.141592653 / 180)) * math.sin(
            pusin_b_3 * (3.141592653 / 180)) + (y_r_3 - y_b_3) * math.cos(gamma_b_3 * (3.141592653 / 180)) * math.cos(
            pusin_b_3 * (3.141592653 / 180)) + (z_r_3 - z_b_3) * math.sin(gamma_b_3 * (3.141592653 / 180))) / d_3)
        q_b__3 = q_b_3 * (180 / 3.141592653)
        temp_3 = math.cos(gamma_r_3 * (3.141592653 / 180)) * math.sin(pusin_r_3 * (3.141592653 / 180)) * math.cos(
            gamma_b_3 * (3.141592653 / 180)) * math.sin(pusin_b_3 * (3.141592653 / 180)) + math.cos(
            gamma_r_3 * (3.141592653 / 180)) * math.cos(pusin_r_3 * (3.141592653 / 180)) * math.cos(
            gamma_b_3 * (3.141592653 / 180)) * math.cos(pusin_b_3 * (3.141592653 / 180)) + math.sin(
            gamma_r_3 * (3.141592653 / 180)) * math.sin(gamma_b_3 * (3.141592653 / 180))
        # print(temp_3)
        if temp_3 > 1:
            temp_3 = 1
        if temp_3 < -1:
            temp_3 = -1
        beta_3 = math.acos(temp_3)
        beta__3 = beta_3 * (180 / 3.141592653)
        delta_h_3 = z_r_3 - z_b_3
        delta_v2_3 = v_r_3 ** 2 - v_b_3 ** 2
        v2_3 = v_r_3 ** 2
        h_3 = z_r_3

        v_r_4 = self.v_r_4
        gamma_r_4 = self.gamma_r_4
        pusin_r_4 = self.pusin_r_4
        v_b_4 = self.v_b_4
        gamma_b_4 = self.gamma_b_4
        pusin_b_4 = self.pusin_b_4

        d_4 = math.sqrt((x_r_4 - x_b_4) ** 2 + (y_r_4 - y_b_4) ** 2 + (z_r_4 - z_b_4) ** 2)
        q_r_4 = math.acos(((x_b_4 - x_r_4) * math.cos(gamma_r_4 * (3.141592653 / 180)) * math.sin(
            pusin_r_4 * (3.141592653 / 180)) + (y_b_4 - y_r_4) * math.cos(gamma_r_4 * (3.141592653 / 180)) * math.cos(
            pusin_r_4 * (3.141592653 / 180)) + (z_b_4 - z_r_4) * math.sin(gamma_r_4 * (3.141592653 / 180))) / d_4)
        q_r__4 = q_r_4 * (180 / 3.141592653)
        q_b_4 = math.acos(((x_r_4 - x_b_4) * math.cos(gamma_b_4 * (3.141592653 / 180)) * math.sin(
            pusin_b_4 * (3.141592653 / 180)) + (y_r_4 - y_b_4) * math.cos(gamma_b_4 * (3.141592653 / 180)) * math.cos(
            pusin_b_4 * (3.141592653 / 180)) + (z_r_4 - z_b_4) * math.sin(gamma_b_4 * (3.141592653 / 180))) / d_4)
        q_b__4 = q_b_4 * (180 / 3.141592653)
        temp_4 = math.cos(gamma_r_4 * (3.141592653 / 180)) * math.sin(pusin_r_4 * (3.141592653 / 180)) * math.cos(
            gamma_b_4 * (3.141592653 / 180)) * math.sin(pusin_b_4 * (3.141592653 / 180)) + math.cos(
            gamma_r_4 * (3.141592653 / 180)) * math.cos(pusin_r_4 * (3.141592653 / 180)) * math.cos(
            gamma_b_4 * (3.141592653 / 180)) * math.cos(pusin_b_4 * (3.141592653 / 180)) + math.sin(
            gamma_r_4 * (3.141592653 / 180)) * math.sin(gamma_b_4 * (3.141592653 / 180))
        # print(temp_4)
        if temp_4 > 1:
            temp_4 = 1
        if temp_4 < -1:
            temp_4 = -1
        beta_4 = math.acos(temp_4)
        beta__4 = beta_4 * (180 / 3.141592653)
        delta_h_4 = z_r_4 - z_b_4
        delta_v2_4 = v_r_4 ** 2 - v_b_4 ** 2
        v2_4 = v_r_4 ** 2
        h_4 = z_r_4

        taishi1 = [q_r__1, q_b__1, d_1, beta__1, delta_h_1, delta_v2_1, v2_1, h_1]
        taishi2 = [q_r__2, q_b__2, d_2, beta__2, delta_h_2, delta_v2_2, v2_2, h_2]
        taishi3 = [q_r__3, q_b__3, d_3, beta__3, delta_h_3, delta_v2_3, v2_3, h_3]
        taishi4 = [q_r__4, q_b__4, d_4, beta__4, delta_h_4, delta_v2_4, v2_4, h_4]

        return taishi1, taishi2, taishi3, taishi4,

    def step(self, r_action_number_1, r_action_number_2, r_action_number_3, r_action_number_4):
        flag_1 = 0
        flag_2 = 0
        flag_3 = 0
        flag_4 = 0
        self.action(r_action_number_1, r_action_number_2, r_action_number_3, r_action_number_4)
        r_position_next_1, b_position_next_1, r_position_next_2, b_position_next_2, r_position_next_3, b_position_next_3, r_position_next_4, b_position_next_4 = self.generate_next_position()
        state__1, state__2, state__3, state__4 = self.situation_information()
        reward_1 = self.dangeous(state__1)
        reward_2 = self.dangeous(state__2)
        reward_3 = self.dangeous(state__3)
        reward_4 = self.dangeous(state__4)
        self.j += 1
        q_r__1, q_b__1, d_1, beta__1, delta_h_1, delta_v2_1, v2_1, h_1 = state__1
        q_r__2, q_b__2, d_2, beta__2, delta_h_2, delta_v2_2, v2_2, h_2 = state__2
        q_r__3, q_b__3, d_3, beta__3, delta_h_3, delta_v3_3, v3_3, h_3 = state__3
        q_r__4, q_b__4, d_4, beta__4, delta_h_4, delta_v4_4, v4_4, h_4 = state__4

        if self.j == self.MAX_STEPS:
            self.done = True
            self.title = self.title_1 + self.title_2 + self.title_3 + self.title_4 + 'over_step'
        if d_1 < 20 and q_r__1 < 30 and q_b__1 > 30:
            self.v_r_1 = 0
            self.title_1 = 'red_1_win'
            flag_1 = 1
        if d_1 < 20 and q_b__1 < 30:
            self.done = True
            self.title = 'blue_1_win'
        if d_2 < 20 and q_r__2 < 30 and q_b__2 > 30:
            self.v_r_2 = 0
            self.title_2 = 'red_2_win'
            flag_2 = 1
        if d_1 < 20 and q_b__1 < 30:
            self.done = True
            self.title = 'blue_2_win'
        if d_3 < 20 and q_r__3 < 30 and q_b__3 > 30:
            self.v_r_3 = 0
            self.title_3 = 'red_3_win'
            flag_3 = 1
        if d_3 < 20 and q_b__3 < 30:
            self.done = True
            self.title = 'blue_3_win'
        if d_4 < 20 and q_r__4 < 30 and q_b__4 > 30:
            self.v_r_4 = 0
            self.title_4 = 'red_4_win'
        if d_4 < 20 and q_b__4 < 30:
            self.done = True
            self.title = 'blue_4_win'
            flag_4 = 1
        if r_position_next_1[0] > 50 or r_position_next_1[0] < -30 \
                or r_position_next_1[1] > 50 or r_position_next_1[1] < -30 \
                or r_position_next_1[2] > 50 or r_position_next_1[2] < 1 \
                or b_position_next_1[0] > 50 or b_position_next_1[0] < -30 \
                or b_position_next_1[1] > 50 or b_position_next_1[1] < -30 \
                or b_position_next_1[2] > 50 or b_position_next_1[2] < 0 \
                or r_position_next_2[0] > 50 or r_position_next_2[0] < -30 \
                or r_position_next_2[1] > 50 or r_position_next_2[1] < -30 \
                or r_position_next_2[2] > 50 or r_position_next_2[2] < 1 \
                or b_position_next_2[0] > 50 or b_position_next_2[0] < -30 \
                or b_position_next_2[1] > 50 or b_position_next_2[1] < -30 \
                or b_position_next_2[2] > 50 or b_position_next_2[2] < 0 \
                or r_position_next_3[0] > 50 or r_position_next_3[0] < -30 \
                or r_position_next_3[1] > 50 or r_position_next_3[1] < -30 \
                or r_position_next_3[2] > 50 or r_position_next_3[2] < 1 \
                or b_position_next_3[0] > 50 or b_position_next_3[0] < -30 \
                or b_position_next_3[1] > 50 or b_position_next_3[1] < -30 \
                or b_position_next_3[2] > 50 or b_position_next_3[2] < 0 \
                or r_position_next_4[0] > 50 or r_position_next_4[0] < -30 \
                or r_position_next_4[1] > 50 or r_position_next_4[1] < -30 \
                or r_position_next_4[2] > 50 or r_position_next_4[2] < 1 \
                or b_position_next_4[0] > 50 or b_position_next_4[0] < -30 \
                or b_position_next_4[1] > 50 or b_position_next_4[1] < -30 \
                or b_position_next_4[2] > 50 or b_position_next_4[2] < 0:
            self.done = True
            self.title = self.title_1 + self.title_2 + self.title_3 + self.title_4 + 'over_range'
        if self.title_1 == 'red_1_win' and self.title_2 == 'red_2_win' and self.title_3 == 'red_3_win' and self.title_4 == 'red_4_win':
            self.done = True
            self.title = self.title_1 + self.title_2 + self.title_3 + self.title_4 + 'winner'
        return r_position_next_1, b_position_next_1, r_position_next_2, b_position_next_2, r_position_next_3, b_position_next_3, r_position_next_4, b_position_next_4, state__1, state__2, state__3, state__4, reward_1, reward_2, reward_3, reward_4, flag_1, flag_2, flag_3, flag_4, self.done, self.title

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
        choose_1B = random.normalvariate(0, 1)
        if choose_1B < -2.58:
            self.pusin_b_1 = self.pusin_b_1 - 5
        elif choose_1B > 2.58:
            self.pusin_b_1 + self.pusin_b_1 + 5
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

        choose_2B = random.normalvariate(0, 1)
        if choose_2B < -2.58:
            self.pusin_b_2 = self.pusin_b_2 - 5
        elif choose_1B > 2.58:
            self.pusin_b_2 + self.pusin_b_2 + 5
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

        choose_3B = random.normalvariate(0, 1)
        if choose_3B < -2.58:
            self.pusin_b_3 = self.pusin_b_3 - 5
        elif choose_1B > 2.58:
            self.pusin_b_3 + self.pusin_b_3 + 5
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

        choose_4B = random.normalvariate(0, 1)
        if choose_4B < -2.58:
            self.pusin_b_4 = self.pusin_b_4 - 5
        elif choose_4B > 2.58:
            self.pusin_b_4 + self.pusin_b_4 + 5
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

        # forth
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

    def interact_with_enviroment(self, position_r, position_b, action_r, action_b):
        x_r_1 = position_r[0]
        x_b_1 = position_b[0]
        y_r_1 = position_r[1]
        y_b_1 = position_b[1]
        z_r_1 = position_r[2]
        z_b_1 = position_b[2]
        v_r_1 = action_r[0]
        gamma_r_1 = action_r[1]
        pusin_r_1 = action_r[2]
        v_b_1 = action_b[0]
        gamma_b_1 = action_b[1]
        pusin_b_1 = action_b[2]

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

        position_r_next = [x_r_1_next, y_r_1_next, z_r_1_next]
        position_b_next = [x_b_1_next, y_b_1_next, z_b_1_next]

        d = math.sqrt((x_r_1 - x_b_1) ** 2 + (y_r_1 - y_b_1) ** 2 + (z_r_1 - z_b_1) ** 2)
        q_r = math.acos(((x_b_1 - x_r_1) * math.cos(gamma_r_1 * (3.141592653 / 180)) * math.sin(
            pusin_r_1 * (3.141592653 / 180)) + (y_b_1 - y_r_1) * math.cos(gamma_r_1 * (3.141592653 / 180)) * math.cos(
            pusin_r_1 * (3.141592653 / 180)) + (z_b_1 - z_r_1) * math.sin(gamma_r_1 * (3.141592653 / 180))) / d)
        q_r_ = q_r * (180 / 3.141592653)
        q_b = math.acos(((x_r_1 - x_b_1) * math.cos(gamma_b_1 * (3.141592653 / 180)) * math.sin(
            pusin_b_1 * (3.141592653 / 180)) + (y_r_1 - y_b_1) * math.cos(gamma_b_1 * (3.141592653 / 180)) * math.cos(
            pusin_b_1 * (3.141592653 / 180)) + (z_r_1 - z_b_1) * math.sin(gamma_b_1 * (3.141592653 / 180))) / d)
        q_b_ = q_b * (180 / 3.141592653)
        beta = math.acos(
            math.cos(gamma_r_1 * (3.141592653 / 180)) * math.sin(pusin_r_1 * (3.141592653 / 180)) * math.cos(
                gamma_b_1 * (3.141592653 / 180)) * math.sin(pusin_b_1 * (3.141592653 / 180)) + math.cos(
                gamma_r_1 * (3.141592653 / 180)) * math.cos(pusin_r_1 * (3.141592653 / 180)) * math.cos(
                gamma_b_1 * (3.141592653 / 180)) * math.cos(pusin_b_1 * (3.141592653 / 180)) + math.sin(
                gamma_r_1 * (3.141592653 / 180)) * math.sin(gamma_b_1 * (3.141592653 / 180)))
        beta_ = beta * (180 / 3.141592653)
        delta_h = z_r_1 - z_b_1
        delta_v2 = v_r_1 ** 2 - v_b_1 ** 2
        v2 = v_r_1 ** 2
        h = z_r_1
        taishi = [q_r_, q_b_, d, beta_, delta_h, delta_v2, v2, h]

        return position_r_next, position_b_next, taishi

    def dangeous(self, taishi):
        q_r_, q_b_, d, beta_, delta_h, delta_v2, v2, h = taishi
        weight = 0.8
        R1 = 0
        if d < 20:
            if q_r_ < 30 and q_b_ > 30:
                R1 = 50
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

    def action_b(self, action_b):
        v_b_1_ = action_b[0]
        gamma_b_1 = action_b[1]
        pusin_b_1 = action_b[2]
        action_b = [v_b_1_, gamma_b_1, pusin_b_1]
        return action_b

    def normalize(self, array):
        array[0] = array[0] / 180
        array[1] = array[1] / 180
        array[2] = array[2] / 42.42
        array[3] = array[3] / 180
        array[4] = array[4] / 40
        array[5] = array[5]
        array[6] = array[6]
        array[7] = array[7] / 40
        return array
    # def normal(self,state_array):