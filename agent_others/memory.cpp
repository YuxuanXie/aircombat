#include"memory.hpp"
#include<stdio.h>
#include<stdlib.h>
#include<iostream>
#include<algorithm>
#include<vector>
#include<cstdlib>
#include<cmath>
#include<random>
#include<string.h>
#include"utils.hpp"

using namespace std;

random_device rdm;
mt19937 gen(rdm());
Memory::Memory()
{
	counter = 0;
	size = REPLAY_SIZE;
	batchsize = BATCH_SIZE;
	nActions = L3_NUM;
	nStates = L1_NUM;
	full = false;
	iter_n = nStates * 2 + 3;
	experience_pool = Utils::create2DArray(size, iter_n);
}
Memory::~Memory()
{
	delete[] experience_pool;
}

void Memory::push(float* state, float* nextState, float reward, float action, float done)
{
	if (counter == size)
	{
		full = true;
		counter = 0;
	}
	int index = 0;
	for(int i = 0; i < nStates; i++)
	{
		experience_pool[counter][index] = state[i];
		index++;
	}
	for (int i = 0; i < nStates; i++)
	{
		experience_pool[counter][index] = nextState[i];
		index++;
	}
	experience_pool[counter][index++] = reward;
	experience_pool[counter][index++] = action;
	experience_pool[counter][index] = done;

	counter++;
}

void Memory::generateRandomBatchdata(float* experience_mem)
{
	int index[BATCH_SIZE];
	if (full == false)
	{
		uniform_int_distribution<int> dis(0, counter - 1);
		for (int i = 0; i < batchsize; i++)
		{
			index[i] = dis(gen);
		}
	}
	else
	{
		uniform_int_distribution<int> dis(0, size - 1);
		for (int i = 0; i < batchsize; i++)
		{
			index[i] = dis(gen);
		}
	}
	cout << "batch random index:";
	for(int i = 0; i < batchsize; i++)
	{
		cout << index[i] << " ";
	}
	cout << endl;
	for (int i = 0; i < batchsize; i++)
	{
		int order = index[i];
		for (int j = 0; j < iter_n; j++)
		{
			experience_mem[i*iter_n + j] = experience_pool[order][j];
		}
	}

}

