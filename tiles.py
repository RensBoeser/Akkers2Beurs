import random
import os

tile_total_1 = 10
tile_total_2 = 12
tile_total_3 = 6
tile_total_4 = 4
tile_total_5 = 4
tile_total_6 = 2
tile_total_7 = 2

def print_tile(tile_ID):
    y = 1
    p = ""
    while(y <= 5):
        x = 1
        while(x <= 9):
            if(y == 1 or y == 5):
                if(x == 1 or x == 9):
                    p = p + "+"
                elif(x == 3 or x == 5 or x == 7):
                    p = p + "-"
                else:
                    p = p + " "
            elif(x == 1 or x == 9):
                p = p + "|"


            elif(tile_ID == 1):
                if(x == 5 and y > 1 and y < 5):
                    p = p + "|"
                else:
                    p = p + " "
            elif(tile_ID == 2):
                if(x == 5 and y == 4):
                    p = p + "|"
                elif(x == 5 and y == 3):
                    p = p + "+"
                elif(x == 7 and y == 3):
                    p = p + "-"
                else:
                    p = p + " " 
            elif(tile_ID == 3):
                if(x == 5 and y == 4):
                    p = p + "|"
                elif(x == 5 and y == 3):
                    p = p + "+"
                elif(x == 3 and y == 3):
                    p = p + "-"
                elif(x == 7 and y == 3):
                    p = p + "-"
                else:
                    p = p + " " 
            elif(tile_ID == 4):
                if(x == 5 and y == 4):
                    p = p + "|"
                elif(x == 5 and y == 2):
                    p = p + "|"
                elif(x == 5 and y == 3):
                    p = p + "+"
                elif(x == 3 and y == 3):
                    p = p + "-"
                elif(x == 7 and y == 3):
                    p = p + "-"
                else:
                    p = p + " " 
            elif(tile_ID == 5):
                if(x == 3 and y >= 3 and y <= 4):
                    p = p + "|"
                elif((x == 3 or x == 7) and y == 2):
                    p = p + "+"
                elif(x == 5 and y == 2):
                    p = p + "-"
                elif(x == 7 and y == 3):
                    p = p + "|"
                elif(x == 5 and y == 4):
                    p = p + "<"
                elif(x == 7 and y == 4):
                    p = p + "+"
                else:
                    p = p + " "
            elif(tile_ID == 6):
                if(x == 5 and y == 3):
                    p = p + "B"
                else:
                    p = p + " "
            elif(tile_ID == 7):
                if(x == 3 and y == 3):
                    p = p + "/"
                elif(x == 5 and y == 2):
                    p = p + "_"
                elif(x == 7 and y == 3):
                    p = p + "\\"
                else:
                    p = p + " "
            x = x + 1
        y = y + 1
        p = p + "\n"
    print(p)
os.system("cls")

deck_IDs = [random.randint(1,7),random.randint(1,7),random.randint(1,7),random.randint(1,7)]
print_tile(deck_IDs[0])
print_tile(deck_IDs[1])
print_tile(deck_IDs[2])
print_tile(deck_IDs[3])