/*
 * cclient.hpp
 *
 *  Created on: 2021Äê4ÔÂ15ÈÕ
 *      Author: chuanshuo16nian
 */

#ifndef SRC_CCLIENT_HPP_
#define SRC_CCLIENT_HPP_

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

class CClient
{
private:
  int m_clientfd;
public:
  CClient();
  ~CClient();
  bool connect_to_server(const char *serveip,const int port);
  ssize_t Recv(void *buf, size_t len);
  ssize_t Send(const void *buf, size_t len);
};



#endif /* SRC_CCLIENT_HPP_ */
