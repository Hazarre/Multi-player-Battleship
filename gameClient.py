#!/usr/bin/env python3

"""CMSC 226 Final project: Ansel, Henning, Henry.

Client side game code for networked battleship game.
Keeps track of game state, taking updates from server,
and sending out moves on players turn.

Author: Ansel Tessier (at9088@bard.edu)
"""

import sys
import numpy
import socket


HOST = '127.0.0.1' ## NOTE: this is using localhost for dev, must change
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def make_move():
    ## TODO: take user input and send it to server
    target = bytes(input("Enter Coordinates:"),'utf-8')
    s.sendall(target)

def recive_update():
    # TODO: listen to server and update local map acordingly

    update = s.recv(1024)

def draw_board():
    print("todo")




"""main fruntion calls game and server functionality"""
def main():
    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s.connect((HOST, PORT))
        #s.sendall(make_move())
        #data = s.recv(1024)
    while 1:
        make_move()
        recive_update()




if __name__ == "__main__":
    main()
