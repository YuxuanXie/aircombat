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
	//m_listenfd=socket(AF_INET,SOCK_DGRAM,0);//监听
	if(m_listenfd==-1)
	{
		perror("creating socket failed");
		return false;
	}
	struct sockaddr_in serveaddr;
	memset(&serveaddr,0,sizeof(serveaddr));
	serveaddr.sin_family=AF_INET;   //ipv4协议族
	serveaddr.sin_addr.s_addr=inet_addr(Getlocal_ip());
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
		printf("SERVER recv msg failed with error: %d\n", iErrMsg);
		exit(-1);

	}
}
void CServer::Send(char *msg,int len)
{
	int iErrMsg = 0;
	iErrMsg = send(m_clientfd, msg,len, 0); //发送
	if (iErrMsg < 0)
	{
		printf("SERVER send msg failed with error: %d\n", iErrMsg);
		exit(-1);
	}
	if (strcmp(msg, "exit") == 0) {
		std::cout << "...disconnect" << std::endl;
		close(m_clientfd);
	}
}

const char* CServer::Getlocal_ip()
{
    int sockfd;
    struct ifconf ifconf;
    struct ifreq *ifreq;
    char buf[512];//缓冲区
    //初始化ifconf
    ifconf.ifc_len =512;
    ifconf.ifc_buf = buf;
    if ((sockfd =socket(AF_INET,SOCK_DGRAM,0))<0)
    {
        perror("socket error in getlocal_ip." );
        exit(1);
    }
    ioctl(sockfd, SIOCGIFCONF, &ifconf); //获取所有接口信息

    //接下来一个一个的获取IP地址
    ifreq = (struct ifreq*)ifconf.ifc_buf;

    for (int i=(ifconf.ifc_len/sizeof (struct ifreq)); i>0; i--)
    {
        if(ifreq->ifr_flags == AF_INET){ //for ipv4
        	std::string cc = (std::string)(inet_ntoa(((struct sockaddr_in*)&(ifreq->ifr_addr))->sin_addr));
        	if(cc[0]=='1'&&cc[1]=='9'&&cc[2]=='2'){
            	std::cout<<"LOCAL_IP:"<<cc<<std::endl;
            	local_ip = cc;
                break;
        	}
        	ifreq++;
        }
    }
    close(sockfd);
	return local_ip.c_str();
}

void  CServer::Close()
{
	if(m_listenfd>0)  close(m_listenfd);
	if(m_clientfd>0)  close(m_clientfd);
}

CServer2::CServer2()
{
	m_listenfd=0;
	m_clientfd=0;
}
CServer2::~CServer2()
{
	close(m_listenfd);
	close(m_clientfd);
}

bool CServer2::initserver(const int port)
{
	//m_listenfd=socket(AF_INET,SOCK_STREAM,0);//监听
	m_listenfd=socket(AF_INET,SOCK_DGRAM,0);//监听
	if(m_listenfd==-1)
	{
		perror("creating socket failed");
		return false;
	}
	struct sockaddr_in serveaddr;
	memset(&serveaddr,0,sizeof(serveaddr));
	serveaddr.sin_family=AF_INET;   //ipv4协议族
	serveaddr.sin_addr.s_addr=inet_addr("192.168.0.2");
	serveaddr.sin_port=htons(port);
	if(bind (m_listenfd,(const struct sockaddr*)&serveaddr,sizeof(serveaddr))!=0){
		perror("bind");close(m_listenfd);return false;}
	//if(listen(m_listenfd,5)!=0){
	//perror("listen");close(m_listenfd);return false;}
	return true;
}

void CServer2::Recv(char *msg,int len)
{
	int iErrMsg = 0;
	struct sockaddr_in cli;
	socklen_t sock_len = sizeof(cli);
	iErrMsg = recvfrom(m_clientfd,msg, len, 0,(struct sockaddr*)&cli,&sock_len);
	if (iErrMsg < 0)
	{
		printf("SERVER recv msg failed with error: %d\n", iErrMsg);
		exit(-1);
	}
}
void CServer2::Send(char *msg,int len)
{
	int iErrMsg = 0;
	struct sockaddr_in cli;
	iErrMsg = sendto(m_clientfd, msg,len, 0,(struct sockaddr*)&cli,sizeof(cli)); //发送
	if (iErrMsg < 0)
	{
		printf("SERVER send msg failed with error: %d\n", iErrMsg);
		exit(-1);
	}
	if (strcmp(msg, "exit") == 0) {
		std::cout << "...disconnect" << std::endl;
		close(m_clientfd);
	}
}

void  CServer2::Close()
{
	close(m_listenfd);
	close(m_clientfd);
}



#endif
