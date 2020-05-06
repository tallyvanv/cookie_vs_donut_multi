import pygame

import os

cookie = pygame.image.load(os.path.join('res', 'cookie.png'))
donut = pygame.image.load(os.path.join('res', 'donut.png'))


class Grid:
    def __init__(self):
        # define grid with x and y coordinates
        # first two: horizontal lines, final two: vertical lines
        # drawn in tuples because immutable grid
        self.grid_lines = [((0, 200), (600, 200)),
                           ((0, 400), (600, 400)),
                           ((200, 0), (200, 600)),
                           ((400, 0), (400, 600))]
        # create the matrix, for every y, create 3 x-es and return value of zero
        # [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.grid = [[0 for x in range(3)] for y in range(3)]
        self.switch_player = True
        # search in directions N        NW          W       SW      S       SE      E       NE
        self.search_dirs = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.game_over = False

    # actually draw the lines
    def draw(self, surface):
        for line in self.grid_lines:
            # draw: surface, tuple of colours, lines and line thickness
            pygame.draw.line(surface, (200, 200, 200), line[0], line[1], 2)
        # 2D grid so nested for loop
        # outer loop goes through each element of the main list
        for y in range(len(self.grid)):
            # go through inner list
            for x in range(len(self.grid[y])):
                # project cookie onto cell if player is x, 200x200 relative to left upper corner cell
                if self.get_cell_value(x, y) == "X":
                    surface.blit(cookie, (x * 200, y * 200))
                # project donut onto cell if player is o
                if self.get_cell_value(x, y) == "O":
                    surface.blit(donut, (x * 200, y * 200))

    def get_cell_value(self, x, y):
        return self.grid[y][x]  # row and column position

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    # get position of mouse and cet cell accordingly
    def get_mouse(self, x, y, current_player):
        # only execute inner if statement if cell is empty
        # use switch_player variable to make sure that we don't switch when clicking on non-empty cell
        if self.get_cell_value(x, y) == 0:
            self.switch_player = True
            if current_player == "X":
                self.set_cell_value(x, y, "X")
                self.check_grid(x, y, current_player)
            elif current_player == "O":
                self.set_cell_value(x, y, "O")
                self.check_grid(x, y, current_player)
        else:
            self.switch_player = False

    # prevent IndexError: list index out of range
    def is_within_bounds(self, x, y):
        return 0 <= x < 3 and 0 <= y < 3  # check if x and y are within bounds of grind

    def check_grid(self, x, y, player):
        count = 1  # method executed after play, so there will be one item on the grid
        # the enumerate function loops over the dirs defined in init
        # this will return the index of the dirs and numbers inside the tuples as defined above
        for index, (dirx, diry) in enumerate(self.search_dirs):
            # check for matches in all directions: valid cell? and same player?
            if self.is_within_bounds(x+dirx, y+diry) and self.get_cell_value(x+dirx, y+diry) == player:
                # count consecutive matches
                count += 1
                # coordinates of match
                xx = x + dirx
                yy = y + diry
                # check consecutive match, does it have another consecutive match?
                if self.is_within_bounds(xx+dirx, yy+diry) and self.get_cell_value(xx+dirx, yy+diry) == player:
                    # count matches
                    count += 1
                    # when 3 next to each other: break
                    if count == 3:
                        break
                if count < 3:
                    new_dir = 0
                    # mapping the indeces to opposite direction
                    # Only consecutive matches counted
                    if index == 0:
                        new_dir = self.search_dirs[4]  # N to S
                    elif index == 1:
                        new_dir = self.search_dirs[5]  # NW to SE
                    elif index == 2:
                        new_dir = self.search_dirs[6]  # W to E
                    elif index == 3:
                        new_dir = self.search_dirs[7]  # SW to NE
                    elif index == 4:
                        new_dir = self.search_dirs[0]  # S to N
                    elif index == 5:
                        new_dir = self.search_dirs[1]  # SE to NW
                    elif index == 6:
                        new_dir = self.search_dirs[2]  # E to W
                    elif index == 7:
                        new_dir = self.search_dirs[3]  # NE to SW

                    if self.is_within_bounds(x + new_dir[0], y + new_dir[1]) and self.get_cell_value(x + new_dir[0], y + new_dir[1]) == player:
                        count += 1
                        if count == 3:
                            break
                    else:
                        count = 1
        if count == 3:
            print(player, 'wins!')
            self.game_over = True
        else:
            self.game_over = self.is_grid_full()

    def is_grid_full(self):
        for row in self.grid:
            for value in row:
                if value == 0:
                    return False
        return True

    def clear_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.set_cell_value(x, y, 0)

    # # print for debugging
    # def print_grid(self):
    #     for row in self.grid:
    #         print(row)
