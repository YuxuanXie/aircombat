#include "xfpga.hpp"
#include "stdio.h"
#include "shared_dram.hpp"
#include "config.hpp"
//#include "xtime_l.h"
#include "drivers/DQN_fpgatop_v4_0/src/xdqn_fpgatop.h"
//XDqn_fpgatop_Config *DQN_Ptr;

XDqn_fpgatop DQN;

#define DQN_CTRL_BASE 0x43C00000


int FPGA_DQN_core_Init(void)
{
	int status;
	// Look Up the device configuration
//	DQN_Ptr = XDqn_fpgatop_LookupConfig(XPAR_DQN_FPGATOP_0_DEVICE_ID);
//	if (!DQN_Ptr) {
//		print("ERROR: Lookup of DQN accelerator configuration failed.\n\r");
//		return XST_FAILURE;
//	}
//
//	// Initialize the Device
//	status = XDqn_fpgatop_CfgInitialize(&DQN,DQN_Ptr);
//	if (status != XST_SUCCESS) {
//		print("ERROR: Could not initialize DQN accelerator.\n\r");
//		 exit(-1);
//	}
	printf("XFPGA Driver: Initialize\n");
	axilite_open();

	SHARED_DRAM_open();
//	status= XDqn_fpgatop_Initialize(&DQN, "DQN_fpgatop_0");
//	if (status != XST_SUCCESS) {
//		printf("ERROR: Could not initialize DQN accelerator.\n\r");
//		 exit(-1);
//	}
	return XST_SUCCESS;

}
void FPGA_DQN_core_Release() {
  printf("XFPGA Driver: Release\n");
  axilite_close();
  //SHARED_DRAM_close();
}

