/*
 * cclient.cpp
 *
 *  Created on: 2021年4月15日
 *      Author: chuanshuo16nian
 */

#ifndef CCLIENT_CPP_
#define CCLIENT_CPP_
#include"cclient.hpp"

CClient::CClient()
{
  m_clientfd=0;
}
CClient::~CClient()
{
  if(m_clientfd>0)  close(m_clientfd);
}
bool CClient::connect_to_server(const char *serveip,const int port)
{
  m_clientfd=socket(AF_INET,SOCK_STREAM,0);
  struct hostent* h;
  memset(h,0,sizeof(h));
  h=gethostbyname(serveip);
  if(h==0)
  {
    close(m_clientfd);
    m_clientfd=0;
    return false;
  }
  struct sockaddr_in serveaddr;
  memset(&serveaddr,0,sizeof(serveaddr));
  serveaddr.sin_family=AF_INET;   //ipv4协议族
  serveaddr.sin_port=htons(port);
  memcpy(&serveaddr.sin_addr,h->h_addr,h->h_length);
  if(connect(m_clientfd,(struct sockaddr *)&serveaddr,sizeof(serveaddr))!=0)
  {
    perror("connect");
    close(m_clientfd);
  return false;
  }
return true;
}
ssize_t CClient::Recv(void *buf,size_t len)
{
  memset(buf,0,len);
  return recv(m_clientfd,buf,len,0);
}
ssize_t CClient::Send(const void *buf,size_t len)
{
  return send(m_clientfd,buf,len,0);
}














#endif
