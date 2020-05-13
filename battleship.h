// client status 
#define CONNECTING_TO_SERVER
#define MATCHING
#define IN_GAME
#define MY_TURN
#define WAITING_FOR_OPPONENT
#define GAME_OVER

//after every move of each player
//the client sends some Move data to the server
//then the client hangs until receiving some data from the server. 
//client -> server
struct Move{
    int player; // 1 or 2 in each game, assigned by the server
    int type; // 0 for placing ship, 1 for guessing target. 
    int x; // 
    int y;
};

// The move data will be communicated between the server client in the 
// following array formate: 
// int move = {player, type, x, y};



//before every new move, the server will send the client some info. 
struct Update{
    char** state;// a matrix of the game board
    int;

};

//