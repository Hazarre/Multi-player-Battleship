#!/usr/bin/env python3

"""CMSC 226 Final project: Ansel, Henning, Henry.

Client side game code for networked battleship game.
Keeps track of game state, taking updates from server,
and sending out moves on players turn.
"""

import threading
import numpy
import socket
import curses
import sys,os

#seting up sockets
HOST = '127.0.0.1' ## NOTE: this is using localhost for dev, must change
PORT = 65432
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
#s.setblocking(0)

#setting up threading
c = threading.Condition()

#seting up curses wrapper
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

#global vars shared between threads
enemyboard = numpy.zeros((10,10), dtype=None, order='c')
myboard = numpy.zeros((10,10), dtype=None, order='c')
threadflag = 0 #threading flag
gameflag = 0
game_play = False
last_shot = (-1,-1) #cords and bool hit (0=false)
state = 'setup'

flagdict = {
    1 : "Wait your turn",
    2 : "Waiting for other player to place ships",
    3 : "Other player ready",
    4 : "placed a ship", #see communications.txt
    5 : "Repeated fire",
    6 : "GAME OVER"#see communications.txt
}


"""listener class makes a thread that listens for messages from the server and updates
    relivent vars
"""
class listener(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global enemyboard
        global myboard
        global game_play
        global state
        global gameflag
        global threadflag
        global last_shot
        global s

        while game_play:
            c.acquire()
            if threadflag == 0:
                message = s.recv(4096)
                ## TODO: parse message and ubate relivent vars.
                #if bool, this is an incoming fire message
                message = [int(i) for i in message.split(' ')]
                if(message[0] == 0):
                    gameflag = flagdict.get(message[1])
                elif(message[0] == 1):
                    if(message[1] == 0):
                        enemyboard[last_shot[2]][last_shot[1]] = 0
                    else:
                        enemyboard[last_shot[2]][last_shot[1]] = 2
                elif(message[0] == 2):
                    if(myboard[message[1]][message[2]] == 1):
                        myboard[message[1]][message[2]] == 2

                threadflag = 1
                c.notify_all()
            else:
                c.wait()
            c.release()

"""game_core class makes a thread that deals with all local game logic
   and rendering."""
class game_core(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        curses.wrapper(self.display)

        #while game_play:
        #    c.acquire()
        #    if threadflag == 1:
        #        # TODO: migrate exsisting code here
        #        threadflag == 0
        #        c.notify_all()
        #    else:
        #        c.wait()
        #    c.release()



    #renders game to terminal
    def display(self, stdscr):

        global enemyboard
        global myboard
        global game_play
        global gameflag
        global threadflag
        global last_shot
        global s

        if(game_play == False):
            game_play = True
            #s.sendall((bytes(,'utf-8'))

        self.k = 0
        self.cursor_x = 0
        self.cursor_y = 0
        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()
        # Start colors in curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        # Loop where k is the last character pressed
        while (self.k != ord('q')):

            #updating instance vars from listener theread
        #    if threadflag == 1:
                # TODO: migrate exsisting code here

        #        threadflag == 0
        #        c.notify_all()
        #    else:
        #        c.wait()
        #    c.release()

            # Initialization
            stdscr.clear()
            self.height, self.width = stdscr.getmaxyx()

            if self.k == curses.KEY_DOWN:
                self.cursor_y = self.cursor_y + 2
            elif self.k == curses.KEY_UP:
                self.cursor_y = self.cursor_y - 2
            elif self.k == curses.KEY_RIGHT:
                self.cursor_x = self.cursor_x + 4
            elif self.k == curses.KEY_LEFT:
                self.cursor_x = self.cursor_x - 4

            self.cursor_x = max(0, self.cursor_x)
            self.cursor_x = min(self.width-1, self.cursor_x)
            self.cursor_y = max(0, self.cursor_y)
            self.cursor_y = min(self.height-1, self.cursor_y)

            if self.k == ord(' '):
                mark = '1 '
                xsend = str(self.cursor_x//4)
                ysend = str(self.cursor_y//2)
                sendmsg = mark + xsend + ' ' + ysend
                s.sendall(bytes(sendmsg,'utf-8'))
                print(sendmsg)
                last_shot = (self.cursor_x//4, self.cursor_y//2)

            #status bar
            self.statusbarstr = "Press 'q' to exit | Target with arrow keys, fire with space | Target: {}, {}".format(self.cursor_x//4, self.cursor_y//2)
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(self.height-1, 0, self.statusbarstr)
            stdscr.addstr(self.height-1, len(self.statusbarstr), " " * (self.width - len(self.statusbarstr) - 1))
            stdscr.attroff(curses.color_pair(3))

            stdscr.attron(curses.A_BOLD)

            #c.acquire()
            #if(threadflag == 1):
            for i in range(0,9): #rendering boards
                for j in range(0,9):
                    try:
                        if(enemyboard[i][j] == 0): #drawing water
                            stdscr.attron(curses.color_pair(1))
                            stdscr.addch(i*2, j*4, 'o')
                            stdscr.attroff(curses.color_pair(1))
                        elif(enemyboard[i][j] == 1): #drawing unhit ship
                            stdscr.attron(curses.color_pair(3))
                            stdscr.addch(i*2, j*4, 'x')
                            stdscr.attroff(curses.color_pair(3))
                        elif(enemyboard[i][j] == 2): #drawing hit ship
                            stdscr.attron(curses.color_pair(2))
                            stdscr.addch(i*2, j*4, 'x')
                            stdscr.attroff(curses.color_pair(2))

                        if(myboard[i][j] == 0):
                            stdscr.attron(curses.color_pair(1))
                            stdscr.addch((i+10)*2, j*4, ord('o'))
                            stdscr.attroff(curses.color_pair(1))
                        elif(myboard[i][j] == 1):
                            stdscr.attron(curses.color_pair(3))
                            stdscr.addch((i+10)*2, j*4, 'x')
                            stdscr.attroff(curses.color_pair(3))
                        elif(myboard[i][j] == 2):
                            stdscr.attron(curses.color_pair(2))
                            stdscr.addch((i+10)*2, j*4, 'x')
                            stdscr.attroff(curses.color_pair(2))

                    except(curses.error):
                        pass
            #else:
            #    c.wait()
            #c.release()

            stdscr.attroff(curses.A_BOLD)

            stdscr.move(self.cursor_y, self.cursor_x)
            # Refresh the screen
            stdscr.refresh()

            # Wait for next input
            self.k = stdscr.getch()





"""main fruntion calls game and server functionality"""
def main():
    l = listener("listener_thread")
    g = game_core("game_thread")
    l.start()
    g.start()
    l.join()
    g.join()


if __name__ == "__main__":
    main()
