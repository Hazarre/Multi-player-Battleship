#define PORT 8080 
/* Round procedure:
Player1 sends server their Move
Server forwards player1's Move to player2 
Player2 processes the Move and responds with an Result to the server
Server forwards this Result back to player1
Player1 confirms with server that Result is received
Server switch the roles(status) of player1 and player2
Start next round
*/


/* Move: player1 -> server
After every move of each player,
the client sends Move data to the server in a buffer.
Then the client hangs until receiving some data from the server. 

The move data will be communicated between the server and 
client in the following array format: 
char move[] = {player, type, x, y, direction};

At the initial game stage, the client sends the client a 
data packet for each ship 
*/
#define SIZE_MOVE 5
#define PLAYER1 1
#define PLAYER2 2
#define SHIP_PLACEMENT 0
#define SEND_MISSLE 1
#define HORIZONTAL 0
#define VERTICAL 1
struct Move{
    int player; // PLAYER1 or PLAYER2
    int type;   // SHIP_PLACEMENT or SEND_MISSLE
    int x;      // x coordinate for the missle or the left most (smallest x coord) of ship placement
    int y;      // y coordinate for the missle or the top (smallest y coord) of ship placement
    int direction; // HORIZONTAL or VERTICAL
};



/*
The Update of each round will be communicated between the server and client in the 
following array format: 
char update[] = {missle_result};
*/
#define SIZE_RESULT 2
#define MISS 0
#define HIT 1
#define SUNK 2
#define GAMEOVER 3
#define RECEIVED 0
#define NOT_RECEIVED 1
struct Result{
    int recieved; // RECEIVED, NOT_RECEIVED
    int missle_result; // MISS, HIT, SUNK, or GAMEOVER
};


#define WIN 0
#define LOST 1

/* APIs to be defined
void opponent_move(type, x, y, direction)
calling this move would update your board based on your opponents move. 

void player_move(&buffer)
updates the game state based on your move. 

void start_game(buffer)
*/