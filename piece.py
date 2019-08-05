from locals import *
from screen import Screen
from landed import Grid
import random

class Piece:

    gridx_min = Screen.GRIDX_0
    gridx_max = Screen.GRIDX_MAX
    gridy_min = Screen.GRIDY_0
    gridy_max = Screen.GRIDY_MAX
    grid_size = Screen.GRID_SIZE

    # =========== PIECES =========== #
    PIECES = {
                I : {ROTATIONS : [
                        [[0, 0, 1, 0],
                         [0, 0, 1, 0],
                         [0, 0, 1, 0],
                         [0, 0, 1, 0]],
                        [[0, 0, 0, 0],
                         [1, 1, 1, 1],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]]
                        ],
                    COLOR: CYAN
                    },
                O : {ROTATIONS : [
                        [[0, 1, 1, 0],
                         [0, 1, 1, 0]]
                        ],
                    COLOR: YELLOW
                    },
                T : {ROTATIONS : [
                    [[0, 1, 0],
                     [1, 1, 1],
                     [0, 0, 0]],
                    [[0, 1, 0],
                     [0, 1, 1],
                     [0, 1, 0]],
                    [[0, 0, 0],
                     [1, 1, 1],
                     [0, 1, 0]],
                    [[0, 1, 0],
                     [1, 1, 0],
                     [0, 1, 0]],
                    ],
                    COLOR: PURPLE
                    },
                S : {ROTATIONS : [
                    [[0, 1, 1],
                     [1, 1, 0],
                     [0, 0, 0]],
                    [[0, 1, 0],
                     [0, 1, 1],
                     [0, 0, 1]],
                    [[0, 0, 0],
                     [0, 1, 1],
                     [1, 1, 0]],
                    [[1, 0, 0],
                     [1, 1, 0],
                     [0, 1, 0]],
                    ],
                    COLOR: GREEN
                    },
                Z : {ROTATIONS : [
                    [[1, 1, 0],
                     [0, 1, 1],
                     [0, 0, 0]],
                    [[0, 0, 1],
                     [0, 1, 1],
                     [0, 1, 0]],
                    [[0, 0, 0],
                     [1, 1, 0],
                     [0, 1, 1]],
                    [[0, 1, 0],
                     [1, 1, 0],
                     [1, 0, 0]],
                    ],
                    COLOR: RED
                    },
                L : {ROTATIONS : [
                    [[0, 1, 0],
                     [0, 1, 0],
                     [0, 1, 1]],
                    [[0, 0, 0],
                     [1, 1, 1],
                     [1, 0, 0]],
                    [[1, 1, 0],
                     [0, 1, 0],
                     [0, 1, 0]],
                    [[0, 0, 1],
                     [1, 1, 1],
                     [0, 0, 0]],
                ],
                    COLOR: ORANGE
                },
                J : {ROTATIONS : [
                    [[0, 1, 0],
                     [0, 1, 0],
                     [1, 1, 0]],
                    [[1, 0, 0],
                     [1, 1, 1],
                     [0, 0, 0]],
                    [[0, 1, 1],
                     [0, 1, 0],
                     [0, 1, 0]],
                    [[0, 0, 0],
                     [1, 1, 1],
                     [0, 0, 1]],
                ],
                    COLOR: BLUE
                },
    }


    def __init__(self, shape=None, next=False):
        """ Initialises new snake with colour of black, and a 3 block body.
            Direction set to left, """

        if not shape:
            self.shape = random.choice(list(Piece.PIECES.keys()))
        else:
            self.shape = shape

        self.gameover = False
        self.surface = Screen.surface
        self.rotation = 0
        self.body = Piece.PIECES[self.shape][ROTATIONS][self.rotation]
        self.color = Piece.PIECES[self.shape][COLOR]
        self.x = int((Piece.gridx_max - Piece.gridx_min) / 2 + Piece.gridx_min) - int(len(self.body[0]) / 2)
        self.y = Piece.gridy_min
        self.direction_x = 0
        self.direction_y = 1
        if not next:
            if self.can_move() == LANDED:
                self.draw()
                self.gameover = True
            else:
                self.draw()


    def draw(self):
        """ Draws piece on display surface """
        block_y = 0
        for row in self.body:
            block_x = 0
            for cell in row:
                if cell:
                    block_position = ((block_x * Screen.GRID_SIZE) + (self.x * Screen.GRID_SIZE),
                                      (block_y * Screen.GRID_SIZE) + (self.y * Screen.GRID_SIZE),
                                      Screen.GRID_SIZE,
                                      Screen.GRID_SIZE)
                    pygame.draw.rect(self.surface, self.color, block_position)
                    pygame.draw.rect(self.surface, BLACK, block_position, 1)


                block_x += 1
            block_y += 1

    def draw_next(self):
        """ Draws next piece at top right """
        block_y = 0
        for row in self.body:
            block_x = 0
            for cell in row:
                if cell:
                    block_position = ((block_x * Screen.GRID_SIZE) + (Screen.WINDOW_WIDTH / 1.5),
                                      (block_y * Screen.GRID_SIZE) + (1 * Screen.GRID_SIZE),
                                      Screen.GRID_SIZE,
                                      Screen.GRID_SIZE)
                    pygame.draw.rect(self.surface, self.color, block_position)
                    pygame.draw.rect(self.surface, BLACK, block_position, 1)
                block_x += 1
            block_y += 1


    def erase(self):
        """ Erases block from display surface """
        block_y = 0
        for row in self.body:
            block_x = 0
            for cell in row:
                if cell:
                    block_position = ((block_x * Screen.GRID_SIZE) + (self.x * Screen.GRID_SIZE),
                                      (block_y * Screen.GRID_SIZE) + (self.y * Screen.GRID_SIZE),
                                      Screen.GRID_SIZE,
                                      Screen.GRID_SIZE)
                    pygame.draw.rect(self.surface, Screen.BG_COLOR, block_position)
                block_x += 1
            block_y += 1

    def move(self):
        """ Erases piece from display surface, updates y position.
            Calculates if it's outside the screen, or side hits landed block and if so: returns False,
            Else if bottom hits landed block return "landed"
            Else returns "possible"
            Then draws piece in new position. """

        if self.can_move() == POSSIBLE:
            self.erase()
            self.x += self.direction_x
            self.y += self.direction_y
            self.draw()

        elif self.can_move() == LANDED:
            Grid.add_piece(self)
            return LANDED


    def can_move(self):
        """ Checks if move is possible and returns True is yes, else returns False """

        possible_x = self.x + self.direction_x
        possible_y = self.y + self.direction_y
        block_y = 0
        for row in self.body:
            block_x = 0
            for cell in row:
                if cell:
                    # Check if at L/R edge of grid
                    if block_x + possible_x < Piece.gridx_min or block_x + possible_x == Piece.gridx_max:
                        return False
                    # Check if at bottom of grid pieces are to left or right
                    elif block_y + possible_y == Piece.gridy_max :
                        return LANDED
                    # Check if piece underneath and not moving to side
                    elif Grid.landed_pieces[block_y + possible_y - Screen.GRIDY_0][block_x + possible_x - Screen.GRIDX_0] \
                            and self.direction_x == 0:
                        return LANDED
                    # Check if no piece underneath and moving to side
                    elif Grid.landed_pieces[block_y + possible_y - Screen.GRIDY_0][block_x + possible_x - Screen.GRIDX_0]:
                        return False
                block_x += 1
            block_y += 1
        return POSSIBLE

    def can_rotate(self):
        """ Checks if move is possible and returns True is yes, else returns False """

        possible_rotation = (self.rotation + 1) % len(Piece.PIECES[self.shape][ROTATIONS])
        possible_body = Piece.PIECES[self.shape][ROTATIONS][possible_rotation]

        block_y = 0
        for row in possible_body:
            block_x = 0
            for cell in row:
                if cell:
                    # If too close to left for rotation, bounceback
                    if block_x + self.x < Piece.gridx_min:
                        self.erase()
                        self.x += 1
                        return self.can_rotate()
                    # If too close to right for rotation, bounceback
                    if block_x + self.x == Piece.gridx_max:
                        self.erase()
                        self.x -= 1
                        return self.can_rotate()
                    elif block_y + self.y == Piece.gridy_max or \
                            Grid.landed_pieces[block_y + self.y - Screen.GRIDY_0][block_x + self.x - Screen.GRIDX_0]:
                        return LANDED
                block_x += 1
            block_y += 1
        return POSSIBLE

    def rotate(self):
        """ Checks if a rotation is possible by calling can_rotate() and if so, rotates """
        if self.can_rotate() == POSSIBLE:
            self.erase()
            self.rotation = (self.rotation + 1) % len(Piece.PIECES[self.shape][ROTATIONS])
            self.body = Piece.PIECES[self.shape][ROTATIONS][self.rotation]
            self.draw()

    def stop(self):
        """ Stops piece by setting it's X and Y direction to 0 """
        self.direction_x = 0
        self.direction_y = 0

    def set_direction(self, dir):
        """ Sets its direction to given argument of one of:
            UP, DOWN, RIGHT, LEFT """
        if dir == DOWN:
            self.direction_x = 0
            self.direction_y = 1
        elif dir == RIGHT:
            self.direction_x = 1
            self.direction_y = 0
        elif dir == LEFT:
            self.direction_x = -1
            self.direction_y = 0

    def get_direction(self):
        """ Returns the direction the snake is headed """
        if self.direction_x == 1:
            return RIGHT
        elif self.direction_x == -1:
            return  LEFT
        elif self.direction_y == 1:
            return DOWN


# ================ FOR TESTING PURPOSES ================ #

if __name__ == "__main__":

    fpsClock = pygame.time.Clock()

    # Start screen, grid and create new piece
    Screen.start_screen()
    Grid.start_grid()
    piece = Piece()

    # Game loop #
    while True:
        # Check for exit
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # If new piece can't move:
        if piece.move() == LANDED:
            piece = Piece()
            if piece.gameover:
                break
        else:
            piece.rotate()

        Screen.update()
        fpsClock.tick(3)
