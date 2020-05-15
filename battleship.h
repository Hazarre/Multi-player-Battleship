

/* Round procedure
Player1 sends server their Move
Server forwards player1's Move to player2 
Player2 processes the Move and responds with an Update to the server
Server forwards this Update back to player1
Player1 confirms with server that Update is completed
Server switch the roles(status) of player1 and player2
Start next round
*/


/*
After every move of each player,
the client sends Move data to the server in a buffer.
Then the client hangs until receiving some data from the server. 

The move data will be communicated between the server and 
client in the following array format: 
int move[] = {player, type, x, y, direction};

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



#define SIZE_RESULT 1
#define MISS 0
#define HIT 1
#define SUNK 2
#define GAMEOVER 3
/*
The Update of each round will be communicated between the server and client in the 
following array format: 
int update[] = {missle_result};
*/
struct Result{
    int missle_result; // MISS, HIT, SUNK, or GAMEOVER
};



