import os
os.environ['SDL_VIDEO_CENTERED'] = "1"

import random
import pygame
pygame.init()

### COLOR DEFINITIONS ###
# colors are the only globals allowed
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)

### CLASS DEFINITIONS ###
class Dice:
    def __init__(self, x, y, width):
        self.X = x
        self.Y = y
        self.Width = width

        self.Code = None
        self.Number = random.randint(1,6)
        self.Eyes = []

        # all coords of possible eyes on a dice
        x = x + width // 9 * 2
        y = y + width // 9 * 2
        for i in range(1,10):
            self.Eyes.append([x,y])
            x = x + self.Width // 9 * 2
            if i % 3 == 0:
                x = self.X + self.Width // 9 * 2
                y = y + self.Width // 9 * 2
    
    def Roll(self):
        self.Number = random.randint(1,6)
    
    def Draw(self):
        # getting the 'code' for the eyes that have to be drawn
        if   self.Number == 1: self.Code = [4]
        elif self.Number == 2: self.Code = [0, 8]
        elif self.Number == 3: self.Code = [0, 4, 8]
        elif self.Number == 4: self.Code = [0, 2, 6, 8]
        elif self.Number == 5: self.Code = [0, 2, 4, 6, 8]
        elif self.Number == 6: self.Code = [0, 2, 3, 5, 6, 8]

        # drawing the dice
        pygame.draw.rect(game.Display, white, (self.X, self.Y, self.Width, self.Width))
        pygame.draw.rect(game.Display, black, (self.X + self.Width / 9, self.Y + self.Width / 9, self.Width / 9 * 7, self.Width / 9 * 7))
        # drawing the eyes
        for i in self.Code: pygame.draw.rect(game.Display, white, (self.Eyes[i][0], self.Eyes[i][1], self.Width/9, self.Width/9))


class Grid:
    def __init__(self, x, y, tilewidth):
        self.X = x
        self.Y = y
        
        # tiles in the grid creation
        tilex = self.X
        tiley = self.Y
        self.Tiles = []
        for x in range(0,8):
            self.Tiles.append([])
            for y in range(0,8):
                self.Tiles[x].append(Tile(tilex, tiley, [x, y], tilewidth))
                tiley += tilewidth + 12
            tilex += tilewidth + 12
            tiley = self.Y

        self.Tiles[0][7].Set_tile("akkers", 0, "any") # creating start-tile
        self.Tiles[7][0].Set_tile("beurs", 0, "any") # creating end-tile

    def Change_tile(self, x, y, tile, rotation, player):
        self.Tiles[x][y].Set_tile(tile, rotation, player)
    
    def Check_connected(self):
        # change all connected vars to False
        for a in self.Tiles:
            for b in a:
                b.Connected = False
        
        # start pathfinding (starting from akkers)
        self.Tiles[0][7].Connected = True
        self.Tiles[0][7].Tell_tiles()

        # checking if beurs is connected
        if self.Tiles[7][0].Connected:
            # the player that connected to beurs wins
            Win(self.Tiles[7][0].Player)

    def Draw(self):
        # draw all tiles of the grid
        for a in self.Tiles:
            for b in a:
                b.Draw()

