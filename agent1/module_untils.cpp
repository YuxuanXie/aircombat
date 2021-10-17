#include "module_untils.hpp"
#include <iostream>
using namespace std;
float learn_rate = 0;
unsigned Batch_size = 0;
int iter_n=0;
bool mode_=0;
bool replacement=0;
bool check_=0;

/*
 * mode == 1 ,only inference
 * mode == 0 ,inference and train
 */
void calcu_error(float*ex_memory,unsigned batch,hls::stream<float>&eval_Q,hls::stream<float>&Target_Q,hls::stream<float>&strm_out,float *result,int iter_n,bool mode)

{
	float Eval[L3_NUM];
	float Target[L3_NUM];
	//std::cout<<std::endl<<"hardware error-----"<<batch<<" ";

       // error= (value==0)? 0 : error;  //delta3 = (a-y)x d_relu(z),y=relu(z)
     //   std::cout<<value<<"-"<<lable[batch*32+i]<<"=";



        if(mode)
        {
        	//cout<<endl<<"hw_eval_inference "<<endl;
        	 for(unsigned i=0;i<L3_NUM;i++)
        	    {
        	   #pragma HLS PIPELINE II=1
        		 float value = eval_Q.read();
        		 result[i]=value;
                // cout<<value<<" ";
        	    }
        	// cout<<endl;

        }
        else
        {
        	 float target_max= Target_Q.read();

        	 float target_Q = ex_memory[batch*iter_n+L1_NUM*2]+0.9*target_max;

        	 result[L3_NUM+batch] = target_Q;
        	 for(unsigned i=0;i<L3_NUM;i++)
				{
        		 #pragma HLS PIPELINE II=1
        		 float value = eval_Q.read();
        		 Eval[i]=value;
        		 Target[i]=value;
				}
        	 int action = ex_memory[batch*iter_n+L1_NUM*2+1];
        	 //cout<<"action"<<action<<endl;
        	 Target[action]=target_Q;
        	 for(unsigned i=0;i<L3_NUM;i++)
				{
                #pragma HLS PIPELINE II=1
	             float error = Eval[i] - Target[i];
                 strm_out.write(error);
				}


             //std::cout<<error<<" ";
    }
  // std::cout<< std::endl;
}

void MemInit(float *matrix_in,float *bias_in)
{

	   //row major in memory
	   load_matrix1:for(int i=0 ;i<PE ;i++)
			for (int j = 0; j < DEPTH; j++)
				for(int k = 0;k < SIMD; k++){
			   #pragma HLS PIPELINE II=1

				float weight1 = matrix_in[i*DEPTH*SIMD+j*SIMD+k];
				buf_m[i][j][k]=weight1;
				T_w1[i][j][k]=weight1;

			}

	   //col major in memory
	   load_matrix2:for(int i=0 ;i<L2_PE ;i++)
			for (int j = 0; j < L2_DEPTH; j++)
				for(int k = 0;k < L2_SIMD; k++){
			   #pragma HLS PIPELINE II=1

				float weight2 = matrix_in[L1_NUM*L2_NUM+i*L2_DEPTH*L2_SIMD+j*L2_SIMD+k];
			    buf_m2[i][j][k] = weight2;
				T_w2[i][j][k]=weight2;
			}

		load_bias1:for(int i=0 ;i<PE ;i++)
			for (int j = 0; j < NF; j++){
			   #pragma HLS PIPELINE II=1
				float bias1 = bias_in[i*NF+j];
			    bias[i][j]=bias1;
			    T_bias[i][j]=bias1;
			}

		load_bias2:for(unsigned  sf = 0; sf < L2_SF; sf++)
	       for (unsigned  simd = 0; simd < L2_SIMD; simd++){
	          #pragma HLS PIPELINE II=1

				float bias2 = bias_in[L2_NUM+sf*L2_SIMD+simd];
				l2_bias[sf][simd] = bias2;
			    T_bias2[sf][simd]= bias2;
		      }
}