void FPGA_setMemory(int iter)
{
	 volatile float *SHARED_DRAM = XFPGA_shared_DRAM_physical();
	 axilite_write(XDQN_FPGATOP_CONTROL_ADDR_MATRIX_IN_DATA,(u32)SHARED_DRAM);
	 //XDqn_fpgatop_WriteReg(DQN_CTRL_BASE, XDQN_FPGATOP_CONTROL_ADDR_MATRIX_IN_DATA, (u32)matrix_in );

	 axilite_write(XDQN_FPGATOP_CONTROL_ADDR_BIAS_IN_DATA,(u32)(SHARED_DRAM+L1_NUM*L2_NUM+L2_NUM*L3_NUM));
	 //XDqn_fpgatop_WriteReg(DQN_CTRL_BASE, XDQN_FPGATOP_CONTROL_ADDR_BIAS_IN_DATA, (u32)bias_in );


	 axilite_write(XDQN_FPGATOP_CONTROL_ADDR_VECTOR_IN_DATA,(u32)(SHARED_DRAM+L1_NUM*L2_NUM+L2_NUM*L3_NUM+L2_NUM+L3_NUM));
	 //XDqn_fpgatop_WriteReg(DQN_CTRL_BASE, XDQN_FPGATOP_CONTROL_ADDR_VECTOR_IN_DATA,  (u32)vector_in);

	 axilite_write(XDQN_FPGATOP_CONTROL_ADDR_EX_MEMORY_DATA,(u32)(SHARED_DRAM+L1_NUM*L2_NUM+L2_NUM*L3_NUM+L2_NUM+L3_NUM+L1_NUM));
	 //XDqn_fpgatop_WriteReg(DQN_CTRL_BASE, XDQN_FPGATOP_CONTROL_ADDR_EX_MEMORY_DATA,(u32)ex_memory  );


	 axilite_write(XDQN_FPGATOP_CONTROL_ADDR_RESULT_DATA,(u32)(SHARED_DRAM+L1_NUM*L2_NUM+L2_NUM*L3_NUM+L2_NUM+L3_NUM+L1_NUM+iter*BATCH_SIZE));
	 //XDqn_fpgatop_WriteReg(DQN_CTRL_BASE, XDQN_FPGATOP_CONTROL_ADDR_RESULT_DATA,(u32)result );

}
void FPGA_setDQNInfo( DQN_info info,unsigned char doInit,bool mode,bool check) {




	 axilite_write(XDQN_FPGATOP_CONTROL_ADDR_INFO_LEARNING_RATE_DATA,*(u32*)&(info.learning_rate));
	// axilite_write(XDQN_FPGATOP_CONTROL_ADDR_INFO_LEARNING_RATE_DATA,info.learning_rate);
	// XDqn_fpgatop_WriteReg(DQN_CTRL_BASE, XDQN_FPGATOP_CONTROL_ADDR_INFO_LEARNING_RATE_DATA,*(u32*)&(info.learning_rate)  );
     //printf("%f",*(u32*)&(info.learning_rate));

	 axilite_write(XDQN_FPGATOP_CONTROL_ADDR_INFO_REWARD_DECAY_DATA,*(u32*)&(info.reward_decay ));
	 //axilite_write(XDQN_FPGATOP_CONTROL_ADDR_INFO_REWARD_DECAY_DATA,info.reward_decay);
	 //XDqn_fpgatop_WriteReg(DQN_CTRL_BASE, XDQN_FPGATOP_CONTROL_ADDR_INFO_REWARD_DECAY_DATA,*(u32*)&(info.reward_decay ) );

	 axilite_write(XDQN_FPGATOP_CONTROL_ADDR_INFO_ITER_N_DATA,info.iter_n);
	 //XDqn_fpgatop_WriteReg(DQN_CTRL_BASE, XDQN_FPGATOP_CONTROL_ADDR_INFO_ITER_N_DATA, info.iter_n );

	 axilite_write(XDQN_FPGATOP_CONTROL_ADDR_INFO_BATCH_SIZE_DATA,info.batch_size);
	 //XDqn_fpgatop_WriteReg(DQN_CTRL_BASE, XDQN_FPGATOP_CONTROL_ADDR_INFO_BATCH_SIZE_DATA,info.batch_size  );

	 axilite_write(XDQN_FPGATOP_CONTROL_ADDR_DOINIT_DATA,doInit);
	 //XDqn_fpgatop_WriteReg(DQN_CTRL_BASE, XDQN_FPGATOP_CONTROL_ADDR_DOINIT_V_DATA, doInit );

	 axilite_write(XDQN_FPGATOP_CONTROL_ADDR_MODE_DATA,mode);
	 //XDqn_fpgatop_WriteReg(DQN_CTRL_BASE, XDQN_FPGATOP_CONTROL_ADDR_MODE_DATA, mode);

	 axilite_write(XDQN_FPGATOP_CONTROL_ADDR_CHECK_DATA,check);
	 //XDqn_fpgatop_WriteReg(DQN_CTRL_BASE, XDQN_FPGATOP_CONTROL_ADDR_CHECK_DATA, check);

}


