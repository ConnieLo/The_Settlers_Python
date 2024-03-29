import pygame

from classes.turn import Turn
from classes.player import Player
from classes.board import Board
from classes.settlement import Settlement
from typing import List

# TESTING INFO
# next_turn() should create and activate a new instance of the turn class. The active player of this turn should
# cycle through the 4 different players in the turn queue
# new_settlement() should instance a new settlement belonging to whichever player is the active player on the
# current turn. this settlement should be added to the board


PLAYER_COLOURS = [
    (255, 0, 0),  # RED
    (50, 100, 255),  # BLUE
    (50, 255, 50),  # GREEN
    (255, 220, 0)  # YELLOW
]

class GameMaster:
    """
    The primary class responsible for maintaining a single game of The Settlers. Acts as the central management node
    through which each other object in the game communicates. Is also responsible for instancing many of the objects

    ATTRIBUTES

    turn_queue: list
        The players in the game, in turn order

    current_turn: int
        Current turn number, starting at -1 for the set-up, and incrementing by one for each player turn

    turn_inst: Turn
        The Turn object currently active

    board: Board
        The board - which holds tiles, settlements, and roads

    initialised: bool
        Whether the game has advanced beyone the set-up phase

    saved_tuples: list
        A list of all the tuples the game master has checked so far.
        Tuples are in the format (x: num, y: num) and represent a position on the gui

    tuple_count: dict
        The amount of times the game master has seen a given tuple, in the format {tuple: int}

    last_checked_tuple: tuple
        The last tuple the game master has seen
    """
    def __init__(self):
        self.turn_queue = [
            Player("player {}".format(i), PLAYER_COLOURS[i]) for i in range(4)
        ]
        self.current_turn: int = -1 #initialised as -1 so that first turn instance will advance it to player 0
        self.turn_inst = None
        self.next_turn()
        self.board = Board()
        self.saved_tuples = []
        self.tuple_count = {}
        self.last_checked_tuple = None
        self.initialised = False

    def next_turn(self) -> Turn:
        """
        Generates a new Turn object for whichever player is next
        :return:
            The Turn
        """
        self.current_turn += 1
        player = self.turn_queue[self.current_turn % 4]
        print("next turn")
        self.turn_inst = Turn(self, player, self.current_turn)

    def check_three_same_tuples(self, positions: list) -> bool:
        """
        Check to see if a list of tuples - representing a point on the board, are the same

        :param positions: list
            The positions

        :return:
            True if they are the same
        """
        for position in positions:
            if position != self.last_checked_tuple:
                self.saved_tuples.append(position)
                self.last_checked_tuple = position
                if position in self.tuple_count:
                    self.tuple_count[position] += 1
                else:
                    self.tuple_count[position] = 1
                if self.tuple_count[position] == 3:
                    return True
        return False

    def new_settlement(self, owner: Player, settlement_info: str) -> Settlement:
        """
        Signals the board to create a new settlement, and updates the player's victory points and number of
        settlements

        :param owner: Player
            The player building the new settlement
        :param settlement_info:
            A data representation of the new settlement
        :return:
            The newly constructed settlement
        """
        owner.increment_victory_points()
        owner.increment_number_of_settlements()
        self.board.new_settlement(owner, settlement_info)
        return True
    
    def new_road(self, owner, position):
        """
        Signals the board to create a new road at the given position, and updates the owner's number of roads
        :param owner: Player
            The player building the new road
        :param position:
        :return:
        """
        self.board.new_road(owner, position)
        owner.increment_number_of_roads()
        return True

    def pass_resources(self, roll: int) -> None:
        for s in self.board.get_settlements():
            s.grant_resources(roll)
    
    def get_board(self):
        return self.board


# UI to display the number of turns so far and the current player's turn
pygame.font.init()
font = pygame.font.Font(None, 36)
# A helper method used in draw method
def draw_text(screen, text, x, y, color=(255, 255, 255), font=None):
    """
    Draws the given text on screen

    :param screen: Pygame.Surface
        The surface on which the text is to be written
    :param text: str
        The text
    :param x: int
        The x co-ordinate
    :param y: inr
        The y co-ordinate
    :param color: tuple, optional
        The colour as an (r, g, b) tuple of ints
    :param font: Pygame.Font
        The font to use
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw(game_master: GameMaster, screen):
    """
    Prompts the given game master to write infor on the current player to the screen

    :param game_master: GameMaster
        The game master
    :param screen: Pygame.Surface
        The surface which is to be written to
    """
    # Get the current player
    current_player = game_master.turn_queue[game_master.current_turn % 4]
    # Display the current player's turn
    draw_text(screen, f"Number of turns: {game_master.current_turn}", 10, 150, font=font)
    draw_text(screen, f"Current Player: {current_player.name}", 10, 200, font=font)
    # Update the screen
