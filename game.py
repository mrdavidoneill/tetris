from time import time

from locals import *
from screen import Screen
from piece import Piece
from landed import Grid
from music import Music
import random


def reset():
    """ Reset game state """
    score = 0
    speed = 0.5
    Screen.start_screen()
    Grid.start_grid()
    Music.play_bg_music()
    return score, speed

def read_best_score():
    """ Reads best score from file """
    with open("best_score.txt", "r") as file:
        best_score = file.read()
        return best_score

def write_best_score(score):
    """ Writes best score to file """
    with open("best_score.txt", "w") as file:
        file.write(str(score))

def random_shape():
    """ Return random shape """
    return random.choice(list(Piece.PIECES.keys()))

def create_pieces(shape=None):
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

def run():
    """ Starts the Screen, starts the Grid and makes new piece and next piece """
    FPS = 30
    fps_clock = pygame.time.Clock()
    POINTS = [0, 40, 100, 300, 1200]  # Points for multiple lines cleared
    HELD_KEY_THRESHOLD = 0.2

    score, speed = reset()
    best_score = read_best_score()
    piece, next_piece = create_pieces()

    Screen.display_top_info("Next shape:")  # Display "next shape:" text
    next_piece.draw_next()

    game_ended = False
    key_down_time = None
    key_down_event = None

    ##### Game loop #####
    done = False
    while not done:

        # If key held down
        if key_down_event:
            if time() - key_down_time > HELD_KEY_THRESHOLD:
                 piece.move(KEY_TO_DIR[key_down_event.key])

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
                break

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

        if done:
            break

        # Check if time to drop piece
        time_since_last_drop = time() - piece.time_last_dropped
        if time_since_last_drop > speed:
            piece.time_last_dropped = time()

            # Check if piece move is possible. If LANDED, check if completed rows, update score and best score
            if piece.move() == LANDED:
                completed_rows = Grid.check_complete()
                if completed_rows:
                    for row in completed_rows:
                        Grid.flash_row(row)
                        Screen.update()
                        Music.play_clear_line()
                        fps_clock.tick(5)   # Slow down screen for completed line graphic
                        Grid.remove_row(row)
                    score += POINTS[len(completed_rows)]
                    if score > int(best_score):
                        best_score = score
                Grid.draw_grid()                                        # Draws grid
                piece, next_piece = create_pieces(next_piece)
                key_down_time = None                                    # Don't allow keydown before new piece
                key_down_event = None                                   # Don't allow keydown before new piece

                # Check if piece can't move down
                if piece.can_move() == LANDED:
                    piece.draw()
                    game_ended = True

                Screen.draw_top_bar()                                   # Draws top bar
                Screen.display_top_info("Next shape:")                  # Writes "Next shape:"
                next_piece.draw_next()                                  # Draws next piece

                # Check if gameover, if so update the best_score.txt if necessary
                if game_ended:
                    if score == int(best_score):
                        write_best_score(score)

                    if gameover() == RESTART:
                        score, speed = reset()
                        game_ended = False
                        piece, next_piece = create_pieces()

                        Screen.display_top_info("Next shape:")  # Display "next shape:" text
                        next_piece.draw_next()
                    else:
                        done = True
                        break

        # Draw bottom bar with updated score
        Screen.draw_btm_bar()
        Screen.display_btm_info(f"Score: {score}  (Best score: {best_score})")  # Display score

        Screen.update()
        fps_clock.tick(FPS)

    pygame.quit()

def gameover():
    """ Checks for quit, or space bar which starts a new game.
        Displays gameover message over image of last lost position """

    Screen.display_msg("Press SPACE to play again")  # Displays instructions to restart game
    Screen.update()
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            return

        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                return RESTART






# ================ FOR TESTING PURPOSES ================ #

if __name__ == "__main__":
    run()


