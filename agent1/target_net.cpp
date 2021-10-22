/*
 * target_net.cpp
 *
 *  Created on: 2020Äê3ÔÂ30ÈÕ
 *      Author: leexp
 */
#include "target_net.hpp"

float T_bias[PE][NF];
float T_bias2[L2_SF][L2_SIMD];
float T_w1[PE][DEPTH][SIMD];
float T_w2[L2_PE][L2_DEPTH][L2_SIMD];
float T_l1_out [PE][NF];
float T_buf_v[SF][SIMD];

float Target_mul(float const &c, float const &d) {
#pragma HLS inline
  float const  res = c*d;
  //std::cout<<"+"<<d<<"x"<<c<<" ";
//#pragma HLS RESOURCE variable=res core=DSP48
  return  res;
}


float Target_mac(int N, float a, float buf_v[SIMD],float buf_m[SIMD]) {
#pragma HLS inline
#pragma HLS PIPELINE II=1
	float  res = a;
	float multresult[SIMD];
#pragma HLS ARRAY_PARTITION variable=multresult complete dim=0

	VM_SIMD:
	for(unsigned  i = 0; i < SIMD; i++) {
#pragma HLS unroll
		multresult[i]= Target_mul(buf_v[i], buf_m[i]);
	}


	float sum5[16];
#pragma HLS ARRAY_PARTITION variable=sum5 complete dim=1
	float sum4[8];
#pragma HLS ARRAY_PARTITION variable=sum4 complete dim=1
	float sum3[4];
#pragma HLS ARRAY_PARTITION variable=sum3 complete dim=1
	float sum2[2];
#pragma HLS ARRAY_PARTITION variable=sum2 complete dim=1
	float sum1;
	//adder_tree_intermediate_t temp;

	ADDER_TREE_LOOP1:
	for(int i = 0; i < 16; i++)
	{
#pragma HLS UNROLL
		sum5[i] = multresult[2 * i] + multresult[2 * i + 1];
	}

	ADDER_TREE_LOOP2:
	for(int i = 0; i < 8; i++)
	{
#pragma HLS UNROLL
		sum4[i] = sum5[2 * i] + sum5[2 * i + 1];
	}

	ADDER_TREE_LOOP3:
	for(int i = 0; i < 4; i++)
	{
#pragma HLS UNROLL
		sum3[i] = sum4[2 * i] + sum4[2 * i + 1];
	}

	ADDER_TREE_LOOP4:
	for(int i = 0; i < 2; i++)
	{
#pragma HLS UNROLL
		sum2[i] = sum3[2 * i] + sum3[2 * i + 1];
	}

	sum1 =  sum2[0] + sum2[1];
	res+=sum1;
	//temp = intermediate_in + bias_in;
	return  res;
}