void data_check(bool check,float *result)
{
	if(check)
	{
	   for(unsigned pe=0;pe<PE;pe++){
		   for(unsigned depth=0;depth<DEPTH;depth++){
		      for(unsigned simd=0;simd<SIMD;simd++)
			   {
				#pragma HLS PIPELINE II=1
				   result[L3_NUM+Batch_size+pe*DEPTH*SIMD+depth*SIMD+simd]=buf_m[pe][depth][simd];
				 //  std::cout<<result[32*32+pe*DEPTH*SIMD+depth*SIMD+simd]<<"  ";
			   }
		   //std::cout<<std::endl;
		   }}
	   for(unsigned pe=0;pe<L2_PE;pe++)
	  		    for(unsigned depth=0;depth<L2_DEPTH;depth++)
	  		       for(unsigned simd=0;simd<L2_SIMD;simd++)
	  			    {
	  				  #pragma HLS PIPELINE II=1
	  				   result[L3_NUM+Batch_size+L1_NUM*L2_NUM+pe*L2_DEPTH*L2_SIMD+depth*L2_SIMD+simd]=buf_m2[pe][depth][simd];
	  			    }
	   for(unsigned i=0;i<PE;i++)
	  		 for(unsigned j=0;j<NF;j++)
	  		 {
	  			 #pragma HLS PIPELINE II=1
	               result[L3_NUM+Batch_size+L1_NUM*L2_NUM+L2_NUM*L3_NUM+i*NF+j]=bias[i][j];
	              // std::cout<<bias[i][j]<<" ";
	  		 }

	   for(unsigned i=0;i<L2_SF;i++)
	  		 for(unsigned j=0;j<L2_SIMD;j++)
	  		 {
                #pragma HLS PIPELINE II=1
	               result[L3_NUM+Batch_size+L1_NUM*L2_NUM+L2_NUM*L3_NUM+L2_NUM+i*L2_SIMD+j]=l2_bias[i][j];
	  		 }
	}

}

void compute(float*ex_memory,unsigned Batch_size,int iter_n,float *result,float *vector_in,bool mode)
{
	static hls::stream<float>Eval_Q("stream_Eval_Q");
	    #pragma HLS STREAM variable=Eval_Q depth=32

		static hls::stream<float>strm_delta3("stream_delta3");
	    #pragma HLS STREAM variable=strm_delta3 depth=32

		static hls::stream<float>Target_Q("stream_Target_Q");
        #pragma HLS STREAM variable=Target_Q depth=32

   for (unsigned batch = 0; batch < Batch_size; batch++) //#Batch_size=2
   {
   #pragma HLS loop_tripcount min=1 max=2

//#pragma HLS PIPELINE


		//std::cout<<"backfowrd hardware compute"<<std::endl;
		if(mode==0)
		{
          load_vector:for (unsigned i = 0; i < SF; i++)
				for(unsigned j = 0; j < SIMD;j++){
			 //  #pragma HLS PIPELINE II=1

				buf_v[i][j]  = ex_memory[batch*iter_n+i*SIMD+j];
				T_buf_v[i][j] = ex_memory[batch*iter_n+L1_NUM+i*SIMD+j];
			}
           // cout<<"Target_vmpu"<<endl<<endl;
			Target_vmpu(batch,result,Target_Q);
			//cout<<"eval_vmpu"<<endl<<endl;
			vmpu(batch,result,Eval_Q);
			calcu_error(ex_memory,batch,Eval_Q,Target_Q,strm_delta3,result,iter_n,mode);
			back_vmpu(batch,strm_delta3,result);
		}
		else
		{
		  load_state:for (unsigned i = 0; i < SF; i++)
				for(unsigned j = 0; j < SIMD;j++){
			 //  #pragma HLS PIPELINE II=1

				buf_v[i][j]  = vector_in[i*SIMD+j];
			}
			vmpu(batch,result,Eval_Q);
	    	calcu_error(ex_memory,batch,Eval_Q,Target_Q,strm_delta3,result,iter_n,mode);
		}
   }

}
void replace_weight()
{
	replace_w1();
	replace_w2();
}

