from time import time

from locals import *
from screen import Screen
from piece import Piece
from landed import Grid
from music import Music
import random

class Game:

    FPS = 30
    fpsClock = pygame.time.Clock()
    POINTS = [0, 40, 100, 300, 1200]  # Points for multiple lines cleared

    def __init__(self):
        """ Initialises the new game with score of 0 and then calls the run method """
        self.score, self.speed = self.reset()
        self.best_score = self.read_best_score()
        self.run()

    def reset(self):
        """ Reset game state """
        score = 0
        speed = 0.5
        Screen.start_screen()
        Grid.start_grid()
        Music.play_bg_music()
        return score, speed

    def read_best_score(self):
        """ Reads best score from file """
        with open("best_score.txt", "r") as file:
            best_score = file.read()
            return best_score

    def write_best_score(self, score):
        """ Writes best score to file """
        with open("best_score.txt", "w") as file:
            file.write(str(score))


    def random_shape(self):
        """ Return random shape """
        return random.choice(list(Piece.PIECES.keys()))

    def create_pieces(self, shape=None):
        """ Creates piece and next piece """
        if not shape:
            shape = random.choice(list(Piece.PIECES.keys()))
            piece = Piece(shape)
            piece.time_last_dropped = time()
        else:
            piece = shape
        next_shape = random.choice(list(Piece.PIECES.keys()))
        next_piece = Piece(next_shape, "next")
        next_piece.time_last_dropped = time()
        return piece, next_piece

    def run(self):
        """ Starts the Screen, starts the Grid and makes new piece and next piece """
        self.reset()


        piece, next_piece = self.create_pieces()

        Screen.display_top_info("Next shape:")  # Display "next shape:" text
        next_piece.draw_next()
        key_down_time = None
        key_down_event = None

        ##### Game loop #####
        while True:

            # If key held down
            if key_down_event:
                if time() - key_down_time > 0.2:
                     piece.move(KEY_TO_DIR[key_down_event.key])

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # Arrow changes direction, piece moves towards direction and resets direction to DOWN
                if event.type == KEYDOWN:
                    if event.key in KEY_TO_DIR:
                        key_down_time = time()
                        key_down_event = event
                        piece.move(KEY_TO_DIR[event.key])
                    elif event.key == K_SPACE:
                        piece.rotate()

                elif event.type == KEYUP:
                    key_down_time = None
                    key_down_event = None


            # Check if time to drop piece
            time_since_last_drop = time() - piece.time_last_dropped
            if time_since_last_drop > self.speed:
                piece.time_last_dropped = time()

                # Check if piece move is possible. If LANDED, check if completed rows, update score and best score
                if piece.move() == LANDED:
                    completed_rows = Grid.check_complete()
                    if completed_rows:
                        for row in completed_rows:
                            Grid.flash_row(row)
                            Screen.update()
                            Music.play_clear_line()
                            Game.fpsClock.tick(5)   # Slow down screen for completed line graphic
                            Grid.remove_row(row)
                        self.score += Game.POINTS[len(completed_rows)]
                        if self.score > int(self.best_score):
                            self.best_score = self.score
                    Grid.draw_grid()                                        # Draws grid
                    piece, next_piece = self.create_pieces(next_piece)
                    key_down_time = None                                    # Don't allow keydown before new piece
                    key_down_event = None                                   # Don't allow keydown before new piece

                    # Check if piece can't move down
                    if piece.can_move() == LANDED:
                        piece.draw()
                        piece.gameover = True

                    Screen.draw_top_bar()                                   # Draws top bar
                    Screen.display_top_info("Next shape:")                  # Writes "Next shape:"
                    next_piece.draw_next()                                  # Draws next piece

                    # Check if gameover, if so update the best_score.txt if necessary
                    if piece.gameover:
                        if self.score == int(self.best_score):
                            self.store_best_score(self.score)
                        self.gameover()                                     # Run gameover() method

            # Draw bottom bar with updated score
            Screen.draw_btm_bar()
            Screen.display_btm_info(f"Score: {self.score}  (Best score: {self.best_score})")  # Display score

            Screen.update()
            Game.fpsClock.tick(Game.FPS)

    def gameover(self):
        """ Checks for quit, or space bar which starts a new game.
            Displays gameover message over image of last lost position """
        while True:
            event = pygame.event.wait()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.reset()
                    return

            Screen.display_msg("Press SPACE to play again")       # Displays instructions to restart game
            Screen.update()
            Game.fpsClock.tick(Game.FPS)



# ================ FOR TESTING PURPOSES ================ #

if __name__ == "__main__":
    new_game = Game()


