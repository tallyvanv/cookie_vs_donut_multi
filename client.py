import pygame
from grid import Grid
import socket
import threading

import os


# window always appears in same place relative to upper-left corner
os.environ['SDL_VIDEO_WINDOW_POS'] = '400, 100'

# create playing surface
surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Cookie vs. Donut')


# threading to prevent connection blocking the main thread
def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


# set up client

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The port used by the server

# 1: create socket object 2: arguments = address family(ipv4) & socket type(tcp), same as server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))



# import grid object

grid = Grid()

# set game running to true
game_still_going = True

current_player = "Cookie"

# execute while loop while game running, game stops running when player quits
while game_still_going:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_still_going = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            # index indicates which mouse button is being pressed ([0] = left, [1] = middle, [2] = right)
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                # convert screen coords into cell coords
                # each cell is 200x200 rectangle so divide by 200 (always divide by dimensions cell)
                # using integer division (//), we will get the integer coords of [0-2, 0-2]
                grid.get_mouse(pos[0] // 200, pos[1] // 200, current_player)
                # flip player
                # use switch_player variable to make sure that we don't switch when clicking on non-empty cell
                if grid.switch_player:
                    if current_player == "Cookie":
                        current_player = "Donut"
                    else:
                        current_player = "Cookie"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over = False

                # grid.print_grid()  # print grid row by row for debugging purposes


# fill surface with black colour
    surface.fill((0, 0, 0))

# invoke draw method from grid object onto surface
    grid.draw(surface)

    pygame.display.flip()

# winner = None
#
#
#
#
# def display_board():
#     print("|" + board[0] + "|" + board[1] + "|" + board[2] + "|")
#     print("|" + board[3] + "|" + board[4] + "|" + board[5] + "|")
#     print("|" + board[6] + "|" + board[7] + "|" + board[8] + "|")
#
#
# def play_game():
#     display_board()
#

#
#     # The game has ended
#     if winner == "Cookie" or winner == "Donut":
#         print(winner + " won.")
#     elif winner is None:
#         print("Tie.")
#
#
# def handle_turn(player):
#     print(player + "'s turn")
#     position = input("Choose a position from 1-9: ")
#
#     # make sure that input is a number between 1-9
#
#     valid = False
#     while not valid:
#
#         while position not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
#             position = input("Invalid input. Choose a position from 1-9: ")
#
#         position = int(position) - 1
#
#         if board[position] == "-":
#             valid = True
#         else:
#             print("That spot's already taken, mate")
#
#     board[position] = player
#     display_board()
#
#
# def check_if_game_over():
#     check_for_winner()
#     check_if_tie()
#
#
# def check_for_winner():
#     # set global variable
#     global winner
#     # check rows
#     row_winner = check_rows()
#     # check columns
#     column_winner = check_columns()
#     # check diagonals
#     diagonal_winner = check_diagonals()
#     if row_winner:
#         # win
#         winner = row_winner
#     elif column_winner:
#         # win
#         winner = column_winner
#     elif diagonal_winner:
#         # win
#         winner = diagonal_winner
#     else:
#         # no win
#         winner = None
#     return
#
#
# def check_rows():
#     global game_still_going
#
#     row_1 = board[0] == board[1] == board[2] != "-"
#     row_2 = board[3] == board[4] == board[5] != "-"
#     row_3 = board[6] == board[7] == board[8] != "-"
#
#     # Game ends when row is full
#     if row_1 or row_2 or row_3:
#         game_still_going = False
#     # return winner (X or O)
#     if row_1:
#         return board[0]
#     elif row_2:
#         return board[3]
#     elif row_3:
#         return board[6]
#     return
#
#
# def check_columns():
#     global game_still_going
#
#     column_1 = board[0] == board[3] == board[6] != "-"
#     column_2 = board[1] == board[4] == board[7] != "-"
#     column_3 = board[2] == board[5] == board[8] != "-"
#
#     # Game ends when row is full
#     if column_1 or column_2 or column_3:
#         game_still_going = False
#     # return winner (X or O)
#     if column_1:
#         return board[0]
#     elif column_2:
#         return board[1]
#     elif column_3:
#         return board[2]
#     return
#
#
# def check_diagonals():
#     global game_still_going
#
#     diagonal_1 = board[0] == board[4] == board[8] != "-"
#     diagonal_2 = board[2] == board[4] == board[6] != "-"
#
#     # Game ends when row is full
#     if diagonal_1 or diagonal_2:
#         game_still_going = False
#     # return winner (X or O)
#     if diagonal_1:
#         return board[0]
#     elif diagonal_2:
#         return board[2]
#
#     return
#
#
# def check_if_tie():
#     global game_still_going
#
#     if "-" not in board:
#         game_still_going = False
#     return
#
#
# # flip between X and O
# def flip_player():
#     global current_player
#

#     return
#
#
# play_game()

# board

# display board

# play game

# check win
# check rows
# check columns
# check diagonals

# check tie

# flip player