void replace_w1()
{
	for(unsigned depth=0;depth<DEPTH;depth++){
	      #pragma HLS PIPELINE II=1
			 for(unsigned pe=0;pe<PE;pe++){
				 #pragma HLS UNROLL
			     for(unsigned simd=0;simd<SIMD;simd++)
				   {
	             #pragma HLS UNROLL
			    	    T_w1[pe][depth][simd]=buf_m[pe][depth][simd];
					}
			   }}
		 for(unsigned i=0;i<PE;i++)
			 for(unsigned j=0;j<NF;j++)
			 {
	#pragma HLS PIPELINE II=1
				 T_bias[i][j]= bias[i][j];
			 }
}

void replace_w2()
{
	for(unsigned depth=0;depth<L2_DEPTH;depth++){
	     #pragma HLS PIPELINE II=1
			 for(unsigned pe=0;pe<L2_PE;pe++){
	        #pragma HLS UNROLL
			   for(unsigned simd=0;simd<L2_SIMD;simd++)
				   {
	                #pragma HLS UNROLL
				    T_w2[pe][depth][simd]=buf_m2[pe][depth][simd];
				   }
			 }
		 }

		 for(unsigned i=0;i<L2_SF;i++)
			 for(unsigned j=0;j<L2_SIMD;j++)
			 {
	          #pragma HLS PIPELINE II=1
				 T_bias2[i][j]= l2_bias[i][j];
			 }

}


void update_weight(bool mode)
{
	if(mode == 0)
	{
		 update_W1();
		 update_W2();
	}
}

void update_W1()
{
	//std::cout<<std::endl;
	 for(unsigned depth=0;depth<DEPTH;depth++){
    //  #pragma HLS PIPELINE II=1
		 for(unsigned pe=0;pe<PE;pe++){
		//	 #pragma HLS UNROLL
		     for(unsigned simd=0;simd<SIMD;simd++)
			   {
          //   #pragma HLS UNROL
				#pragma HLS PIPELINE II=1
				   buf_m[pe][depth][simd]=buf_m[pe][depth][simd]-learn_rate*dw1[pe][depth][simd];
				   if(depth==0&&pe==0&&simd==0){
		//			 std:;cout<<"hw_update"<<endl;
				     std::cout<<buf_m[pe][depth][simd]<<"-"<<learn_rate<<"*"<<dw1[pe][depth][simd]<<"  "<<endl;
				   }

			   }
		   //std::cout<<std::endl;
		   }}
	 for(unsigned i=0;i<PE;i++)
		 for(unsigned j=0;j<NF;j++)
		 {
#pragma HLS PIPELINE II=1
             bias[i][j]= bias[i][j]-learn_rate*db1[i][j];
		 }
}

void update_W2()
{
	 for(unsigned depth=0;depth<L2_DEPTH;depth++){
 //    #pragma HLS PIPELINE II=1
		 for(unsigned pe=0;pe<L2_PE;pe++){
   //     #pragma HLS UNROLL
		   for(unsigned simd=0;simd<L2_SIMD;simd++)
			   {
     //     #pragma HLS UNROLL
				#pragma HLS PIPELINE II=1
				   buf_m2[pe][depth][simd]=buf_m2[pe][depth][simd]-learn_rate*dw2[pe][depth][simd];
			   }
		 }
	 }

//	 cout<<"-------------eval_db2_compute-------------"<<endl;
	 for(unsigned i=0;i<L2_SF;i++)
		 for(unsigned j=0;j<L2_SIMD;j++)
		 {
//#pragma HLS PIPELINE II=6
			 l2_bias[i][j]= l2_bias[i][j]-learn_rate*db2[i][j];
			 //cout<<"print-----db2---------------"<<endl;
//			 cout<<db2[i][j]<<" ";
		 }

}
