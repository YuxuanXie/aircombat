//#include "ap_axi_sdata.h"
//#include "ap_int.h"
//#include "hls_stream.h"
#include "math.h"
#include "config.hpp"
#include "target_net.hpp"
#include "eval_net.hpp"
#include "module_untils.hpp"
#include "DQN.hpp"
using namespace std;


//float l2_out[L2_PE][L2_SIMD];

void MUAV_fpgatop(float*ex_memory,float *vector_in ,float *matrix_in ,float *bias_in ,float *result,DQN_info info,bool doInit,bool mode,bool check){

#pragma HLS INTERFACE m_axi port = ex_memory offset=slave bundle=gmem0 depth=EX_DEPTH  //(state+state'+action+reward)*batchsize
#pragma HLS INTERFACE m_axi port = vector_in offset=slave bundle=gmem0 depth=VE_DEPTH        //state*batchsize
#pragma HLS INTERFACE m_axi port = matrix_in offset = slave bundle = gmem0 depth=MA_DEPTH
#pragma HLS INTERFACE m_axi port = bias_in offset = slave bundle = gmem0 depth=BI_DEPTH
#pragma HLS INTERFACE m_axi port = result    offset = slave bundle = gmem1 depth=RES_DEPTH
#pragma HLS INTERFACE s_axilite port=info bundle=control
#pragma HLS INTERFACE s_axilite port=doInit bundle=control
#pragma HLS INTERFACE s_axilite port=mode bundle=control
#pragma HLS INTERFACE s_axilite port=check bundle=control
#pragma HLS INTERFACE s_axilite port = return bundle = control

#pragma HLS RESOURCE variable=buf_m core=RAM_T2P_BRAM
#pragma HLS RESOURCE variable=buf_m2 core=RAM_T2P_BRAM

#pragma HLS RESOURCE variable=l2_bias  core=RAM_T2P_BRAM
#pragma HLS RESOURCE variable=bias     core=RAM_T2P_BRAM
//#pragma HLS RESOURCE variable=l1_out core=RAM_T2P_BRAM
#pragma HLS RESOURCE variable=dw2      core=RAM_T2P_BRAM
#pragma HLS RESOURCE variable=dw1      core=RAM_T2P_BRAM

#pragma HLS ARRAY_PARTITION variable=l1_out block factor=PE dim=1

#pragma HLS ARRAY_PARTITION variable=buf_v    complete            dim=0

#pragma HLS ARRAY_PARTITION variable=db1             factor=PE     dim=1
#pragma HLS ARRAY_PARTITION variable=buf_m    block  factor=PE     dim=1
#pragma HLS ARRAY_PARTITION variable=buf_m    block  factor=SIMD   dim=3
#pragma HLS ARRAY_PARTITION variable=dw1      block  factor=PE     dim=1
#pragma HLS ARRAY_PARTITION variable=dw1      block  factor=SIMD   dim=3
#pragma HLS ARRAY_PARTITION variable=d_l1_out block  factor=PE     dim=1
#pragma HLS ARRAY_PARTITION variable=bias     block  factor=PE     dim=1


#pragma HLS ARRAY_PARTITION variable=buf_m2  block factor=L2_PE      dim=1
#pragma HLS ARRAY_PARTITION variable=buf_m2  block factor=L2_SIMD    dim=3
#pragma HLS ARRAY_PARTITION variable=dw2     block factor=L2_PE      dim=1
#pragma HLS ARRAY_PARTITION variable=dw2     block factor=L2_SIMD    dim=3
#pragma HLS ARRAY_PARTITION variable=l2_bias       factor=L2_SIMD    dim=2

	if(doInit)
	{

		MemInit(matrix_in,bias_in);
	}
	else if(doInit == 0)
	{
		learn_rate=info.learning_rate;
		Batch_size=info.batch_size;
		iter_n=info.iter_n;
		replacement=info.replace;
		mode_=mode;
		check_=check;
		compute(ex_memory,Batch_size,iter_n,result,vector_in,mode_);
		update_weight(mode_);
		data_check(check_,result);
	}
	/*
	else if(doInit == 2)
	{
		replace_weight();
	}*/

}






