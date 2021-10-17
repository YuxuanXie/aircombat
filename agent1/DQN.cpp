#include "DQN.hpp"
#include<stdio.h>
#include<stdlib.h>
#include<iostream>
#include<algorithm>
#include<vector>
#include<ctime>
#include<cstdlib>
#include<cmath>
#include<string>
#include<random>

using namespace std;
random_device rd;
mt19937 mt(rd());

DQN::DQN()
{
	layer_neuron[0] = L1_NUM;
	layer_neuron[1] = L2_NUM;
	layer_neuron[2] = L3_NUM;
	layer_size = LAYER_SIZE;
	action_n = L3_NUM;
	state_n = L1_NUM;
	memory_size = 5000;
	batch_size = BATCH_SIZE;
	replace_target_iter = 2;
	learning_rate = 0.00001;
	reward_decay = 0.9;
	e_greedy = INITIAL_EPSILON;
	e_greedy_increment = 0;
}

int DQN::calculateMaxOutput(float *eval_output)
{
	float maxAction = eval_output[0];
	float a0 = eval_output[0];
	float a1 = eval_output[1];
	float a2 = eval_output[2];
	float a3 = eval_output[3];
	float a4 = eval_output[4];
	float a5 = eval_output[5];
	float a6 = eval_output[6];
	float a7 = eval_output[7];
	float a8 = eval_output[8];
	float a9 = eval_output[9];

	int action = 0;
	for(int i = 0; i < action_n; i++)
	{
		if (eval_output[i] > maxAction)
		{
			maxAction = eval_output[i];
			action = i;
		}
	}
	return action;
}
int DQN::choose_action_egreedy()
{
	int action;
	uniform_real_distribution<float>distance(0.0, 1.0);
	uniform_int_distribution<int> disint(0, L3_NUM);

	float randF = distance(mt);

	if (randF < e_greedy)
	{
		e_greedy -= (INITIAL_EPSILON - FINAL_EPSILON) / 10000;
		action = disint(mt);
		//cout << "e_greedy->" << e_greedy << endl;
	}
	else
	{
		e_greedy -= (INITIAL_EPSILON - FINAL_EPSILON) / 10000;
		//cout << "e_greedy->" << e_greedy << endl;
		action = -1;
	}
	//cout << "choose action e_greedy" << randF << "action->" << action << endl;

	return action;
}

int DQN::choose_action_random()
{
	int action;
	float randF = (rand() % 100 + 1) / 100.f;
	cout << randF << endl;
	action = rand() % (action_n);
	return action;
}