void FPGA_readDQNInfo() {
  //XFPGA_Set_layer_width_V(256);
	u32 data;
    float fdata;





    data=  axilite_read(XDQN_FPGATOP_CONTROL_ADDR_MATRIX_IN_DATA);
    //printf("matrix_in ->%x \r\n",data);
    data=  axilite_read(XDQN_FPGATOP_CONTROL_ADDR_BIAS_IN_DATA);
    //printf("bias_in ->%x \r\n",data);
    data= axilite_read(XDQN_FPGATOP_CONTROL_ADDR_VECTOR_IN_DATA);
    //printf("vector_in ->%x \r\n",data);
	data= axilite_read(XDQN_FPGATOP_CONTROL_ADDR_EX_MEMORY_DATA);
    //printf("ex_memory ->%x \r\n",data);
    data= axilite_read(XDQN_FPGATOP_CONTROL_ADDR_RESULT_DATA);
    //printf("result_in ->%x \r\n",data);
    fdata=  axilite_read(XDQN_FPGATOP_CONTROL_ADDR_INFO_LEARNING_RATE_DATA);
    //printf("learning_rate ->%f \r\n",fdata);
    fdata= axilite_read(XDQN_FPGATOP_CONTROL_ADDR_INFO_REWARD_DECAY_DATA);
   // printf("reward_decay ->%f \r\n",fdata);
	 data =axilite_read(XDQN_FPGATOP_CONTROL_ADDR_INFO_ITER_N_DATA);
	 //printf("iter_n ->%d \r\n",data);
	 data =axilite_read(XDQN_FPGATOP_CONTROL_ADDR_INFO_BATCH_SIZE_DATA);
	 //printf("batch_size ->%d \r\n",data);
	 data =axilite_read(XDQN_FPGATOP_CONTROL_ADDR_DOINIT_DATA);
	 //printf("doinit ->%d \r\n",data);
	 data =axilite_read(XDQN_FPGATOP_CONTROL_ADDR_MODE_DATA);
	 //printf("mode ->%d \r\n",data);
	//printf("XPOOL_TOP_AXILITE_ADDR_LAYER_POOL_DATA           --> %d \n",data);
}

void send_weight_to_FPGA(DQN_info info)
{
	// send the weight data to PL
	FPGA_setDQNInfo(info,1,0,0);
	//FPGA_readDQNInfo() ;
	XDqn_fpgatop_Start();
	fflush(stdout);
    while (!XDqn_fpgatop_IsDone()) { // busy-wait
      //usleep(1);            // sleep 100us
      //print("send the weight data to PL");
    }
}
void FPGA_DQN(DQN_info info,unsigned char doInit,bool mode,bool check)
{

	   //info.batch_size=1;
	   FPGA_setDQNInfo(info,doInit,mode,check);
	   FPGA_readDQNInfo() ;
	   XDqn_fpgatop_Start();
	   while (!XDqn_fpgatop_IsDone()) { // busy-wait
		// usleep(1);            // sleep 100us
		// print("inference ,get the Q value  from  evaluate network");
	   }
	   fflush(stdout);
	// Train ,get the update date  value  from PL
//
//	   info.batch_size=BATCH_SIZE;
//	   FPGA_setDQNInfo(info,0,0,0);
//	   FPGA_readDQNInfo();
//	   XDqn_fpgatop_Start();
//	   while (!XDqn_fpgatop_IsDone()) { // busy-wait
//		 //usleep(1);            // sleep 100us
//		// print("Train ,get the update date  value  from PL");
//	   }
//	   fflush(stdout);
	//   XTime_GetTime(&tEnd);
	  //	  tUsed = ((tEnd-tCur)*1000000)/(COUNTS_PER_SECOND);
	  	//  xil_printf("time elapsed is %d us\r\n",tUsed);
}
void XDqn_fpgatop_Start() {

    u32 Data = axilite_read(XDQN_FPGATOP_CONTROL_ADDR_AP_CTRL) & 0x80;
     axilite_write(XDQN_FPGATOP_CONTROL_ADDR_AP_CTRL, Data | 0x01);
}
u32 XDqn_fpgatop_IsDone() {
	  u32 Data = axilite_read(XDQN_FPGATOP_CONTROL_ADDR_AP_CTRL);
	  return (Data >> 1) & 0x1;
}

u32 XDqn_fpgatop_IsIdle() {
	  u32 Data = axilite_read(XDQN_FPGATOP_CONTROL_ADDR_AP_CTRL);
	  return (Data >> 2) & 0x1;
}

u32 XDqn_fpgatop_IsReady() {
	  u32 Data = axilite_read(XDQN_FPGATOP_CONTROL_ADDR_AP_CTRL);
	  // check ap_start to see if the pcore is ready for next input
	  return !(Data & 0x1);
}
