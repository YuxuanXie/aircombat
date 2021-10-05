import numpy as np
import tensorflow as tf


# Deep Q Network off-policy
class DeepQNetwork:
    def __init__(
            self,
            n_actions,
            n_features,
            learning_rate=0.0001,
            reward_decay=0.9,
            e_greedy=0.9,
            replace_target_iter=300,
            memory_size=int(1e5),
            batch_size=128,
            e_greedy_decrement=1e-4,
            output_graph=False,
    ):
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = learning_rate
        self.gamma = reward_decay
        self.replace_target_iter = replace_target_iter
        self.memory_size = memory_size
        self.batch_size = batch_size

        self.epsilon_decrement = e_greedy_decrement
        self.epsilon = e_greedy
        self.epsilon_min = 1e-2

        # total learning step
        self.learn_step_counter = 0

        # initialize zero memory [s, a, r, s_]
        self.memory = np.zeros((int(self.memory_size), n_features * 2 + 2))

        # consist of [target_net, evaluate_net]
        self._build_net()
        t_params = tf.get_collection('target_net_params')
        e_params = tf.get_collection('eval_net_params')
        self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)]

        self.sess = tf.Session(config=tf.ConfigProto(device_count={"gpu":4}, inter_op_parallelism_threads=1,
                                intra_op_parallelism_threads=1, log_device_placement=True))

        if output_graph:
            # $ tensorboard --logdir=logs
            # tf.train.SummaryWriter soon be deprecated, use following
            tf.summary.FileWriter("logs/", self.sess.graph)

        self.sess.run(tf.global_variables_initializer())
        self.cost_his = []

    def _build_net(self):
        # ------------------ build evaluate_net ------------------
        self.s = tf.placeholder(tf.float32, [None, self.n_features], name='s')  # input
        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='Q_target')  # for calculating loss
        with tf.variable_scope('eval_net'):
            # c_names(collections_names) are the collections to store variables
            c_names, n_l1, w_initializer, b_initializer = \
                ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES], 64, \
                tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)  # config of layers

            # first layer. collections is used later when assign to target net
            with tf.variable_scope('l1'):
                w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                l1 = tf.nn.relu(tf.matmul(self.s, w1) + b1)

            # second layer. collections is used later when assign to target net
            with tf.variable_scope('l2'):
                w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_eval = tf.matmul(l1, w2) + b2

        with tf.variable_scope('loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))

        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)

        # ------------------ build target_net ------------------
        self.s_ = tf.placeholder(tf.float32, [None, self.n_features], name='s_')  # input
        with tf.variable_scope('target_net'):
            # c_names(collections_names) are the collections to store variables
            c_names = ['target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]

            # first layer. collections is used later when assign to target net
            with tf.variable_scope('l1'):
                w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                l1 = tf.nn.relu(tf.matmul(self.s_, w1) + b1)

            # second layer. collections is used later when assign to target net
            with tf.variable_scope('l2'):
                w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_next = tf.matmul(l1, w2) + b2


    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0

        transition = np.hstack((s, [a, r], s_))

        # replace the old memory with new memory
        index = self.memory_counter % int(self.memory_size)
        self.memory[index, :] = transition

        self.memory_counter += 1

    def choose_action(self, observation):
        # to have batch dimension when feed into tf placeholder
        observation = observation[np.newaxis, :]
        if np.random.uniform() < self.epsilon:
            action = np.random.randint(0, self.n_actions)
        else:
            # forward feed the observation and get q value for every actions
            actions_value = self.sess.run(self.q_eval, feed_dict={self.s: observation})
            #print(actions_value)
            action = np.argmax(actions_value)
            #print("***",action,"***")
        return action

    def learn(self):
        # check to replace target parameters
        if self.learn_step_counter % self.replace_target_iter == 0:
            self.sess.run(self.replace_target_op)
            # print('\ntarget_params_replaced\n')

        # sample batch memory from all memory
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]

        q_next_target, q = self.sess.run(
            [self.q_next, self.q_eval],
            feed_dict={
                self.s_: batch_memory[:, -self.n_features:],  # fixed params
                self.s: batch_memory[:, :self.n_features],  # newest params
            })
        
        # change q_target w.r.t q_eval's action
        q_next = self.sess.run(self.q_eval, feed_dict={self.s : batch_memory[:, -self.n_features:]})

        q_next_argmax_a = np.argmax(q_next_target, axis=-1)

        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = batch_memory[:, self.n_features].astype(int)
        reward = batch_memory[:, self.n_features + 1]
        q[batch_index, eval_act_index] = reward + self.gamma * q_next[batch_index, q_next_argmax_a]  # np.max(q_next, axis=1)

        """
        For example in this batch I have 2 samples and 3 actions:
        q_eval =
        [[1, 2, 3],
         [4, 5, 6]]
        q_target = q_eval =
        [[1, 2, 3],
         [4, 5, 6]]
        Then change q_target with the real q_target value w.r.t the q_eval's action.
        For example in:
            sample 0, I took action 0, and the max q_target value is -1;
            sample 1, I took action 2, and the max q_target value is -2:
        q_target =
        [[-1, 2, 3],
         [4, 5, -2]]
        So the (q_target - q_eval) becomes:
        [[(-1)-(1), 0, 0],
         [0, 0, (-2)-(6)]]
        We then backpropagate this error w.r.t the corresponding action to network,
        leave other action as error=0 cause we didn't choose it.
        """

        # train eval network
        _, self.cost = self.sess.run([self._train_op, self.loss],
                                     feed_dict={self.s: batch_memory[:, :self.n_features],
                                                self.q_target: q})
        self.cost_his.append(self.cost)

        # increasing epsilon
        self.epsilon = max(self.epsilon - self.epsilon_decrement, self.epsilon_min)
        self.learn_step_counter += 1
        return self.cost

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()
    def storew_b_test(self,num):
        saver = tf.train.Saver()
        saver.save(self.sess, global_step=num)
    def storevariable(self, i_episode):
        saver = tf.train.Saver()
        save_path =saver.save(self.sess, f"my_net_new/save_net_{i_episode}.ckpt")
        print(save_path)
    def storevariable_2(self):
        saver = tf.train.Saver()
        save_path =saver.save(self.sess,"my_net_new_2/save_net.ckpt")
        print(save_path)
    def storevariable_3(self):
        saver = tf.train.Saver()
        save_path =saver.save(self.sess,"my_net_new_3/save_net.ckpt")
        print(save_path)
    def storevariable_4(self):
        saver = tf.train.Saver()
        save_path =saver.save(self.sess,"my_net_new_4/save_net.ckpt")
        print(save_path)
    def storevariable_6(self):
        saver = tf.train.Saver()
        save_path =saver.save(self.sess,"my_net_6/save_net.ckpt")
        print(save_path)
    def addw_b_test(self):
        #g = tf.get_default_graph()
        #print(g.get_operations())
        #a=self.sess.run('eval_net/l1/b1:0')
        #saver = tf.train.import_meta_graph('./my_net_new/save_net.ckpt.meta')
        saver = tf.train.Saver()
        saver.restore(self.sess,'./my_net_new/save_net.ckpt')
        #a=self.sess.run('eval_net/l1/b1:0')
        #print(a)
        #print(a)
        #    print ("No Model")
    def addw_b_test_2(self):
        #g = tf.get_default_graph()
        #print(g.get_operations())
        #a = self.sess.run('eval_net/l1/b1:0')
        saver = tf.train.Saver()
        #ckpt = tf.train.get_checkpoint_state('./222/')
        #if ckpt and ckpt.model_checkpoint_path:
            #print('**************************************')
            #print(ckpt.model_checkpoint_path)
            #print ("Model restord")
        saver.restore(self.sess,'./my_net_new_2/save_net.ckpt')
        #a = self.sess.run('eval_net/l1/b1:0')
        #print(a)
        #print(a)
        #else:
        #    print ("No Model")
    def addw_b_test_3(self):
        saver = tf.train.Saver()
        saver.restore(self.sess,'./my_net_new_3/save_net.ckpt')
    def addw_b_test_4(self):
        saver = tf.train.Saver()
        saver.restore(self.sess,'./my_net_new_4/save_net.ckpt')
    def addw_b_test_6(self):
        saver = tf.train.Saver()
        saver.restore(self.sess,'./my_net_6/save_net.ckpt')
