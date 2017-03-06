import os
os.environ['SDL_VIDEO_CENTERED'] = "1"

import random
import math
import pygame
pygame.init()

### COLOR DEFINITIONS ###
# colors are the only globals allowed
red = (255,0,0)
darkred = (175,0,0)
green = (0,255,0)
blue = (0,0,255)
darkblue = (0,0,175)
white = (255,255,255)
black = (0,0,0)

### CLASS DEFINITIONS ###
class Player:
    def __init__(self, playername, team):
        self.Name = playername
        self.Team = team

        if self.Team == "blue":
            self.Color = blue
            self.Color_sec = darkblue
            self.Dice = Dice(750, 50, 100, self)
        elif self.Team == "red":
            self.Color = red
            self.Color_sec = darkred
            self.Dice = Dice(900, 50, 100, self)
        else:
            self.Color = green

    def Draw(self):
        self.Dice.Draw()

class Dice:
    def __init__(self, x, y, width, player):
        self.X = x
        self.Y = y
        self.Width = width
        self.Player = player

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
        pygame.draw.rect(game.Display, self.Player.Color, (self.X, self.Y, self.Width, self.Width))
        pygame.draw.rect(game.Display, black, (self.X + self.Width / 9, self.Y + self.Width / 9, self.Width / 9 * 7, self.Width / 9 * 7))
        # drawing the eyes
        for i in self.Code: pygame.draw.rect(game.Display, self.Player.Color, (self.Eyes[i][0], self.Eyes[i][1], self.Width/9, self.Width/9))

class Path_node:
    def __init__(self, starttile, player):
        self.X = starttile.X + 40 # + 40 is the middle of the tile. a tile is 80x80
        self.Y = starttile.Y + 40
        self.Player = player

        self.Path = []
        self.Element = len(self.Path) - 1

        self.Speed = 0.5

        self.Trail = []
        self.Trail_temp = []
        self.Trail_old = []
    
    def Set_path(self, path):
        self.Path = path[::-1] + path
        self.Element = len(self.Path)
        self.Next()
    
    def Next(self):
        self.Element = self.Element - 1
        if self.Element == -1:
            self.Element = len(self.Path) - 1
            self.Trail_old = self.Trail
            self.Trail = []
            self.X = self.Path[self.Element].X + 40
            self.Y = self.Path[self.Element].Y + 40
    
    def Get_vel(self):
        # coords of the next tile (element in path)
        tx = self.Path[self.Element].X + 40
        ty = self.Path[self.Element].Y + 40
        
        s = math.sqrt((tx - self.X)**2 + (ty - self.Y)**2)
        # if s > 41: speed = int((s - 41) // 4.1 * 0.25) + 1
        
        speed = int(-0.00225 * (s-47.14)**2 + 6)

        x = 0
        y = 0

        if   tx > self.X: # left
            if tx - self.X < speed: # distance between node and tile smaller than its speed?
                excess_speed = speed - (tx - self.X) # set the excess speed
                x = x + (speed - excess_speed) # set the movement as the distance between the tile and node
            else:
                x = x + speed
        elif tx < self.X: # right
            if self.X - tx < speed:
                excess_speed = speed - (self.X - tx)
                x = x - (speed - excess_speed)
            else:
                x = x - speed
    
        if   ty > self.Y: # down
            if ty - self.Y < speed:
                excess_speed = speed - (ty - self.Y)
                y = y + (speed - excess_speed)
            else:
                y = y + speed
        elif ty < self.Y: # up
            if self.Y - ty < speed:
                excess_speed = speed - (self.Y - ty)
                y = y - (speed - excess_speed)
            else:
                y = y - speed
        
        #TODO: do something with the excess speed

        return (x,y)

    def Draw(self):
        x = self.X
        y = self.Y
        self.Trail_temp.append([self.X, self.Y])

        self.X = self.X + self.Get_vel()[0]
        self.Y = self.Y + self.Get_vel()[1]
        if self.X == self.Path[self.Element].X + 40 and self.Y == self.Path[self.Element].Y + 40:
            self.Trail.append([self.Path[self.Element].X+40, self.Path[self.Element].Y+40])
            self.Trail_temp = []
            self.Next()

        if len(self.Trail_temp) > 1: pygame.draw.lines(game.Display, self.Player.Color_sec, False, self.Trail_temp, 3)

        if len(self.Trail) > 1:
            pygame.draw.lines(game.Display, self.Player.Color_sec, False, self.Trail, 3)
        for coords in self.Trail: pygame.draw.circle(game.Display, self.Player.Color_sec, coords, 5, 0) # CHANGE TO PNGS

        if len(self.Trail_old) > 1:
            pygame.draw.lines(game.Display, self.Player.Color_sec, False, self.Trail_old, 3)
        for coords in self.Trail_old: pygame.draw.circle(game.Display, self.Player.Color_sec, coords, 5, 0) # CHANGE TO PNGS
        
        if self.X != x: pygame.draw.rect(game.Display, self.Player.Color_sec, (self.X-10, self.Y-5, 20, 10))
        else: pygame.draw.rect(game.Display, self.Player.Color_sec, (self.X-5, self.Y-10, 10, 20))

