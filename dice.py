import random
import time
import os
import sys

N = ""
dice_number = int(input("How many dice do you want to roll? "))
while(dice_number > 5 or dice_number < 1):
    if(dice_number > 5):
        print("Python cannot handle more than 5 dice...")
    if(dice_number < 1):
        print("Insert a valid number...")
    dice_number = int(input("How many dice do you want to roll? "))
def dice():
    roll = random.randint(1,6)
    y = 1
    while(y <= 7):
        x = 1
        while(x <= 13):
    #ROLL 1
            if(roll == 1):
                if(y == 1 or y == 7):
                    print("#", end="")
                elif(x == 1 or x == 13):
                    print("#", end="")
                # DICE THROW
                elif(y == 4 and x == 7):
                    print("#", end="")
                else:
                    print(" ", end="")
    #ROLL 2
            if(roll == 2):
                if(y == 1 or y == 7):
                    print("#", end="")
                elif(x == 1 or x == 13):
                    print("#", end="")
                # DICE THROW
                elif(y == 2 and x == 7):
                    print("#", end="")
                elif(y == 6 and x == 7):
                    print("#", end="")
                else:
                    print(" ", end="")
    #ROLL 3
            if(roll == 3):
                if(y == 1 or y == 7):
                    print("#", end="")
                elif(x == 1 or x == 13):
                    print("#", end="")
                # DICE THROW
                elif(y == 2 and x == 7):
                    print("#", end="")
                elif(y == 4 and x == 7):
                    print("#", end="")
                elif(y == 6 and x == 7):
                    print("#", end="")
                else:
                    print(" ", end="")
    #ROLL 4
            if(roll == 4):
                if(y == 1 or y == 7):
                    print("#", end="")
                elif(x == 1 or x == 13):
                    print("#", end="")
                # DICE THROW
                elif(y == 2 and x == 4):
                    print("#", end="")
                elif(y == 2 and x == 10):
                    print("#", end="")
                elif(y == 6 and x == 4):
                    print("#", end="")
                elif(y == 6 and x == 10):
                    print("#", end="")
                else:
                    print(" ", end="")
    # ROLL 5
            if(roll == 5):
                if(y == 1 or y == 7):
                    print("#", end="")
                elif(x == 1 or x == 13):
                    print("#", end="")
                # DICE THROW
                elif(y == 2 and x == 4):
                    print("#", end="")
                elif(y == 2 and x == 10):
                    print("#", end="")
                elif(y == 4 and x == 7):
                    print("#", end="")
                elif(y == 6 and x == 4):
                    print("#", end="")
                elif(y == 6 and x == 10):
                    print("#", end="")
                else:
                    print(" ", end="")
    # ROLL 6
            if(roll == 6):
                if(y == 1 or y == 7):
                    print("#", end="")
                elif(x == 1 or x == 13):
                    print("#", end="")
                # DICE THROW
                elif(y == 2 and x == 4):
                    print("#", end="")
                elif(y == 2 and x == 10):
                    print("#", end="")
                elif(y == 4 and x == 4):
                    print("#", end="")
                elif(y == 4 and x == 10):
                    print("#", end="")
                elif(y == 6 and x == 4):
                    print("#", end="")
                elif(y == 6 and x == 10):
                    print("#", end="")
                else:
                    print(" ", end="")

            x = x + 1
        y = y + 1
        print("")
def diceroll():
    for i in range(1,6):
        os.system("cls")
        x = 1
        while(x <= dice_number):
            dice()
            print("")
            x = x + 1
        time.sleep(0.1)
while(N == ""):
    N = input("Press enter to roll the dice.\nType \'x\' to exit the dice program. ")
    os.system('cls')
    if(N == ""):
        diceroll()