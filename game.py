from locals import *
from screen import Screen
from piece import Piece
from landed import Grid
import random

class Game:

    # Store best score
    with open("best_score.txt", "r") as file:
        best_score = file.read()

    starting_FPS = 3                  # Starting FPS used for resetting the game
    FPS = starting_FPS                # FPS  - option to speed up game
    fpsClock = pygame.time.Clock()    # Clock object
    POINTS = [0, 40, 100, 300, 1200]  # Points for multiple lines cleared

    def __init__(self):
        """ Initialises the new game with score of 0 and then calls the run method """
        self.score = 0
        self.run()

    def run(self):
        """ Initialises the Screen, calls Screen.display_score function and initialises a new snake and a new apple """

        Screen.start_screen()         # Start screen
        Grid.start_grid()             # Start grid

        piece = Piece(random.choice(list(Piece.PIECES.keys())))     # Create piece with random shape
        next_shape = random.choice(list(Piece.PIECES.keys()))       # Get a random shape for next piece
        Screen.display_top_info("Next shape:")                      # Display "next shape:" text
        next_piece = Piece(next_shape, "next")                      # Create a "next" piece
        next_piece.draw_next()                                      # Draw next piece on screen

        ##### Game loop #####
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # Arrow changes direction, piece moves towards direction and resets direction to DOWN
                elif event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        piece.set_direction(LEFT)
                        piece.move()
                        piece.set_direction(DOWN)
                        break
                    elif event.key == K_RIGHT:
                        piece.set_direction(RIGHT)
                        piece.move()
                        piece.set_direction(DOWN)
                        break
                    elif event.key == K_DOWN:
                        piece.move()
                        break
                    elif event.key == K_SPACE:
                        piece.rotate()
                        break

            # Check if piece move is possible. If LANDED, check if completed rows, update score and best score
            if piece.move() == LANDED:
                completed_rows = Grid.check_complete()
                if completed_rows:
                    for row in completed_rows:
                        Grid.flash_row(row)
                        Screen.update()
                        Game.fpsClock.tick(Game.FPS)
                        Grid.remove_row(row)
                    self.score += Game.POINTS[len(completed_rows)]
                    if self.score > int(Game.best_score):
                        Game.best_score = self.score

                Grid.draw_grid()                                        # Draws grid
                piece = Piece(next_shape)                               # Creates new piece
                next_shape = random.choice(list(Piece.PIECES.keys()))   # Creates new shape
                Screen.draw_top_bar()                                   # Draws top bar
                Screen.display_top_info("Next shape:")                  # Writes "Next shape:"
                next_piece = Piece(next_shape, "next")                  # Creates "next" piece
                next_piece.draw_next()                                  # Draws next piece

                # Check if gameover, if so update the best_score.txt if necessary
                if piece.gameover:
                    if self.score == int(Game.best_score):
                        with open("best_score.txt", "w") as file:
                            file.write(str(self.score))
                    Game.gameover()                                     # Run gameover() method

            # Draw bottom bar with updated score
            Screen.draw_btm_bar()
            Screen.display_btm_info(f"Score: {self.score}  (Best score: {Game.best_score})")  # Display score

            Screen.update()
            Game.fpsClock.tick(Game.FPS)

    @staticmethod
    def gameover():
        """ Checks for quit, or space bar which starts a new game.
            Displays gameover message over image of last lost position """
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        Game()                  # Restart game

            Screen.display_msg("Press SPACE to play again")       # Displays instructions to restart game
            Screen.update()
            Game.fpsClock.tick(Game.FPS)



# ================ FOR TESTING PURPOSES ================ #

if __name__ == "__main__":
    new_game = Game()