class Grid:
    def __init__(self, x, y, tilewidth):
        self.X = x
        self.Y = y

        self.Paths = [[], []]
        
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
        
        self.Akkers = self.Tiles[0][7]
        self.Beurs  = self.Tiles[7][0]
        self.Akkers.Set_tile("akkers", 0, Player("any", "any")) # creating start-tile
        self.Beurs.Set_tile("beurs", 0, Player("any", "any")) # creating end-tile

        self.Tiles[1][7].Set_tile("cross", 0, player1)
        self.Tiles[2][7].Set_tile("cross", 0, player1)
        self.Tiles[2][6].Set_tile("cross", 0, player1)
        self.Tiles[2][5].Set_tile("cross", 0, player1)
        self.Tiles[3][5].Set_tile("cross", 0, player1)
        self.Tiles[4][5].Set_tile("cross", 0, player1)
        self.Tiles[5][5].Set_tile("cross", 0, player1)
        self.Tiles[6][5].Set_tile("cross", 0, player1)
        self.Tiles[7][5].Set_tile("cross", 0, player1)
        self.Tiles[7][4].Set_tile("cross", 0, player1)
        self.Tiles[7][3].Set_tile("cross", 0, player1)
        self.Tiles[6][3].Set_tile("cross", 0, player1)
        self.Tiles[5][3].Set_tile("cross", 0, player1)
        self.Tiles[5][2].Set_tile("cross", 0, player1)
        self.Tiles[5][1].Set_tile("cross", 0, player1)
        self.Tiles[5][0].Set_tile("cross", 0, player1)
        self.Tiles[6][0].Set_tile("cross", 0, player1)
        self.Tiles[2][5].Set_tile("cross", 0, player1)
        self.Tiles[7][2].Set_tile("cross", 0, player1)
        self.Tiles[7][1].Set_tile("cross", 0, player1)

        
        self.Tiles[0][6].Set_tile("cross", 0, player2)
        self.Tiles[0][5].Set_tile("cross", 0, player2)
        self.Tiles[1][5].Set_tile("cross", 0, player2)
        self.Tiles[1][4].Set_tile("cross", 0, player2)

        # path follower
        self.Path_nodes = [Path_node(self.Akkers, player1), Path_node(self.Akkers, player2)]

    def Change_tile(self, x, y, tile, rotation, player):
        self.Tiles[x][y].Set_tile(tile, rotation, player)
    
    def Check_connected(self): # connected to the start tile
        # change all connected vars to False
        for a in self.Tiles:
            for tile in a:
                tile.Connected = False
        
        # start pathfinding (starting from akkers)
        self.Tiles[0][7].Connected = True
        self.Tiles[0][7].Tell_tiles()

        # checking if beurs is connected
        if self.Tiles[7][0].Connected:
            # the player that connected to beurs wins
            Win(self.Tiles[7][0].Player)
    
        self.Paths = self.Best_paths()

        for i in range(0,2):
            self.Path_nodes[i].Set_path(self.Paths[i])

    def Best_paths(self):
        for team in ("blue", "red"): # TODO: change this to actual players?
            best_dist = self.Tiles[0][7].Raw_distance() + 1 # RAW distance from start to finish (longest distance possible)
            best_tile = None

            # get the tile closest to the beurs tile
            for a in self.Tiles:
                for tile in a: 
                    if tile.Connected == True and tile.Player.Team == team: # connected + team restriction
                        print(str(tile.Pos) + " " + str(tile.Raw_distance()))
                        if tile.Raw_distance() < best_dist: # is the distance of this tile shorter than the (until now) shortest?
                            best_dist = tile.Raw_distance() # shortest distance
                            best_tile = tile # best tile
            
            if best_tile == None:
                print("NO TILES FOUND FOR " + team)
                if team == "blue":
                    bluepath = [self.Akkers]
                else:
                    redpath = [self.Akkers]
            else:
                print("TILE FOUND FOR " + team + ". <" + str(best_tile.Pos) + ">")
                # put all the parents of the best tile in a list
                path = [best_tile] + best_tile.Get_parent()

                # set the best paths of both players
                if team == "blue":
                    bluepath = path
                else:
                    redpath = path
            
        return [bluepath, redpath]
    
    def Draw(self):
        # draw all tiles of the grid
        for a in self.Tiles:
            for b in a:
                b.Draw()
        
        for i in self.Path_nodes:
            if i.Path != [self.Akkers] and i.Path != []:
                i.Draw()
        
