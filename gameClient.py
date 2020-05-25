#!/usr/bin/env python3

"""CMSC 226 Final project: Ansel, Henning, Henry.

Client side game code for networked battleship game.
Keeps track of game state, taking updates from server,
and sending out moves on players turn.

Author: Ansel Tessier (at9088@bard.edu)
"""


import numpy
import socket
import curses
import sys,os

#seting up sockets
HOST = '127.0.0.1' ## NOTE: this is using localhost for dev, must change
PORT = 65432
setup = True
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.setblocking(0)

#seting up curses wrapper
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

#manually setting up boards for testing
enemyboard = numpy.zeros((10,10), dtype=None, order='c')
myboard = numpy.zeros((10,10), dtype=None, order='c')



#sends your move to the server as a byte object
def make_move(pos):
    target = bytes(str(pos),'utf-8')
    s.sendall(target)

# TODO: s.recv dosen't play well with sockets
def recive_update():
    myboard = s.recv(4096)
    #if(update = "setup")

    # TODO: look for message that switches game state
    #may need to convert update from bytes to numpyarray

#renders game to terminal
def draw_board(stdscr):
    print("here")
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 2
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 2
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 4
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 4

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        if k == ord(' '):
            make_move((cursor_x//4, cursor_y//2))

        #status bar
        statusbarstr = "Press 'q' to exit | Target with arrow keys, fire with space | Target: {}, {}".format(cursor_x//4, cursor_y//2)
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        stdscr.attron(curses.A_BOLD)
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

        stdscr.attroff(curses.A_BOLD)

        stdscr.move(cursor_y, cursor_x)
        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

        #recive_update()



"""main fruntion calls game and server functionality"""
def main():
    curses.wrapper(draw_board)


if __name__ == "__main__":
    main()
