#ifndef  MEMORY_HPP_
#define  MEMORY_HPP_
#include<vector>
#include"config.hpp"

using namespace std;

class Memory
{
	public:
		Memory();
		~Memory();
		void generateRandomBatchdata(float * expericen_mem);
		void sampleStates(float ** result, int **infices);

		void push(float* state, float* nextState, float reward, float action, float done);
		float **experience_pool;
		int counter;
		int size;
		int batchsize;
		int iter_n;
		int nActions;
		int nStates;
		bool full;
};



#endif
