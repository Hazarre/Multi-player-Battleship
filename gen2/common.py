# game meta data
PORT = 8080
BUFFER_SIZE = 20

STATUS = {  'water': 0,
            'ship': 1,
            'miss':2,
            'hit':3}

STATE ={'setup':0,      # possible game states
        'fire':1,
        'gameover':2,
         }

MSG_TYPE = {'flag':'0', 'fire':'1', 'fire result': '1', 'ship placement': '2', 'under fire':'2'}
TYPE = MSG_TYPE

RESULT = {'hit':'1', 'miss':'0'}

FLAGS = {   'bad input': '0',
            'wait': '1',
            'my turn': '2',
            'placed a ship': '3',
            'win': '4',
            'lost': '5', 
        }

ORIENTATION = {'V': '1', 'H': '0', 'v': '1', 'h':'0'}

BOARD_SIZE, NUM_SHIPS, SHIP_SIZE  = 4, 1, 2
