import os
from time import sleep
import random


def display_title():
    """ Clears the terminal, then prints the title."""
    os.system('cls')
    print('')
    print("*********************")
    print("**** TIC TAC TOE ****")
    print("*********************")


def check_pos(board, x, y):
    """ Checks the position the user input, if there isn't anything in that pos then it returns true."""
    if board[int(x)][int(y)] == 'X' or board[int(x)][int(y)] == 'O':
        return False
    else:
        return True


def check_player_pos(board, x, y):
    """ Used for finding player moves on the board. Returns true if found"""
    if 0 <= int(x) <= 2 and 0 <= int(y) <= 2:
        if board[int(x)][int(y)] == 'X':
            return True


def check_bot_pos(board, x, y):
    """ Used for finding bot moves on the board. Returns true if found"""
    if 0 <= int(x) <= 2 and 0 <= int(y) <= 2:
        if board[int(x)][int(y)] == 'O':
            return True


def check_win_player(board):
    """ Finds player positions and checks the columns and rows around to
    see if the player has three in a row"""
    for row in range(0, 3):
        for col in range(0, 3):
            # First Check
            if check_player_pos(board, row, col):
                # Second checks
                if check_player_pos(board, row + 1, col):
                    # Third Check
                    if check_player_pos(board, row + 2, col):
                        return True
                if check_player_pos(board, row - 1, col):
                    if check_player_pos(board, row - 2, col):
                        return True
                if check_player_pos(board, row, col + 1):
                    if check_player_pos(board, row, col + 2):
                        return True
                if check_player_pos(board, row, col - 1):
                    if check_player_pos(board, row, col - 2):
                        return True
                if check_player_pos(board, row + 1, col + 1):
                    if check_player_pos(board, row + 2, col + 2):
                        return True
                if check_player_pos(board, row - 1, col + 1):
                    if check_player_pos(board, row - 2, col + 2):
                        return True
    return False


def check_win_bot(board):
    """ Finds bot positions and checks the columns and rows around to
    see if the bot has three in a row"""
    for row in range(0, 3):
        for col in range(0, 3):
            # First Check
            if check_bot_pos(board, row, col):
                # Second checks
                if check_bot_pos(board, row + 1, col):
                    # Third Check
                    if check_bot_pos(board, row + 2, col):
                        return True
                if check_bot_pos(board, row - 1, col):
                    if check_bot_pos(board, row - 2, col):
                        return True
                if check_bot_pos(board, row, col + 1):
                    if check_bot_pos(board, row, col + 2):
                        return True
                if check_bot_pos(board, row, col - 1):
                    if check_bot_pos(board, row, col - 2):
                        return True
                if check_bot_pos(board, row + 1, col + 1):
                    if check_bot_pos(board, row + 2, col + 2):
                        return True
                if check_bot_pos(board, row - 1, col + 1):
                    if check_bot_pos(board, row - 2, col + 2):
                        return True
    return False


def create_board():
    """ Empty 3x3 board is created and returned."""
    row1 = []
    row2 = []
    row3 = []

    pos_list = [row1, row2, row3]

    for row in range(0, 3):
        for col in range(0, 3):
            if row == 0:
                row1.append(' ')
            elif row == 1:
                row2.append(' ')
            elif row == 2:
                row3.append(' ')
    return pos_list


def show_board(board):
    """ Prints the board."""
    print("   c0  c1  c2    (rows=r, columns=c)")
    for row in range(0, 3):
        num = 0
        print("r" + str(row) + ' ' + board[row][0] +
              " | " + board[row][1] + " | " + board[row][2])
        if row < 2:
            print("   _________")


def user_play(board):
    """ Gets input from user for positioning their move."""
    play_made = False
    while not play_made:
        display_title()
        show_board(board)
        x = input('Which row will you choose? (0 through 2): ')
        if x == 'quit':
            return False
        y = input('Which column will you choose? (0 through 2): ')
        if y == 'quit':
            return False
        if check_pos(board, x, y):
            player_update(board, x, y)
            play_made = True
        else:
            print("Choose a new spot!")
            sleep(1)


def bot_play(board):
    """ As basic as an AI can get :), random moves."""
    play_made = False
    while not play_made:
        rand_num1 = random.randint(0, 2)
        rand_num2 = random.randint(0, 2)
        if check_pos(board, rand_num1, rand_num2):
            bot_update(board, rand_num1, rand_num2)
            play_made = True


def player_update(board, x, y):
    """ Plots the players position on the board."""
    board[int(x)][int(y)] = 'X'


def bot_update(board, x, y):
    """ Plots the bots position on the board."""
    board[int(x)][int(y)] = 'O'
