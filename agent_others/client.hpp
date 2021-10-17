#ifndef   CLIENT_HPP
#define   CLIENT_HPP
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<errno.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include<iostream>
using namespace std;
class ClientNet
{
	private:
	int socket_fd;

	public:

	int ClientConnect(int port, const char* address);
	void ClientSend(char* msg, int len);
	void ClientRecv(char* msg, int len);
	void ClientClose();

};
#endif