class Tile:
    def __init__(self, x, y, pos, width):
        self.X = x
        self.Y =  y
        self.Width = width
        self.Pos = pos
        
        self.Tile = None
        self.Rotation = None
        self.Rail = [False, False, False, False]
        self.Player = None
        self.Connected = False
        self.Parent = None
    
    def Get_parent(self):
        if self.Parent == None:
            return []
        else:
            return [self.Parent] + self.Parent.Get_parent()
    def Raw_distance(self):
        # (7, 7) is the position of the beurs tile
        x = 7 - self.Pos[0]
        y = self.Pos[1]
        return math.sqrt(x**2 + y**2) # straight line from this tile to the beurs tile. (1 : tilewidth)

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
        if self.Player != None:
            access = False
            if (self.Player.Team == telling_tile.Player.Team or telling_tile.Player.Team == "any") and not self.Connected: # Checks if the tile's not yet connected to the start and if he's from the same team
                # checks if this tile is connected to the one that is telling
                if   angle == "under" and self.Rail[0]: access = True
                elif angle == "left"  and self.Rail[1]: access = True
                elif angle == "above" and self.Rail[2]: access = True
                elif angle == "right" and self.Rail[3]: access = True
            
            if access: # if not connected, of the same team and has a rail going to the telling tile
                print("[" + str(telling_tile.Pos[0]) + "][" + str(telling_tile.Pos[1]) + "] tells the tile " + angle + " that he is connected. The tile (" + str(self.Player) + ") listened and tells the others.")
                self.Connected = True # sets itself as connected to akkers
                self.Parent = telling_tile # sets his parent as the telling tile
                self.Tell_tiles() # tells the tiles around him he's connected (RECURSION EFFECT)
            else:
                print("[" + str(telling_tile.Pos[0]) + "][" + str(telling_tile.Pos[1]) + "] tells the tile " + angle + " that he is connected. The tile did not listen.")
    def Check_neighbours(self):
        #RESTRICTION: if its out of the grid
        if self.Pos[1] - 1 >= 0: a = grid.Tiles[self.Pos[0]][self.Pos[1] - 1].Rail[2]
        else: a = False
        if self.Pos[0] + 1 <= 7: b = grid.Tiles[self.Pos[0] + 1][self.Pos[1]].Rail[3]
        else: b = False
        if self.Pos[1] + 1 <= 7: c = grid.Tiles[self.Pos[0]][self.Pos[1] + 1].Rail[0]
        else: c = False
        if self.Pos[0] - 1 >= 0: d = grid.Tiles[self.Pos[0] - 1][self.Pos[1]].Rail[1]
        else: d = False

        return [a, b, c, d]


    def Draw(self):
        # TEMP: drawing squares instead of actual tile images
        if   self.Tile == None:
            pygame.draw.rect(game.Display, white, (self.X, self.Y, self.Width, self.Width))
        elif self.Tile == "akkers" or self.Tile == "beurs":
            pygame.draw.rect(game.Display, green, (self.X, self.Y, self.Width, self.Width))
        elif self.Connected:
            pygame.draw.rect(game.Display, self.Player.Color, (self.X, self.Y, self.Width, self.Width))

        # around the tile
        directions = self.Check_neighbours()
        if directions[0] and self.Rail[0]: pygame.draw.rect(game.Display, self.Player.Color, (self.X, self.Y - 6, self.Width, 6))
        if directions[1] and self.Rail[1]: pygame.draw.rect(game.Display, self.Player.Color, (self.X + self.Width, self.Y, 6, self.Width))
        if directions[2] and self.Rail[2]: pygame.draw.rect(game.Display, self.Player.Color, (self.X, self.Y + self.Width, self.Width, 6))
        if directions[3] and self.Rail[3]: pygame.draw.rect(game.Display, self.Player.Color, (self.X - 6, self.Y, 6, self.Width))

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
                player1.Draw()
                player2.Draw()

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
player1 = Player("Henk", "blue")
player2 = Player("Harry", "red")
grid = Grid(10, 10, 80)
grid.Check_connected()

### STARTS THE GAME ###
game.Loop()

### ENDS THE GAME ###
pygame.quit()
quit()
