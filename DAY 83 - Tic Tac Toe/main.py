# import ascii source and cls
from math import e
import ascii as asc
from os import system
from random import randint, choice

# custom class to catch invalid index specification in row and column
class OutOfBoundsError(IndexError):
    def __init__(self):            
        # Call the base class constructor with the parameters it needs
        super().__init__()

# turn into array
x_ascii = asc.x_ascii.splitlines()
o_ascii = asc.o_ascii.splitlines()

GAME_STATE = 'start'
O_SYMBOL = 'O'
X_SYMBOL = 'X'

# array to hold the values of X and O in the table
array = [None for i in range(9)]


# function to draw each row in tic-tac-toe table
def draw_row(row, marker):

    print()

    for i in range(4):
        for j in range(3):
            if row[j] == None:
                print("       ", end='')
            elif row[j] == X_SYMBOL:
                print(x_ascii[i], end='')
            elif row[j] == O_SYMBOL:
                print(o_ascii[i], end='')
        
            if j != 2:
                print("|", end='')

        if i == 1:
            print(f" {marker + 1}")
        else:
            print()
    
    for i in range(23):
        print("_", end='')
    
    print()


# function to draw table
def draw_table(table):
    for i in range(3):
        print(f"   {i + 1}    ", end="")


    for i in range(3):
        draw_row(table[(i * 3): (i * 3) + 3], i)


# function to check values on table
# returns True if there is already a win detected for specified symbol
def check(table, symbol):

    flag = 0

    # diagonal cases
    d1 = [table[0], table[4], table[8]]
    d2 = [table[2], table[4], table[6]]

    if d1.count(symbol) == 3 or d2.count(symbol) == 3:
        return True

    # check for horizontal matches
    for i in range(3):
        for j in range(i * 3, (i * 3) + 3):
            if table[j] == symbol:
                flag += 1
        
        if flag == 3:
            return True
        
        flag = 0
    
    # check for vertical matches
    for i in range(3):
        for j in range(3):
            if table[i + (j * 3)] == symbol:
                flag += 1
        
        if flag == 3:
            return True

        flag = 0

    return False

# might as well make a function since it gets repetitive
def put(table, index, symbol) -> bool:
    table[index] = symbol

    if check(table, symbol):
        return True
    return False


# for better game flow
player_win = False
enemy_win = False
repeat = False

# game start
while GAME_STATE != 'over':
    system('cls')

    # game instructions
    if GAME_STATE == 'start':
        print("Welcome to Tic Tac Toe!")
        player_symbol = (input("Pick a symbol (O/X): ")).upper()
        
        if player_symbol == X_SYMBOL:
            enemy_symbol = O_SYMBOL
        elif player_symbol == O_SYMBOL:
            enemy_symbol = X_SYMBOL
        else:
            continue

        print("\n\nTo play, you would specify the row and column of the cell you want to mark by")
        print("typing it in the prompts.\n")
        print("Good luck!!")

        input("Press anything to continue.\n")

        go_first = choice([True, False])

        # switch to play state
        GAME_STATE = 'play'
        continue


    # game play state
    if GAME_STATE == 'play':


        if go_first and array.count(X_SYMBOL) == 0:
            print("\nYou are going first!")
        elif not repeat and not go_first:

            # plotting mark process and win condition checking
            enemy_win = put(array, choice([array.index(cell) for cell in array if cell == None]), enemy_symbol)

            if enemy_win:
                GAME_STATE = 'over'
                continue

            if array.count(None) == 0:
                GAME_STATE = 'over'
                continue

        
        # draw plotted data
        draw_table(array)

        # try catch statement to avoid sudden errors to interrupt game flow
        try:
            repeat = False
            
            row = int(input("\nRow: "))
            if row > 3 or row < 1:
                raise OutOfBoundsError()

            col = int(input("Col: "))
            if row > 3 or row < 1:
                raise OutOfBoundsError()

            if array[3 * (row - 1) + (col - 1)] != None:
                repeat = True
                continue

        except ValueError:
            repeat = True
            continue
        except OutOfBoundsError:
            repeat = True
            continue
        else:
            player_win = put(array, 3 * (row - 1) + (col - 1), player_symbol)

            if player_win:
                GAME_STATE = 'over'
                continue

            if array.count(None) == 0:
                GAME_STATE = 'over'
                continue


        if go_first:
            enemy_win = put(array, choice([array.index(cell) for cell in array if cell == None]), enemy_symbol)

            if enemy_win:
                GAME_STATE = 'over'
                continue
            
            if array.count(None) == 0:
                GAME_STATE = 'over'
                continue
        

system('cls')
draw_table(array)

if player_win:
    print("\n\nYou win!")
elif enemy_win:
    print("\n\nYou lose!")
else:
    print("\n\nIt's a tie!")