#ifndef  TARGET_NET_HPP
#define  TARGET_NET_HPP
#include "config.hpp"

#include "hls_stream.h"
extern float T_bias[PE][NF];
extern float T_bias2[L2_SF][L2_SIMD];
extern float T_w1[PE][DEPTH][SIMD];
extern float T_w2[L2_PE][L2_DEPTH][L2_SIMD];
extern float T_l1_out [PE][NF];
extern float T_buf_v[SF][SIMD];

void Target_vmpu(unsigned batch,float *result,hls::stream<float>&strm_out);
void Target_vmpu_A(hls::stream<VECTOR>&strm_out);
void Target_vmpu_B(hls::stream<VECTOR>&strm_in,float *result,hls::stream<float>&strm_out);
float Target_mul(float const &c, float const &d);
float Target_mac(int N, float a, float buf_v[SIMD],float buf_m[SIMD]);

#endif
