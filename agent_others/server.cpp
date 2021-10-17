/*
 * server.cpp
 *
 *  Created on: 2021年4月15日
 *      Author: chuanshuo16nian
 */
#ifndef SERVER_CPP_
#define SERVER_CPP_
#include"server.hpp"
CServer::CServer()
{
  m_listenfd=0;
  m_clientfd=0;
}
CServer::~CServer()
{
  if(m_listenfd>0)  close(m_listenfd);
  if(m_clientfd>0)  close(m_clientfd);
}
bool CServer::initserver(const int port)
{
  m_listenfd=socket(AF_INET,SOCK_STREAM,0);//监听
  if(m_listenfd==-1)
  {
	  perror("creating socket failed");
	  return false;
  }
  struct sockaddr_in serveaddr;
  memset(&serveaddr,0,sizeof(serveaddr));
  serveaddr.sin_family=AF_INET;   //ipv4协议族
  serveaddr.sin_addr.s_addr=inet_addr("192.168.1.111");
  serveaddr.sin_port=htons(port);
  if(bind (m_listenfd,(const struct sockaddr*)&serveaddr,sizeof(serveaddr))!=0){
    perror("bind");close(m_listenfd);return false;}
  if(listen(m_listenfd,5)!=0){
    perror("listen");close(m_listenfd);return false;}
return true;
}
bool CServer::Accept()
{
  int socklen;
  struct sockaddr_in clientaddr;  //客户端的地址信息
  m_clientfd=accept(m_listenfd,(struct sockaddr *)&clientaddr,(socklen_t*)&socklen);
  if(m_clientfd<0)  return false;
  return true;
}
void CServer::Recv(char *msg,int len)
{
	int iErrMsg = 0;

	iErrMsg = recv(m_clientfd,msg, len, 0);
	if (iErrMsg < 0)
	{
		printf("recv msg failed with error: %d\n", iErrMsg);
		exit(-1);

	}
}
void CServer::Send(char *msg,int len)
{
	int iErrMsg = 0;
	iErrMsg = send(m_clientfd, msg,len, 0); //发送
	if (iErrMsg < 0)
	{
		printf("send msg failed with error: %d\n", iErrMsg);
		exit(-1);
	}
	 if (strcmp(msg, "exit") == 0) {
	         std::cout << "...disconnect" << std::endl;
	         close(m_clientfd);
	  }
}








#endif
