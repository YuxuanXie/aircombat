#ifndef CLIENTNET_CPP_
#define CLIENTNET_CPP_

#include"client.hpp"


int ClientNet::ClientConnect(int port, const char* address)
{
	cout<<"Agent connecting the test environment......."<<endl;
	socket_fd = socket(AF_INET, SOCK_STREAM,0);
	if(socket_fd == -1)
	{
		cout<<"create socket error"<<endl;
		exit(-1);
	}
	struct sockaddr_in addr;
	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_port = htons(port);
	addr.sin_addr.s_addr = inet_addr(address);
	int res = connect(socket_fd,(struct sockaddr*)&addr,sizeof(addr));
	if(res == -1) {
		cout<<"bind error"<<endl;
		exit(-1);
	}

   cout<<"agent1 connect environment server successfully."<<endl;
   cout<<"-------------------------"<<endl;

}


void ClientNet::ClientSend(char* msg, int len)
{
	int iErrMsg = 0;
	iErrMsg = send(socket_fd, msg,len, 0); //·¢ËÍ
	if (iErrMsg < 0)
	{
		printf("PC send msg failed with error: %d\n", iErrMsg);
		exit(-1);
	}
  if (strcmp(msg, "exit") == 0) {
         std::cout << "...disconnect" << std::endl;
         close(socket_fd);
     }

}

void ClientNet::ClientRecv(char* msg, int len)
{


	int iErrMsg = 0;


	iErrMsg = recv(socket_fd,msg, len, 0);
	if (iErrMsg < 0)
	{
		printf("PC recv msg failed with error: %d\n", iErrMsg);
		exit(-1);

	}
	//printf("recv msg successfully\n");
}

void ClientNet::ClientClose()
{
	close(socket_fd);

}




#endif /* CLIENTNET_CPP_ */