class Tile:
    def __init__(self,x,y,pos, width):
        self.X = x
        self.Y =  y
        self.Width = width
        self.Pos = pos
        
        self.Tile = None
        self.Rotation = None
        self.Rail = [False, False, False, False]
        self.Player = None
        self.Connected = False

    def Set_tile(self, tile, rotation, player):
        if   tile == "akkers":  self.Rail = [True, True, False, False]
        
        elif tile ==  "beurs":  self.Rail = [False, False, True, True]

        elif tile ==  "cross":  self.Rail =   [True, True, True, True]

        elif tile == "straight":
            if   rotation == 0: self.Rail = [True, False, True, False]
            elif rotation == 1: self.Rail = [False, True, False, True]

        elif tile == "turn":
            if   rotation == 0: self.Rail = [True, False, False, True]
            elif rotation == 1: self.Rail = [True, True, False, False]
            elif rotation == 2: self.Rail = [False, True, True, False]
            elif rotation == 3: self.Rail = [False, False, True, True]
        
        elif tile == "tcross":
            if   rotation == 0: self.Rail =  [False, True, True, True]
            elif rotation == 1: self.Rail =  [True, False, True, True]
            elif rotation == 2: self.Rail =  [True, True, False, True]
            elif rotation == 3: self.Rail =  [True, True, True, False]
        
        self.Player   = player
        self.Tile     = tile
        self.Rotation = rotation
    
    def Tell_tiles(self):
        if self.Rail[0] and self.Pos[1]-1 >= 0: grid.Tiles[self.Pos[0]][self.Pos[1]-1].Listen(self, "above") # Tells the tile above to listen
        if self.Rail[1] and self.Pos[0]+1 < 8 : grid.Tiles[self.Pos[0]+1][self.Pos[1]].Listen(self, "right") # Tells the tile on the right to listen
        if self.Rail[2] and self.Pos[1]+1 < 8 : grid.Tiles[self.Pos[0]][self.Pos[1]+1].Listen(self, "under") # Tells the tile under to listen
        if self.Rail[3] and self.Pos[0]-1 >= 0: grid.Tiles[self.Pos[0]-1][self.Pos[1]].Listen(self, "left")  # Tells the tile on the left to listen
    
    def Listen(self, telling_tile, angle):
        access = False
        if (self.Player == telling_tile.Player or telling_tile.Player == "any") and not self.Connected: # Checks if the tile's not yet connected to the start and if he's from the same team
            # checks if this tile is connected to the one that is telling
            if   angle == "under" and self.Rail[0]: access = True
            elif angle == "left"  and self.Rail[1]: access = True
            elif angle == "above" and self.Rail[2]: access = True
            elif angle == "right" and self.Rail[3]: access = True
        
        if access: # if not connected, of the same team and has a rail going to the telling tile
            print("[" + str(telling_tile.Pos[0]) + "][" + str(telling_tile.Pos[1]) + "] tells the tile " + angle + " that he is connected. The tile (" + str(self.Player) + ") listened and tells the others.")
            self.Connected = True # sets itself as connected to akkers
            self.Tell_tiles() # tells the tiles around him he's connected (RECURSION EFFECT)
        else:
            print("[" + str(telling_tile.Pos[0]) + "][" + str(telling_tile.Pos[1]) + "] tells the tile " + angle + " that he is connected. The tile did not listen.")
    
    def Draw(self):
        # TEMP: drawing squares instead of actual tile images
        if   self.Tile == None:
            pygame.draw.rect(game.Display, red, (self.X, self.Y, self.Width, self.Width))
        elif self.Tile == "akkers" or self.Tile == "beurs":
            pygame.draw.rect(game.Display, green, (self.X, self.Y, self.Width, self.Width))
        elif self.Connected:
            pygame.draw.rect(game.Display, blue, (self.X, self.Y, self.Width, self.Width))

class Game:
    def __init__(self):
        # FPS setup
        self.FPS = 30
        self.clock = pygame.time.Clock()

        # pygame window creation
        self.Width = 1360
        self.Height = 768
        self.Display = pygame.display.set_mode((self.Width, self.Height))
        
        # gameloop and first level setup
        self.Exit = False
        self.Level = "menu"
            
    def Draw(self): # create a black screen
        self.Display.fill((0,0,0))
    def Tick(self): # refresh the window and wait 1/FPS seconds
        pygame.display.update()
        self.clock.tick(self.FPS)
    def Loop(self): # game loop
        while not self.Exit:

            if self.Level == "menu": # loop only goes here if the level is 'menu'
                for event in pygame.event.get(): # checking for any events

                    if event.type == pygame.QUIT: # checks if someone tries to close the window
                        self.Exit = True # stops the while-loop
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.Exit = True

                self.Draw() # black screen. draw all your things after this line

                grid.Draw()

                self.Tick() # refreshes the window. this is the end of the loop
            
            # you can use elifs here to make new levels

            else: self.Exit = True # if self.Level is not a valid level, it will terminate the while-loop

### FUNCTION DEFINITIONS ###
def win(player):
    game.Level = "exit"
def text(text, size, x, y, fontname=None, textcolor=(255,255,255)):
    # blits text on the screen
    font = pygame.font.SysFont(fontname, size)
    screen_text = font.render(text, True, textcolor)
    game.Display.blit(screen_text, [x,y])


### INITIALISTATIONS OF CLASSES ###
game = Game()
grid = Grid(10, 10, 80)

### STARTS THE GAME ###
game.Loop()

### ENDS THE GAME ###
pygame.quit()
quit()
