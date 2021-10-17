#ifndef  EVAL_NET_HPP
#define  EVAL_NET_HPP
#include "config.hpp"
#include "hls_stream.h"

extern float buf_v[SF][SIMD];
extern float buf_m[PE][DEPTH][SIMD];
extern float bias [PE][NF];
extern float l1_out [PE][NF];
extern float d_l1_out [PE][NF];
extern float db1[PE][NF];
extern float dw1[PE][DEPTH][SIMD];

extern float buf_m2[L2_PE][L2_DEPTH][L2_SIMD];
extern float l2_bias[L2_SF][L2_SIMD];
extern float dw2[L2_PE][L2_DEPTH][L2_SIMD];
extern float db2[L2_SF][L2_SIMD];

float mul(float const &c, float const &d);
float mac(int N, float a, float buf_v[SIMD],float buf_m[SIMD]);
float back_mac(const int  N, float a, float buf_v[L2_SIMD],float buf_m[L2_SIMD]);

void vmpu_A(hls::stream<VECTOR>&strm_out);
void vmpu_B(hls::stream<VECTOR>&strm_in , float *result,hls::stream<float>&strm_out);
void vmpu(unsigned batch,float *result,hls::stream<float>&strm_out);

void back_vmpu(unsigned batch,hls::stream<float>&strm_in,float *result);
void back_vmpu_B(float delta_3[L2_SF][L2_SIMD],hls::stream<VECTOR>&strm_out,float *result);
void calcu_dw3(float delta_3[L2_SF][L2_SIMD]);
void back_vmpu_A(hls::stream<VECTOR>&strm_in,float *result);

#endif
