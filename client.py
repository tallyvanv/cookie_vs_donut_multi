import pygame
from grid import Grid
import socket
import threading

import os

# window always appears in same place relative to upper-left corner (diff position from server)
os.environ['SDL_VIDEO_WINDOW_POS'] = '850, 100'

# create playing surface
surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Cookie vs. Donut')


# threading to prevent connection blocking the main thread
def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


# set up client

HOST = '10.242.147.136'  # The server's hostname or IP address
PORT = 5555  # The port used by the server

# 1: create socket object 2: arguments = address family(ipv4) & socket type(tcp), same as server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


def receive_data():
    # infinite while loop: don't receive data in closed connection, always check if new data coming in
    global turn
    while True:
        # block main thread, amount of bytes it can receive + decode byte string to regular string
        data = sock.recv(1024).decode()
        data = data.split('-')  # will create a list with data x, y, yourturn, playing
        x, y = int(data[0]), int(data[1])  # receive x and y as integer from data list
        if data[2] == "yourturn":
            turn = True
        if data[3] == 'False':
            grid.game_over = True  # when playing is false, game is over
        if grid.get_cell_value(x, y) == 0:
            # don't use current_player variable, pass player so client and server blit the same image
            grid.set_cell_value(x, y, "Cookie")
        print(data)


create_thread(receive_data)

# import grid object

grid = Grid()

# set game running to true
game_still_going = True

current_player = "Donut"
turn = False
playing = "True"

# execute while loop while game running, game stops running when player quits
while game_still_going:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_still_going = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            # index indicates which mouse button is being pressed ([0] = left, [1] = middle, [2] = right)
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    # convert screen coords into cell coords
                    # each cell is 200x200 rectangle so divide by 200 (always divide by dimensions cell)
                    # using integer division (//), we will get the integer coords of [0-2, 0-2]
                    grid.get_mouse(cellX, cellY, current_player)
                    if grid.game_over:
                        playing = False
                    send_data = f'{cellX}-{cellY}-{"yourturn"}-{playing}'.encode()
                    # on the client side we're using socket send method
                    sock.send(send_data)
                    # flip player
                    # use switch_player variable to make sure that we don't switch when clicking on non-empty cell
                    turn = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over = False
                playing = True

                # grid.print_grid()  # print grid row by row for debugging purposes

    # fill surface with black colour
    surface.fill((0, 0, 0))

    # invoke draw method from grid object onto surface
    grid.draw(surface)

    pygame.display.flip()
