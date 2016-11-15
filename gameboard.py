board_width = int(input("What size will the gameboard be? "))

def print_hor():
    print(("+ - - - " * board_width) + "+")

def print_ver():
    print("|       " * (board_width + 1))
    print("|       " * (board_width + 1))
    print("|       " * (board_width + 1))

for i in range(0, board_width):
    print_hor()
    print_ver()
print_hor()