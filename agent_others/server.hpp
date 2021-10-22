/*
 * server.hpp
 *
 *  Created on: 2021Äê4ÔÂ15ÈÕ
 *      Author: chuanshuo16nian
 */

#ifndef SRC_SERVER_HPP_
#define SRC_SERVER_HPP_

#include <stdio.h>
#include<unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#include<stdlib.h>
#include<sys/stat.h>
#include<time.h>
#include <stdarg.h>
#include<iostream>
class CServer
{
private:
  int m_listenfd;
  int m_clientfd;
public:
  CServer();
  ~CServer();
  bool initserver(const int port);
  bool Accept();
  void Recv(char *msg,int len);
  void Send(char *msg,int len);
};



#endif /* SRC_SERVER_HPP_ */
