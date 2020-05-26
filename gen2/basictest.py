from battleship import*


from time import sleep

# Test 1
g = Game()
g.update_game("0 0 v",0)
print(MESSAGE_DECODING[g.players[0].message])
g.update_game("0 0 v",1)
print(MESSAGE_DECODING[g.players[1].message])
g.update_game("1 0 v",0)
g.update_game("1 0 v",1)
g.update_game("2 0 v",0)
g.update_game("2 0 v",1)

for i in range(3):
    for j in range(3):
        g.update_game("%d %d"%(i,j),0)
        g.update_game("%d %d"%(i,j),1)
        print(MESSAGE_DECODING[g.players[0].message], "player1")
        print(MESSAGE_DECODING[g.players[1].message], "player2")


#Test 2
# while True:
#     print("player1's turn")
#     mes = g.get_input_prompt()
#     g.update_game(mes,0)

#     print("player2's turn")
#     mes = g.get_input_prompt()
#     print(g.update_game(mes,1))
    


# MESSAGE_DECODING = ['input_error','placement_success','target_hit','target_miss','you_loss']
# MESSAGE_ENCODING = {}
# for i in range(len(MESSAGE_DECODING)):
#     MESSAGE_ENCODING[MESSAGE_DECODING[i]] = i 

# print(MESSAGE_ENCODING)