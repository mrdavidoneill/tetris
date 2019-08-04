from locals import *

class Screen:

    ######## USER CHANGEABLE DATA ########

    S_TITLE = "Snake"  # Window title
    SCREEN_SIZE = (10, 20)  # Playing area in grid cells
    GRID_SIZE = 30          # Grid size in pixels
    BG_COLOR = GREY         # Playing area background colour
    T_BG_COLOR = R_BG_COLOR = B_BG_COLOR = L_BG_COLOR = BLACK   # Side panels background colour
    T_SIZE, R_SIZE, B_SIZE, L_SIZE = (5, 5, 3, 5)              # Side panels sizes in grid cells (0 = Non existent)

    ############### END ###################

    # Outside panel sizes in pixels
    TOPBAR = GRID_SIZE * T_SIZE
    RIGHTBAR = GRID_SIZE * R_SIZE
    BOTTOMBAR = GRID_SIZE * B_SIZE
    LEFTBAR = GRID_SIZE * L_SIZE

    SCREEN_WIDTH = GRID_SIZE * SCREEN_SIZE[0]  # Playing screen width in pixels
    SCREEN_HEIGHT = GRID_SIZE * SCREEN_SIZE[1]  # Playing screen height in pixels

    WINDOW_WIDTH = SCREEN_WIDTH + LEFTBAR + RIGHTBAR
    WINDOW_HEIGHT = SCREEN_HEIGHT + TOPBAR + BOTTOMBAR
    WINDOW_SIZE = (WINDOW_WIDTH,  WINDOW_HEIGHT)

    GRID_WIDTH = int(SCREEN_WIDTH / GRID_SIZE)  # Total number of grid squares on x axis
    GRID_HEIGHT = int(SCREEN_HEIGHT / GRID_SIZE)  # Total number of grid squares on y axis

    GRID_MID_Y = int(((SCREEN_HEIGHT / 2 + TOPBAR) / GRID_SIZE))  # Mid point on y axis in Grid coordinates
    GRID_MID_X = int(((SCREEN_WIDTH / 2 + LEFTBAR) / GRID_SIZE)) # Mid point on x axis in Grid coordinates

    # Grid boundaries in grid coordingates
    GRIDX_0 = int(LEFTBAR / GRID_SIZE)
    GRIDX_MAX = int((SCREEN_WIDTH + LEFTBAR) / GRID_SIZE)

    GRIDY_0 = int(TOPBAR / GRID_SIZE)
    GRIDY_MAX = int((SCREEN_HEIGHT + TOPBAR) / GRID_SIZE)

    TOP_BAR = (0,0,WINDOW_WIDTH,T_SIZE * GRID_SIZE)
    BTM_BAR = (0, WINDOW_HEIGHT - (B_SIZE * GRID_SIZE), WINDOW_WIDTH, WINDOW_HEIGHT)
    LEFT_BAR = (0, 0, L_SIZE * GRID_SIZE, WINDOW_HEIGHT)
    RIGHT_BAR = (WINDOW_WIDTH - (R_SIZE * GRID_SIZE), 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    surface = None

    BTM_FONT = pygame.font.Font("freesansbold.ttf", min(int(SCREEN_WIDTH/10), 40))
    ONSCREEN_FONT = pygame.font.Font("freesansbold.ttf", int(SCREEN_WIDTH/15))

    @classmethod
    def start_screen(cls):
        """ Starts screen with options as spceified above in the class fields """

        cls.surface = pygame.display.set_mode(cls.WINDOW_SIZE)
        pygame.display.set_caption(cls.S_TITLE)

        cls.fill_background()
        cls.draw_top_bar()
        cls.draw_btm_bar()
        cls.draw_left_bar()
        cls.draw_right_bar()

    @classmethod
    def fill_background(cls):
        """ Fills background with game_bg_color """
        cls.surface.fill(cls.BG_COLOR)

    @classmethod
    def draw_top_bar(cls):
        """ Draws score bar on display surface """
        pygame.draw.rect(cls.surface, cls.T_BG_COLOR, cls.TOP_BAR)

    @classmethod
    def draw_right_bar(cls):
        """ Draws score bar on display surface """
        pygame.draw.rect(cls.surface, cls.R_BG_COLOR, cls.RIGHT_BAR)

    @classmethod
    def draw_btm_bar(cls):
        """ Draws score bar on display surface """
        pygame.draw.rect(cls.surface, cls.B_BG_COLOR, cls.BTM_BAR)

    @classmethod
    def draw_left_bar(cls):
        """ Draws score bar on display surface """
        pygame.draw.rect(cls.surface, cls.L_BG_COLOR, cls.LEFT_BAR)

    @classmethod
    def display_btm_info(cls, msg):
        """ Displays the msg onto the bottom of the window where the bottom bar is """
        btm_surface = cls.BTM_FONT.render(msg, True, WHITE)
        btm_rect = btm_surface.get_rect()
        btm_rect.center = (cls.WINDOW_WIDTH / 2, cls.WINDOW_HEIGHT - (cls.BOTTOMBAR / 2))
        cls.surface.blit(btm_surface, btm_rect)

    @classmethod
    def display_msg(cls, msg):
        """ Displays msg onto the middle of the screen """
        display_msg_surface = cls.ONSCREEN_FONT.render(msg, True, BLACK)
        display_msg_rect = display_msg_surface.get_rect()
        display_msg_rect.center = (cls.WINDOW_WIDTH / 2,
                                (cls.WINDOW_HEIGHT - cls.BOTTOMBAR - cls.TOPBAR) /2 + cls.TOPBAR)
        cls.surface.blit(display_msg_surface, display_msg_rect)

    @classmethod
    def display_top_info(cls, msg):
        """ Displays the msg onto the top of the window where the top bar is """
        top_surface = cls.BTM_FONT.render(msg, True, WHITE)
        top_rect = top_surface.get_rect()
        top_rect.center = (cls.WINDOW_WIDTH / 2, cls.TOPBAR / 2)
        cls.surface.blit(top_surface, top_rect)

    @staticmethod
    def update():
        """ Updates Screen """
        pygame.display.update()

# ================ FOR TESTING PURPOSES ================ #

if __name__ == "__main__":

    Screen.start_screen()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        Screen.update()
