from locals import *
from screen import Screen

class Grid:

    COLUMNS = Screen.SCREEN_SIZE[0]
    ROWS = Screen.SCREEN_SIZE[1]
    landed_pieces = []

    @classmethod
    def start_grid(cls):
        """ Creates the playing grid matrix """
        cls.landed_pieces = []
        for row in range(Grid.ROWS):
            cls.landed_pieces.append(cls.create_row())

    @classmethod
    def create_row(cls):
        """ Create an empty row """
        empty_row = []
        for cell in range(Grid.COLUMNS):
            empty_row.append(0)
        return empty_row

    @classmethod
    def print_grid(cls):
        """ Prints formatted playing grid to screen """
        display = ""
        for row in cls.landed_pieces:
            for cell in row:
                display += str(cell) + " "
            display += "\n"
        print(display)

    @classmethod
    def add_piece(cls, piece):
        """ Adds a piece to Grid.landed_pieces """
        block_y = 0
        for row in piece.body:
            block_x = 0
            for cell in row:
                if cell:
                    cls.landed_pieces[piece.y + block_y - Screen.GRIDY_0][piece.x + block_x - Screen.GRIDX_0] = piece.shape
                block_x += 1
            block_y += 1

    @classmethod
    def check_complete(cls):
        """ Checks if row has been completed """
        complete_rows = []
        row_number = 0
        for row in cls.landed_pieces:
            complete = True
            for cell in row:
                if not cell:
                    complete = False
                    break
            if complete:
                complete_rows.append(row_number)
            row_number += 1
        return complete_rows

    @classmethod
    def remove_row(cls, row):
        """ Removes a specified row from the landed grid and adds an empty row to the top """
        cls.landed_pieces.pop(row)
        cls.landed_pieces.insert(0, cls.create_row())

    @classmethod
    def draw_grid(cls):
        """ Draws entire grid to display surface """

        from piece import Piece             # Need to import to get color, but circle import

        block_y = 0
        for row in cls.landed_pieces:
            block_x = 0
            for cell in row:
                block_position = ((block_x * Screen.GRID_SIZE) + (Screen.GRIDX_0 * Screen.GRID_SIZE),
                                  (block_y * Screen.GRID_SIZE) + (Screen.GRIDY_0 * Screen.GRID_SIZE),
                                  Screen.GRID_SIZE,
                                  Screen.GRID_SIZE)
                if cell:
                    pygame.draw.rect(Screen.surface, Piece.PIECES[cell][COLOR], block_position)
                else:
                    pygame.draw.rect(Screen.surface, Screen.BG_COLOR, block_position)
                block_x += 1
            block_y += 1


# ================ FOR TESTING PURPOSES ================ #

if __name__ == "__main__":
    Grid.start_grid()
    Grid.print_grid()
