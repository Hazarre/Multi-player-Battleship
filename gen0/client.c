// Client side C/C++ program to demonstrate Socket programming 
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <unistd.h> 
#include <string.h> 
#define PORT 8080 
#define BUF_SIZE 1024

int main(int argc, char const *argv[]) { 
	int clientfd = 0, valread; 
	struct sockaddr_in serv_addr; 
	char buffer[BUF_SIZE] = {0}; 


  // Create client socket that uses IPv4
	if ((clientfd = socket(AF_INET, SOCK_STREAM, 0)) < 0){ 
		printf("\n Socket creation error \n"); 
		return -1; 
	} 


	serv_addr.sin_family = AF_INET; 
	serv_addr.sin_port = htons(PORT); 
	
	// Convert IPv4 and IPv6 addresses from text to binary form 
	if(inet_pton(AF_INET, "10.10.54.144", &serv_addr.sin_addr)<=0){ 
		printf("\nInvalid address/ Address not supported \n"); 
		return -1; 
	} 

	if (connect(clientfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0){ 
		printf("\nConnection Failed \n"); 
		return -1; 
	}
  else{
    printf("Connected to server.\n");
  }




  //interact with the server
  while(valread = read( clientfd , buffer, BUF_SIZE)){
	    printf("Recieved from server: %s\n",buffer ); 

      // send to server
      valread = read(STDIN_FILENO , buffer, BUF_SIZE); 
      send(clientfd , buffer , BUF_SIZE , 0); 
	    printf("Message sent to server: %s\n", buffer); 

      if(buffer[0]=='e') break;
  }

  close(clientfd);
	return 0; 
} 
