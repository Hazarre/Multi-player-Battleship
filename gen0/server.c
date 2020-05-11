// Single thread C server program. 
#include <unistd.h> 
#include <stdio.h> 
#include <sys/socket.h> 
#include <stdlib.h> 
#include <netinet/in.h> 
#include <string.h> 
#define PORT 8080 
#define BUF_SIZE 1024

int main(int argc, char const *argv[]){
    int servfd, clientfd, valread; 
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
    if (listen(servfd, 5) < 0){ 
        perror("listening failed"); 
        exit(EXIT_FAILURE); 
    } 
    else{
        printf("listening\n");
    }

    //accept the client socket
    addrlen = sizeof(address);
    clientfd = accept(servfd, (struct sockaddr *) &address, (socklen_t*) &addrlen);
    if (clientfd < 0){ 
        perror("accept faileed"); 
        exit(EXIT_FAILURE); 
    } 
    else{
        printf("Connection established client @ IP %s.\n", inet_ntoa(address.sin_addr));
    }


    //read the message recieved 
    while (valread = read(clientfd, buffer, BUF_SIZE)){
        printf("Recieved from client: %s\n",buffer);

        //send to client
        valread = read(STDIN_FILENO , buffer, BUF_SIZE); 
        send(clientfd , buffer, BUF_SIZE , 0 ); 
        printf("Message sent: %s\n", buffer); 

    }
    
    close(servfd);
    return 0; 
} 