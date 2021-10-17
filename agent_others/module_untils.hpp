
#ifndef  MODULE_UNTILS_HPP
#define  MODULE_UNTILS_HPP
#include "config.hpp"
#include "eval_net.hpp"
#include "target_net.hpp"
#include "hls_stream.h"

extern float learn_rate;
extern unsigned Batch_size;
extern int iter_n;
extern bool mode_;
extern bool replacement;
extern bool check_;

void MemInit(float *matrix_in,float *bias_in);
void compute(float*ex_memory,unsigned Batch_size,int iter_n,float *result,float *vector_in,bool mode);
void calcu_error(float*ex_memory,unsigned batch,hls::stream<float>&eval_Q,hls::stream<float>&Target_Q,hls::stream<float>&strm_out,float *result,int iter_n,bool mode);
void data_check(bool check,float *result);

void replace_weight(bool rp);
void replace_w1();
void replace_w2();


void update_weight();
void update_W1();
void update_W2();


#endif

