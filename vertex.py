import settlement
import vertex

class Vertex():

    def __init__(self, coords):
        self.coords = coords
        self.settlement = None

    def get_coords(self):
        return self.coords
    
    def add_settlement(self, owner):
        self.settlement = settlement.Settlement(owner, [])#brackets will contain the 2/3 hexes the vertex connects to


        