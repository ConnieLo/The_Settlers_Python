import random as rnd
import pygame
from tools import hugo_hex
from tools.grid import GridStruct
from classes.settlement import Settlement
from classes.road import Road

# TESTING INFO
# generate_tiles() should create a randomly generated array of tuples (number, resource) according to the rules of
# Cataan
# new_settlement() should create a new object of the settlement class, which should contain information about which
# tiles are adjacent to the settlement and which player owns it
# get_settlements() should return a list of all the settlements

class Board:
    """
    The class responsible for storing tiles, settlements, roads, and their positions (or, more accurately, abstractions
    of their positions so that the rest of the game can function).

    ATTRIBUTES

    tiles: list
        A list of tiles in the board, where each tile in the board is represented by a tuple in the format
        (dice_no: in, resource: str)

    grid: GridStruct
        The grid structure used for storage

    settlements: list
        A list of the Settlements in the board

    roads: list
        A list of the Roads in the board
    """
    def __init__(self):
        self.tiles = self.generate_tiles()
        self.grid = GridStruct()
        self.settlements = []
        self.roads = []
        print("board initialised")

    def generate_tiles(self):
        """
        Generates 19 tiles in random positions according to the rules of The Settlers
        :return:
            The list of tiles
        """
        new_tiles = []

        # The resource pool
        resources = []
        resources.extend(["sheep" for i in range(4)])
        resources.extend(["wheat" for i in range(4)])
        resources.extend(["wood" for i in range(4)])
        resources.extend(["ore" for i in range(3)])
        resources.extend(["clay" for i in range(3)])
        rnd.shuffle(resources)

        # The number tokens pool
        # There whould be two of every number between 2 and 12
        # but NO 7s, only ONE 2, and only ONE 12
        numbers = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        rnd.shuffle(numbers)

        # Assigning the numbers and resources randomly
        for i in range(18):
            new_tiles.append((numbers[i], resources[i]))

        # Putting the desert at a random spot
        new_tiles.insert(rnd.randint(0, 18), (0, "desert"))

        return new_tiles

    def new_settlement(self, owner, settlement_info):
        """
        Instances and stores a new settlement
        :param owner: Player
            The Player to whom the new settlement belongs
        :param settlement_info:
            Infor on the new settlement
        :return:
            True if the settlement has been successfully created
        """
        new: Settlement = Settlement(owner, settlement_info)
        self.settlements.append(new)
        return True
    
    def new_road(self, owner, position):
        """
        Instances and stores a new road
        :param owner: Player
            The Player to whom the new road belongs
        :param position:
            The position of the new road
        """
        new = Road(owner, position)
        self.roads.append(new)

    def get_settlements(self):
        """
        Gets every settlement stored
        :return:
            A list of the settlements
        """
        return self.settlements

    def get_tile_info(self, position):
        """
        returns the tile number, resource, and position number for a given position
        :param position:
            The positions
        :return:
            Position, resource, number
        """
        if 0 <= position < len(self.tiles):
            number, resource = self.tiles[position]
            return position, resource, number
        else:
            return None

    def draw_board(self, _surface, hex_images, number_images):
        """
        Renders the board to the screen

        :param _surface: Pygame.Surface
            The surface on which to draw the board
        :param hex_images:
            The images to use for the resources
        :param number_images:
             The images to use for the numbers
        """
        for i, (number, resource) in enumerate(self.tiles):
            # Draw the hexagon
            center = hex_grid.offset(*co_ords[i])
            center = (center[0] + SCREEN_WIDTH / 2, center[1] + SCREEN_HEIGHT / 2)
            image = hex_images.get(resource)

            if image is not None:
                hex_surface = pygame.Surface(hex_grid.hex_size, pygame.SRCALPHA)
                image = pygame.transform.scale(image, (hex_grid.hex_size[0] - 30, hex_grid.hex_size[1] - 20))
                hex_surface.blit(image, (15, 10))
                surface_rect = hex_surface.get_rect(center=center)
                _surface.blit(hex_surface, surface_rect)

            # Draw the number
            if number != 0:
                image = number_images.get(number)
                if image is not None:
                    hex_surface = pygame.Surface(hex_grid.hex_size, pygame.SRCALPHA)
                    image = pygame.transform.scale(image, (hex_grid.hex_size[0] + 60, hex_grid.hex_size[1] + 40))
                    hex_surface.blit(image, (-30, -20))
                    surface_rect = hex_surface.get_rect(center=center)
                    _surface.blit(hex_surface, surface_rect)


#################  UI ###########################
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
# Creating a new hex grid at the center of the screen
hex_grid = hugo_hex.HexGrid(60, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
hex_radius = hex_grid.hex_size
# Grid co-ordinates
co_ords = []
co_ords += [(i, 2) for i in range(-2, 1)]
co_ords += [(i, 1) for i in range(-2, 2)]
co_ords += [(i, 0) for i in range(-2, 3)]
co_ords += [(i, -1) for i in range(-1, 3)]
co_ords += [(i, -2) for i in range(0, 3)]
####################################################

b = Board()
print(b.tiles)

# The class TileInfor extracts the vertex number, tile number, and resource information from the Board object
# and stores it in instances of the TileInfo class. Then, it will print out the index,
# vertex number, tile number, and resource for each TileInfo object in the tile_info_list.
class TileInfo:
    i = 0
    def __init__(self, vertex_number, tile_number, resource):
        self.position = TileInfo.i
        TileInfo.i += 1
        self.vertex_number = vertex_number
        self.tile_number = tile_number
        self.resource = resource

    def print_info(self):
        print(f"Position: {self.position}, Vertex Number: {self.vertex_number}, Tile Number: {self.tile_number}, Resource: {self.resource}")
# List to store TileInfo objects
tile_info_list = []
# This extracts resources from the Board object
for idx, co in enumerate(co_ords):
    points = hex_grid.get_hex_vertices(*co)
    for vertex_number, point in enumerate(points):
        _, resource, tile_number = b.get_tile_info(idx)
        tile_info = TileInfo(vertex_number, tile_number, resource)
        tile_info_list.append(tile_info)

# Prints the information for each TileInfo object
#for info in tile_info_list:
#    info.print_info()