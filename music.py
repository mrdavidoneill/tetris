from locals import *
class Music:

    clear_line = pygame.mixer.Sound("clear.wav")

    @staticmethod
    def play_bg_music(rep=-1):
        pygame.mixer.music.load("tetris.mp3")
        pygame.mixer.music.play(rep)

    @classmethod
    def play_clear_line(cls):
        cls.clear_line.play()