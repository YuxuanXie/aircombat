#ifndef  XFPGA_HPP
#define  XFPGA_HPP

//#include "xdqn_fpgatop.h"
#include "DQN.hpp"
#include "axilite.hpp"
//#include "xil_printf.h"
//#include "sleep.h"


int FPGA_DQN_core_Init(void);
void FPGA_setDQNInfo(DQN_info info,unsigned char doInit,bool mode,bool check);
void FPGA_DQN(DQN_info info,unsigned char doInit,bool mode,bool check);
void FPGA_readDQNInfo();
void send_weight_to_FPGA(DQN_info info);
void FPGA_DQN_core_Release();
void XDqn_fpgatop_Start();

u32 XDqn_fpgatop_IsDone();

u32 XDqn_fpgatop_IsIdle();
u32 XDqn_fpgatop_IsReady() ;
void FPGA_setMemory(int iter);

#endif
