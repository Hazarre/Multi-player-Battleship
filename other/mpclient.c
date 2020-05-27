// Client side C program to demonstrate Socket programming 
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
	if(inet_pton(AF_INET, "18.209.174.234", &serv_addr.sin_addr)<=0){ 
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
  char type, x, y, direction;

  while(valread = read(clientfd , buffer, BUF_SIZE)){
	  // Move data is stored in buffer
	  // Recieve opponents move from server
	  printf("Recieved from server: %s\n", buffer); 
	  player=buffer[0];
	  type = buffer[1];
	  x    = buffer[2];
	  y    = buffer[3];
	  direction = buffer[4];
	  // call some game API opponent_move(type, x, y, direction);
      // to update the game status based on the opponents move.
	  for(int j=0;j<=BUF_SIZE;j++) buffer[j] = 0;


      // call some game API player_move(buffer) that updates 
	  // the game status based on the player's move
	  // and store the player's move in buffer
      // send player's move to server
	  // if inputting player's move from stdin, keep the following line
	  read(STDIN_FILENO , buffer, BUF_SIZE);
	  send(clientfd , buffer , BUF_SIZE , 0);
	  if(buffer[0]=='e') break; // this ends the game, add end game condition into the if
	  printf("Message sent to server: %s\n", buffer); 
	  for(int j=0;j<=BUF_SIZE;j++) buffer[j] = 0;
  }
  printf("GAME OVER\n");
  close(clientfd);
  return 0; 
} 
