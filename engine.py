import pygame
pygame.init()

### COLOR DEFINITIONS ###
# colors are the only globals allowed
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

### CLASS DEFINITIONS ###
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

                self.Draw() # black screen. draw all your things after this line

                text("This is a test.", 60, 10, 10)

                self.Tick() # refreshes the window. this is the end of the loop
            
            # you can use elifs here to make new levels

            else: self.Exit = True # if self.Level is not a valid level, it will terminate the while-loop

### FUNCTION DEFINITIONS ###
def text(text, size, x, y, fontname=None, textcolor=(255,255,255)):
    # blits text on the screen
    font = pygame.font.SysFont(fontname, size)
    screen_text = font.render(text, True, textcolor)
    game.Display.blit(screen_text, [x,y])


### INITIALISTATIONS OF CLASSES ###
game = Game()


### STARTS THE GAME ###
game.Loop()

### ENDS THE GAME ###
pygame.quit()
quit()