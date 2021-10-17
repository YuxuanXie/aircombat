#ifndef DQN_HPP_
#define DQN_HPP_

#define EPSILON 0.009
#include"config.hpp"

using namespace std;

class DQN {
public:
	int layer_neuron[LAYER_SIZE];
	int layer_size;
	int action_n;
	int state_n;
	int memory_size;
	int replace_target_iter;
	unsigned batch_size;
	float learning_rate;
	float reward_decay;
	float e_greedy;
	float e_greedy_increment;

	DQN();
	~DQN();
	int calculateMaxOutput(float *eval_output);
	int choose_action_random();
	int choose_action_egreedy();
};


struct DQN_info {
	float learning_rate;
	float reward_decay;
	int  iter_n;
	unsigned batch_size;
	bool replace;

	DQN_info(float lr, float gamma, int iter_n, unsigned bs,bool rp):learning_rate(lr),reward_decay(gamma),iter_n(iter_n),batch_size(bs),replace(rp)
	{}
	DQN_info():learning_rate(0),reward_decay(0),iter_n(0),batch_size(0),replace(0)
	{}
};

#endif

