// Single thread C server program. 
#include <unistd.h> 
#include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 
#include <sys/socket.h> 
#include <arpa/inet.h>
#include <netinet/in.h> 
#include <fcntl.h> // for open
#include <unistd.h> // for close
#include <pthread.h>
#include<sys/wait.h> 

#define PORT 8080 
#define BUF_SIZE 1024
#define MAX_GAMES 50
#define NUM_SHIPS 3
#define MAX_REQUESTS_QUEUED MAX_GAMES*2


void gamePlay(int player1fd, int player2fd){
  
  char buffer[BUF_SIZE];
  send(player1fd , buffer , BUF_SIZE , 0);
  send(player2fd , buffer , BUF_SIZE , 0);
  

  // Send message to the client socket 
  // char* start_message = "Player please start placing battleship!\n";
    // send(clientfd , start_message, strlen(start_message) , 0 );
    // //read the message recieved 
    // while (valread = read(clientfd, buffer, BUF_SIZE)){
    //     printf("Recieved from client: %s\n",buffer);
    //     for(int j=0;j<BUF_SIZE;j++) buffer[j] = 0;

    //     //send to client
    //     valread = read(STDIN_FILENO , buffer, BUF_SIZE); 
    //     send(clientfd , buffer, BUF_SIZE , 0 ); 
    //     printf("Message sent: %s\n", buffer); 
    //     for(int j=0;j<=BUF_SIZE;j++) buffer[j] = 0;
    // }
    pthread_mutex_lock(&lock);
    char *message = malloc(sizeof(client_message)+20);
    strcpy(message,"Hello Client : ");
    strcat(message,client_message);
    strcat(message,"\n");
    strcpy(buffer,message);
    free(message);
    pthread_mutex_unlock(&lock);


  close(player2fd);
  close(player1fd);  
}

int main(int argc, char const *argv[]){
    int servfd, player1fd, player2fd, valread; 
    struct sockaddr_in address; 
    char buffer[BUF_SIZE] = {0}; 
    unsigned int addrlen;

    // Creating server socket that uses IPv4
    servfd = socket(AF_INET, SOCK_STREAM, 0);
    if (servfd == 0){ 
        perror("socket creation failed"); 
        exit(EXIT_FAILURE); 
    }
    else{
        printf("server socket created with file descriptor %d\n", servfd);
    }
    

    int option_value = 1; 
    // set socket to TCP level protocal 
    if (setsockopt(servfd, SOL_SOCKET, SO_REUSEADDR, &option_value, sizeof(option_value))){ 
        perror("setsockopt"); 
        exit(EXIT_FAILURE); 
    }
    else{
        printf("set socket to TCP protocal level\n");
    }


    // bind the socket to an address and port 
    bzero((char *) &address, sizeof(address));
    address.sin_family = AF_INET; 
    address.sin_addr.s_addr = INADDR_ANY; 
    address.sin_port = htons( PORT ); 
    if (bind(servfd, (struct sockaddr *)&address, sizeof(address))<0){ 
        perror("bind failed"); 
        exit(EXIT_FAILURE); 
    } 
    else{
        printf("server addr boound port %d correctly\n", PORT);
    }


    // Start listening for incoming connections, max 5 connections a time
    if (listen(servfd, MAX_REQUESTS_QUEUED) < 0){ 
        perror("listening failed"); 
        exit(EXIT_FAILURE); 
    } 
    else{
        printf("listening\n");
    }


    pthread_t pids[MAX_GAMES];
    int count = 0;
    while(1){
        //accept the client socket
        char dst[INET_ADDRSTRLEN+1];
        addrlen = sizeof(address);
        player1fd = accept(servfd, (struct sockaddr *) &address, (socklen_t*) &addrlen);
        if (player1fd < 0){ perror("accept failed"); exit(EXIT_FAILURE); }    
        else{
            printf("Connection established player1 with IP %s.\n",
            inet_ntop(AF_INET, &(address.sin_addr), dst, INET_ADDRSTRLEN));
        }

        player2fd = accept(servfd, (struct sockaddr *) &address, (socklen_t*) &addrlen);
        if (player2fd < 0){ perror("accept failed"); exit(EXIT_FAILURE); }    
        else{
            printf("Connection established player2 with IP %s.\n",
            inet_ntop(AF_INET, &(address.sin_addr), dst, INET_ADDRSTRLEN));
        }

        int pid = 0;
        if ((pid = fork())==0) gamePlay(player1fd, player2fd);
        else{
          pids[count++] = pid;
          if(count >= 49){
             count = 0;
             while(count < 50) waitpid(pids[count++], NULL, 0);
             count = 0;
          }
        }
    }
    return 0; 
} 
