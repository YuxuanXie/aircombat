#ifndef  CONFIG_HPP
#define  CONFIG_HPP
#include "hls_stream.h"
#include <iostream>

#define LAYER_SIZE    3
const int  L1_NUM = 32;
const int  L2_NUM = 64;
const int  L3_NUM = 10;

const int REPLAY_SIZE = 5000;
const int BATCH_SIZE = 32;
const int STEP =300;
const int EPISODE =2000;
const int TEST =5;
const int REPLACE_FREQ =10;
const int  INITIAL_EPSILON =0;
const int FINAL_EPSILON =0;

const int SIMD = 32;
const int PE = 2;
const int DEPTH=32;
const int SF = 1;
const int NF = 32;

const int L2_SIMD = 10;
const int L2_PE = 2;
const int L2_DEPTH  = 32;
const int L2_SF = 1;
const int L2_NF = 32;

const int EX_DEPTH = (L1_NUM*2+3)*BATCH_SIZE;
const int VE_DEPTH = L1_NUM*BATCH_SIZE ;
const int MA_DEPTH = L1_NUM*L2_NUM+L2_NUM*L3_NUM ;
const int BI_DEPTH = L2_NUM+L3_NUM ;
const int RES_DEPTH = L1_NUM*L2_NUM+L2_NUM*L3_NUM+L2_NUM+L3_NUM+L3_NUM+BATCH_SIZE ;

typedef struct
{
	 float array [PE];

} VECTOR;







#endif