void Target_vmpu_A(hls::stream<VECTOR>&strm_out)
{
	unsigned  L1_nf   = 0;
	unsigned  L1_sf   = 0;
	unsigned  tile = 0;
	unsigned  TOTAL_FOLD = NF * SF;

	float acc[PE];
	VECTOR T_o;
#pragma HLS ARRAY_PARTITION variable=acc complete dim=0
	// std::cout<<"Target_hwl1_result--------";
	VM_L1:
	for(unsigned fold=0;fold <TOTAL_FOLD;fold++)
	{
#pragma HLS PIPELINE II=5
//#pragma AP dependence variable=acc inter false

		if(L1_sf == 0) {
			L1_init:
			for(unsigned  pe = 0; pe < PE; pe++) {
#pragma HLS UNROLL
				float temp  = T_bias[pe][L1_nf];
				acc[pe]=temp;
			}
		}


		L1_pe:
		for(unsigned  pe = 0; pe < PE; pe++) {
#pragma HLS UNROLL
			acc[pe]=Target_mac(SIMD,acc[pe],T_buf_v[L1_sf],T_w1[pe][fold]);
		}

		L1_sf++;
		if( L1_sf== SF) {
			// produce output and clear accumulators
			L1_sf = 0;
			L1_pestore:
			for (unsigned  pe = 0; pe < PE; pe++) {
#pragma HLS UNROLL
				T_l1_out[pe][L1_nf]=acc[pe]<0?0:acc[pe];
				//out[pe]=T_l1_out[pe][L1_nf];
				T_o.array[pe]=T_l1_out[pe][L1_nf];
			}
			strm_out.write(T_o);
		/*L1_peout:  for (unsigned  pe = 0; pe < PE; pe++) {
		#pragma HLS PIPELINE II=1
		float temp=T_l1_out[pe][L1_nf];
		// d_l1_out[pe][L1_nf]= temp>0?1:0;
		strm_out.write(temp);

		//outElem[pe] = activation.activate(nf, pe, accu[pe]);
		std::cout<<temp <<"  ";
		}*/
			if(++L1_nf == NF) {
			 L1_nf   = 0;
			}
		}
	}
//std::cout<<std::endl;
}
void Target_vmpu_B(hls::stream<VECTOR>&strm_in,float *result,hls::stream<float>&strm_out)
{


	unsigned  L2_nf   = 0;
	unsigned  L2_sf   = 0;
	unsigned  L2_tile = 0;
	unsigned  L2_FOLD = L2_NF * L2_SF;
	float acc[PE];
	float multresult[L2_PE][L2_SIMD];
	float addresult1[2];
	float addresult[L2_SIMD];
	float T_l2_out[L2_SF][L2_SIMD];
	VECTOR T_i;
#pragma HLS ARRAY_PARTITION variable=acc complete dim=0
#pragma HLS ARRAY_PARTITION variable=multresult   complete dim=0
#pragma HLS ARRAY_PARTITION variable=addresult    complete dim=0
#pragma HLS ARRAY_PARTITION variable=addresult1  complete dim=0
#pragma HLS ARRAY_PARTITION variable=T_l2_out    complete dim=0
//#pragma HLS dependence variable=l2_out inter false
	// std::cout<<"L2 hardware compute"<<std::endl;

	VM_L2:for(unsigned fold=0;fold <L2_FOLD;fold++)
	{
#pragma HLS PIPELINE II=5
//#pragma HLS PIPELINE II=7
// #pragma AP dependence variable=acc inter false
		if(L2_sf==0)
		{
			T_i=strm_in.read();
			for(unsigned pe=0 ;pe<L2_PE;pe++)
			{//acc[pe]=strm_in.read();
				acc[pe]=T_i.array[pe];
			}
		}

		if(fold == 0) {
			L2_init:
			for(unsigned  sf = 0; sf < L2_SF; sf++){
//#pragma HLS PIPELINE II=1
				for  (unsigned  simd = 0; simd < L2_SIMD; simd++){
#pragma HLS UNROLL
					T_l2_out[sf][simd] = T_bias2[sf][simd];
					// std::cout << l2_out[sf][simd]<<" ";
				}
			}
		}
		// std::cout<<std::endl;
		L2_pe:
		for(unsigned  pe = 0; pe < L2_PE; pe++) {
// #pragma HLS UNROLL
			L2_simd:
			for(unsigned simd=0 ;simd<L2_SIMD;simd++)
			{
//  #pragma HLS UNROLL
				multresult[pe][simd]=T_w2[pe][fold][simd]*acc[pe];
			}
		}
		// std::cout.setf(ios::fixed,ios::floatfield);
		L2_add:
		for(unsigned simd=0 ;simd<L2_SIMD;simd++)
		{
#pragma HLS UNROLL
			for(unsigned pe=0; pe<2;pe++)
			{
#pragma HLS UNROLL
				addresult1[pe]=multresult[2*pe][simd]+multresult[2*pe+1][simd];

			}
			addresult[simd]=addresult1[0]+addresult1[1];
			T_l2_out[L2_sf][simd]+=addresult[simd];
		}

			/* L2_resullt:for(unsigned simd=0 ;simd<L2_SIMD;simd++)
			{
				#pragma HLS UNROLL
			T_l2_out[L2_sf][simd]+=addresult[simd];
			}*/

		if(++L2_sf == SF) {
			// produce output and clear accumulators

			/*L2_peout:  for (unsigned  pe = 0; pe < L2_PE; pe++) {
			#pragma HLS UNROLL
			// acc[pe] += bias[pe][nf];
			l2_out[pe][nf]=acc[pe]<0?0:acc[pe];
			//outElem[pe] = activation.activate(nf, pe, accu[pe]);
			//std::cout << "out " << outElem[pe] << std::endl;
			}*/
			L2_sf = 0;
			if(++L2_nf == L2_NF) {
				L2_nf   = 0;
			}
		}
	}

	float max=T_l2_out[0][0];
	//std::cout<<"Target_hwl2_result------- ";
	result_out:
	for(unsigned sf=0;sf<L2_SF;sf++)
	{
		for(unsigned simd=0;simd<L2_SIMD;simd++){
//#pragma HLS PIPELINE II=1

			float value =T_l2_out[sf][simd];
			// result[sf*L2_SIMD+simd] =value;
			max=max>value?max:value;
			//strm_out.write(value);
			//  std::cout<<value<<" ";
		}
		//std::cout<<std::endl;
	}

	strm_out.write(max);
	//std::cout<<std::endl;
}


void Target_vmpu(unsigned batch,float *result,hls::stream<float>&strm_out){
#pragma HLS RESOURCE variable=T_w1 core=RAM_T2P_BRAM
#pragma HLS RESOURCE variable=T_w2 core=RAM_T2P_BRAM
#pragma HLS RESOURCE variable=T_bias core=RAM_T2P_BRAM
#pragma HLS RESOURCE variable=T_bias2 core=RAM_T2P_BRAM
//#pragma HLS RESOURCE variable=T_l1_out core=RAM_T2P_BRAM


#pragma HLS ARRAY_PARTITION variable=T_buf_v complete dim=0

#pragma HLS ARRAY_PARTITION variable=T_w1 block factor=PE        dim=1
#pragma HLS ARRAY_PARTITION variable=T_w1 block factor=SIMD      dim=3
#pragma HLS ARRAY_PARTITION variable=T_w2 block factor=L2_PE     dim=1
#pragma HLS ARRAY_PARTITION variable=T_w2 block factor=L2_SIMD   dim=3

#pragma HLS ARRAY_PARTITION variable=T_l1_out  block factor=PE   dim=1

#pragma HLS ARRAY_PARTITION variable=T_bias    block factor=PE        dim=1
#pragma HLS ARRAY_PARTITION variable=T_bias2   block factor=L2_SIMD   dim=2

	static hls::stream<VECTOR>strm_T("stream_AB_TARGET");
#pragma HLS STREAM variable=strm_T depth=NF*SF
#pragma HLS dataflow

	Target_vmpu_A(strm_T);

	Target_vmpu_B(strm_T,result,strm_out);

}




