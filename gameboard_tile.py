# + - - - +
# |       |
# |       |
# |       |
# + - - - +

class tile:
    def __init__(self, name, line1, line2, line3):
        self.Name = name
        self.Line1 = line1
        self.Line2 = line2
        self.Line3 = line3

tile_0 = tile("none","       ","       ","       ")
tile_1 = tile("straight1","   |   ","   |   ","   |   ")
tile_2 = tile("turn1","       ","   + - ","   |   ")

