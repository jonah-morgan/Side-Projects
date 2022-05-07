
from time import sleep
from ttt_functions import *


# MAIN


run = True
while run:
    game_board = create_board()
    display_title()
    choice = input("\n[1] Play New Game\n[2] Quit\nAnswer: ")
    if choice == '1':
        play = True
        while play:
            user_play(game_board)
            if check_win_player(game_board):
                display_title()
                show_board(game_board)
                print('Congrats! You Won!')
                sleep(1)
                print('GAME OVER...')
                sleep(2)
                break
            bot_play(game_board)
            if check_win_bot(game_board):
                display_title()
                show_board(game_board)
                print('The Bot Wins! GAME OVER...')
                sleep(1)
                print('GAME OVER...')
                sleep(2)
                break
    elif choice == '2':
        run = False
        print("Goodbye..")
        sleep(.5)


# END MAIN
