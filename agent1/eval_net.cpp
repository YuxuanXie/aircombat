
/*
 * target_net.cpp
 *
 *  Created on: 2020Äê3ÔÂ30ÈÕ
 *      Author: leexp
 */

#include "eval_net.hpp"
#include <iostream>
using namespace std;
float buf_v[SF][SIMD];
float buf_m[PE][DEPTH][SIMD];
float bias [PE][NF];
float l1_out [PE][NF];
float d_l1_out [PE][NF];
float db1[PE][NF];
float dw1[PE][DEPTH][SIMD];

float buf_m2[L2_PE][L2_DEPTH][L2_SIMD];
float l2_bias[L2_SF][L2_SIMD];
float dw2[L2_PE][L2_DEPTH][L2_SIMD];
float db2[L2_SF][L2_SIMD];

float  mul(float const &c, float const &d) {
#pragma HLS inline
  float const  res = c*d;
  //std::cout<<"+"<<d<<"x"<<c<<" ";
//#pragma HLS RESOURCE variable=res core=DSP48
  return  res;
}


/**/
float mac(int N, float a, float buf_v[SIMD],float buf_m[SIMD]) {
#pragma HLS inline
#pragma HLS PIPELINE II=1
  float  res = a;
  float multresult[SIMD];
  #pragma HLS ARRAY_PARTITION variable=multresult complete dim=0

VM_SIMD:for(unsigned  i = 0; i < SIMD; i++) {
#pragma HLS unroll
	  multresult[i]= mul(buf_v[i], buf_m[i]);
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


void vmpu_A(hls::stream<VECTOR>&strm_out)
{
	  unsigned  L1_nf   = 0;
	  unsigned  L1_sf   = 0;
	  unsigned  tile = 0;
	  unsigned const TOTAL_FOLD = NF * SF;
	  float acc[PE];

      #pragma HLS ARRAY_PARTITION variable=acc complete dim=0

	  VECTOR o;
    // std::cout<<"hwl1_result--------";
	 VM_L1:for(unsigned fold=0;fold <TOTAL_FOLD;fold++)
			  {
				#pragma HLS PIPELINE II=5

	             // #pragma AP dependence variable=acc inter false

				 //  if(L1_sf == 0) {
		 L1_init: for(unsigned  pe = 0; pe < PE; pe++) {
				       #pragma HLS UNROLL
					    float temp  = bias[pe][L1_nf];
					    acc[pe]=temp;
				      }

				 // }


		     L1_pe: for(unsigned  pe = 0; pe < PE; pe++) {
	                  #pragma HLS UNROLL


				    	acc[pe]=mac(SIMD,acc[pe],buf_v[0],buf_m[pe][fold]);

				    }

		        // L1_sf++;
				//    if( L1_sf== SF) {
				      // produce output and clear accumulators
				       L1_sf = 0;
			L1_pestore:  for (unsigned  pe = 0; pe < PE; pe++) {
				       #pragma HLS UNROLL
				        l1_out[pe][L1_nf]=acc[pe]<0?0:acc[pe];

				      }
			          for (unsigned  pe = 0; pe < PE; pe++) {
                        #pragma HLS UNROLL
						float temp=l1_out[pe][L1_nf];
						d_l1_out[pe][L1_nf]= temp>0?1:0;
						//strm_out[pe].write(temp);
                        //out[pe]=l1_out[pe][L1_nf];
                        o.array[pe]=temp;

						//outElem[pe] = activation.activate(nf, pe, accu[pe]);
						//std::cout<<out[pe] <<"  ";
					 }
			          strm_out.write(o);

			/*L1_peout:  for (unsigned  pe = 0; pe < PE; pe++) {
                       #pragma HLS PIPELINE II=1
				        float temp=l1_out[pe][L1_nf];
				        d_l1_out[pe][L1_nf]= temp>0?1:0;
				        strm_out.write(temp);

				  	    //outElem[pe] = activation.activate(nf, pe, accu[pe]);
					    std::cout<<temp <<"  ";
				      }*/

					   if(++L1_nf == NF) {
						 L1_nf   = 0;
						}

			       //  }
				    //std::cout<<std::endl;
	       }

	// std::cout<<std::endl;
}
void vmpu_B(hls::stream<VECTOR>&strm_in,float *result,hls::stream<float>&strm_out)
{
	  VECTOR i;
	  unsigned  L2_nf   = 0;
	  unsigned  L2_sf   = 0;
	  unsigned  L2_tile = 0;
	  unsigned const L2_FOLD = L2_NF * L2_SF;
	  float acc[PE];
	  float multresult[L2_PE][L2_SIMD];
	  float addresult[L2_SIMD];
	  float addresult1[2];
      float l2_out[L2_SF][L2_SIMD];
    #pragma HLS ARRAY_PARTITION variable=acc complete dim=0
    #pragma HLS ARRAY_PARTITION variable=multresult  complete dim=0
    #pragma HLS ARRAY_PARTITION variable=addresult   complete dim=0
    #pragma HLS ARRAY_PARTITION variable=addresult1  complete dim=0

     #pragma HLS ARRAY_PARTITION variable=l2_out complete dim=0
   //#pragma HLS dependence variable=l2_out inter false
	 // std::cout<<"L2 hardware compute"<<std::endl;

	  VM_L2:for(unsigned fold=0;fold <L2_FOLD;fold++)
	  {
		#pragma HLS PIPELINE II=5

       // #pragma AP dependence variable=acc inter false
         if(L2_sf==0)
         {
        	i=strm_in.read();
      	   for(unsigned pe=0 ;pe<L2_PE;pe++)
      	   {
             #pragma HLS UNROLL
      		 //acc[pe]=strm_in[pe].read();
      		// acc[pe]=in[pe];
      		   acc[pe]=i.array[pe];
      	//	std::cout<<acc[pe] <<"  ";
      	   }

     // 	 std::cout<<endl;
         }

		   if(fold == 0) {
L2_init: for(unsigned  sf = 0; sf < L2_SF; sf++){
           //  #pragma HLS PIPELINE II=1
	         for  (unsigned  simd = 0; simd < L2_SIMD; simd++){
		         #pragma HLS UNROLL
	          l2_out[sf][simd] = l2_bias[sf][simd];

	         // std::cout << l2_out[sf][simd]<<" ";
		      }
            }

		  }

		  // std::cout<<std::endl;

   L2_pe: for(unsigned  pe = 0; pe < L2_PE; pe++) {
             #pragma HLS UNROLL
            //
   L2_simd:for(unsigned simd=0 ;simd<L2_SIMD;simd++)
	           {
               #pragma HLS UNROLL
  	    	  multresult[pe][simd]=buf_m2[pe][fold][simd]*acc[pe];

	           }
		    }
  // std::cout.setf(ios::fixed,ios::floatfield);
   L2_add: for(unsigned simd=0 ;simd<L2_SIMD;simd++)
         {
           #pragma HLS UNROLL
		   for(unsigned pe=0; pe<2;pe++)
		   {
			 #pragma HLS UNROLL
		      addresult1[pe]=multresult[2*pe][simd]+multresult[2*pe+1][simd];
		   }

			 addresult[simd]=addresult1[0]+addresult1[1];
	        l2_out[L2_sf][simd]+=addresult[simd];
         }

 /*  L2_resullt:for(unsigned simd=0 ;simd<L2_SIMD;simd++)
        {
            #pragma HLS UNROLL
  	     l2_out[L2_sf][simd]+=addresult[simd];
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


		//std::cout<<"hwl2_result------- ";
result_out:for(int sf=0;sf<L2_SF;sf++)
{

 for(int simd=0;simd<L2_SIMD;simd++){
#pragma HLS PIPELINE II=1

  float value =l2_out[sf][simd];
 // result[sf*L2_SIMD+simd] =value;
   strm_out.write(value);
 //  std::cout<<value<<" ";
 }
// std::cout<<std::endl;
}

//std::cout<<std::endl;

}


void vmpu(unsigned batch,float *result,hls::stream<float>&strm_out){
	static hls::stream<VECTOR>strm_v("stream_AB");

	#pragma HLS STREAM variable=strm_v depth=NF*SF

    #pragma HLS dataflow

	 vmpu_A(strm_v);

	 vmpu_B(strm_v,result,strm_out);

}


float back_mac(const int N, float a, float buf_v[L2_SIMD],float buf_m[L2_SIMD]) {
#pragma HLS inline
#pragma HLS PIPELINE II=1
  float  res = a;
  float multresult[N];
  #pragma HLS ARRAY_PARTITION variable=multresult complete dim=0

VM_SIMD:for(unsigned  i = 0; i < N; i++) {
#pragma HLS unroll
	  multresult[i]= mul(buf_v[i], buf_m[i]);

  }
float sum3[4];
#pragma HLS ARRAY_PARTITION variable=sum3 complete dim=1
float sum2[2];
#pragma HLS ARRAY_PARTITION variable=sum2 complete dim=1
float sum1;
ADDER_TREE_LOOP2:
	for(int i = 0; i < 4; i++)
	{
#pragma HLS UNROLL
		sum3[i] = multresult[2 * i] + multresult[2 * i + 1];
	}
ADDER_TREE_LOOP3:
	for(int i = 0; i < 2; i++)
	{
#pragma HLS UNROLL
		sum2[i] = sum3[2 * i] + sum3[2 * i + 1];
	}

sum1 =  sum2[0] + sum2[1]+ multresult[8]+multresult[9];
	res+=sum1;
	//std::cout<< res<<std::endl;
	//temp = intermediate_in + bias_in;
  return  res;
}

void back_vmpu(unsigned batch,hls::stream<float>&strm_in,float *result)
{

	 float delta_3[L2_SF][L2_SIMD];
	#pragma HLS ARRAY_PARTITION variable=delta_3 complete dim=0

	static hls::stream<VECTOR>strm_delta2("stream_delta2");
    #pragma HLS STREAM variable=strm_delta2 depth=L2_NF*L2_SF

 //   std::cout<<std::endl<<"hw_delta_3"<<"---";
    load_delta3:for(unsigned sf = 0 ;sf<L2_SF;sf++){
    	for(unsigned simd = 0;simd<L2_SIMD;simd++)
    	{
           #pragma HLS PIPELINE II=4
    		float delta = strm_in.read();
    		delta_3[sf][simd] = delta;

    		db2[sf][simd] += delta;
    	} }

	dataflow:{
#pragma HLS dataflow
    back_vmpu_B(delta_3,strm_delta2,result);
    back_vmpu_A(strm_delta2,result);
    calcu_dw3(delta_3);
	}



		 //
}

void back_vmpu_B(float delta_3[L2_SF][L2_SIMD],hls::stream<VECTOR>&strm_out,float *result)
{



    //calcu_dw3(delta_3);
	VECTOR back_o;
	unsigned  nf=0;
	unsigned  sf=0;
	unsigned const TOTAL_FOLD = L2_NF * L2_SF;
	float d3_out [L2_PE][L2_NF];
	float acc[L2_PE];
    #pragma HLS ARRAY_PARTITION variable=acc complete dim=0
    #pragma HLS ARRAY_PARTITION variable=d3_out complete dim=0

	 VM_d3_back:for(unsigned fold=0;fold <TOTAL_FOLD;fold++)
			  {
	//			#pragma HLS PIPELINE II=5

	             // #pragma AP dependence variable=acc inter false

				   if(sf == 0) {
	VM_d3_init: for(unsigned  pe = 0; pe < PE; pe++) {
				       #pragma HLS UNROLL
					    acc[pe]=0;
				      }

				  }


	 d3_back_pe: for(unsigned  pe = 0; pe < PE; pe++) {
	                  #pragma HLS UNROLL

				    	acc[pe]=back_mac(L2_SIMD,acc[pe],delta_3[sf],buf_m2[pe][fold]);

				    }

		         sf++;
				    if( sf== L2_SF) {
				      // produce output and clear accumulators
				         sf = 0;

   d3_back_pestore:  for (unsigned  pe = 0; pe < PE; pe++) {
				       #pragma HLS UNROLL

                 	  d3_out[pe][nf]=d_l1_out[pe][nf]==0?0:acc[pe];
                 	   db1[pe][nf]+= d3_out[pe][nf];
				      }
                    // std::cout<<std::endl;
     d3_back_peout:  for (unsigned  pe = 0; pe < PE; pe++) {

				        float delta_temp=d3_out[pe][nf];
				        back_o.array[pe]=delta_temp;
				       // std::cout<<delta_temp<<" ";
				        //strm_out.write(delta_temp);
                     }
                      strm_out.write(back_o);
                    //  std::cout<<std::endl;
					   if(++nf == L2_NF) {
						 nf = 0;
						}

			         }


       }
		// std::cout<<"write result";
		 //fflush(stdout);
		 /*result_out:for(int pe=0;pe<L2_PE;pe++)
		 {
		  for(int nf=0;nf<L2_NF;nf++){
		 #pragma HLS PIPELINE II=1

		   float value =d3_out[pe][nf];
		   result[pe*L2_NF+nf] =value;
		   //std::cout<<value<<" ";
		    //strm_out.write(value);
		  }
		 }*/

}


void calcu_dw3(float delta_3[L2_SF][L2_SIMD])
{
	 unsigned flod=0;
	 dw_out1: for(unsigned  v2_nf=0; v2_nf<L2_NF;v2_nf++){

		 dw_out2 :for(unsigned  d3_sf=0; d3_sf<L2_SF;d3_sf++){
		//	  #pragma HLS PIPELINE II=5

				for(unsigned  v2_pe=0; v2_pe<L2_PE;v2_pe++){
				   #pragma HLS UNROLL

					 for(unsigned  d3_simd=0; d3_simd<L2_SIMD;d3_simd++)
				 {
					#pragma HLS UNROLL
					dw2[v2_pe][flod][d3_simd]+= l1_out[v2_pe][v2_nf]*delta_3[d3_sf][d3_simd];

				 }
				}
			 flod++;
		   }
	   }

}


void back_vmpu_A(hls::stream<VECTOR>&strm_in,float *result)
{
//	std::cout<<std::endl<<"hw_delta2--"<<"---";
	VECTOR back_i;
	 unsigned flod=0;
	 dw_out1: for(unsigned  nf=0; nf<NF;nf++){
		 dw_out2 :for(unsigned  v1_sf=0; v1_sf<SF;v1_sf++){
			     float delta_2[PE];
			  #pragma HLS PIPELINE II=5
                 if(v1_sf==0)
                 {
                	 back_i=strm_in.read();
                	 for(unsigned pe=0;pe<L2_PE;pe++)
                	 {
                       #pragma HLS UNROLL
                        // float delta = strm_in.read();
                         delta_2[pe]=back_i.array[pe];
                         //std::cout<<delta<<"  ";
                	 }

                 }
                // std::cout<<flod<<std::endl;
				for(unsigned  d2_pe=0; d2_pe<PE;d2_pe++){
				   #pragma HLS UNROLL
					 for(unsigned  v1_simd=0; v1_simd<SIMD;v1_simd++)
				 {
					#pragma HLS UNROLL
					dw1[d2_pe][flod][v1_simd]+= buf_v[v1_sf][v1_simd]*delta_2[d2_pe];
					//std::cout<<dw1[d2_pe][flod][v1_simd]<<"  ";
				 }
					// std::cout<<std::endl;
				}
			 flod++;
		   }
	   }
}

