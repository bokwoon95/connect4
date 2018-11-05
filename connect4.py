import numpy as np


def next_TD_LR_diagonal(mat, x, y):
    """
    Given the current x & y coords,
    finds the next VALID Top->Down Left->Right diagonal cell
    else returns False
    """
    r, c = mat.shape
    x_new = x + 1
    y_new = y + 1
    if x_new < r and y_new < c:
        return (x_new, y_new)
    else:
        return False


def next_TD_RL_diagonal(mat, x, y):
    """
    Given the current x & y coords,
    finds the next VALID Top->Down Right->Left diagonal cell
    else returns False
    """
    r, c = mat.shape
    x_new = x + 1
    y_new = y - 1
    if x_new < r and y_new >= 0:
        return (x_new, y_new)
    else:
        return False


def generate_TD_LR_starting_coords(mat, wins):
    """
    Generates a list of initial coordinates
    to call next_TD_LR_diagonal() on
    """
    r, c = mat.shape
    starting_coords = []
    for i in range(0, r):
        if (r - i) >= wins:
            starting_coords.append((i, 0))
    for j in range(1, c):
        if (c - j) >= wins:
            starting_coords.append((0, j))
    return starting_coords


def generate_TD_RL_starting_coords(mat, wins):
    """
    Generates a list of initial coordinates
    to call next_TD_LR_diagonal() on
    """
    r, c = mat.shape
    rd = r - 1  # r_decrement
    cd = c - 1  # c_decrement
    winsd = wins - 1  # wins_decrement
    starting_coords = []
    for i in range(rd):
        if (r - i) >= wins:
            starting_coords.append((i, cd))
    for j in range(cd):
        if (j - winsd) >= 0:
            starting_coords.append((0, j))
    return starting_coords


def check_diagonals(mat, starting_coords, next_diagonal_cell):
    """
    Given a list of starting coordinates and an iterator function for coordinates,
    scan the matrix until a winning combination is first found,
    then return (winner, winning_coords)
    else return (     0,       (-1, -1))
    """
    p1counter = 0
    p2counter = 0
    # winner
    result = 0
    # last coordinates of where the winning combo was found.
    # For debugging only
    last = (-1, -1)
    # starting_coords is a list of tuples representing
    for x, y in starting_coords:
        print("")
        while True:
            print(x, y)
            # if cell(x,y) is 1, increment p1counter
            if mat[x][y] == 1:
                p1counter += 1
                # if p1counter is already 4, player 1 wins
                if p1counter >= 4:
                    result = 1
                    last = (x, y)
                    break
            # if cell(x,y) is 2, increment p2counter
            elif mat[x][y] == 2:
                p2counter += 1
                # if p2counter is already 4, player 2 wins
                if p2counter >= 4:
                    result = 2
                    last = (x, y)
                    break
            # if cell(x,y) is 0, reset both p1counter & p2counter
            else:
                p1counter = 0
                p2counter = 0
            # obtain the next_cell based on the current x,y
            #   as well as fx & fy, which affect which diagonal direction to go
            next_cell = next_diagonal_cell(mat, x, y)
            # if next_cell is valid, unpack the new x & y coords
            if next_cell:
                x, y = next_cell
            # if next_cell is invalid, break out of the while True loop
            else:
                if p1counter >= 4:
                    result = 1
                    last = (x, y)
                elif p2counter >= 4:
                    result = 2
                    last = (x, y)
                else:
                    result = 0
                break
        # if the winner is still found, break out of the for loop
        if result != 0:
            break
    return (result, last)


def check_horizontals(mat):
    r, c = mat.shape
    p1counter = 0
    p2counter = 0
    result = 0
    last = (-1, -1)
    for row in mat:
        for num in row:
            if num == 1:
                p1counter += 1
                if p1counter >= 4:
                    result = 1
                    last = (row, num)
                    break
            elif num == 2:
                p2counter += 1
                if p2counter >= 4:
                    result = 2
                    last = (row, num)
                    break
            else:
                p1counter = 0
                p2counter = 0
        if result != 0:
            break
    return (result, last)


def check_victory(mat):
    """
    Check if victory condition has been reached.
    Takes in a game object as input and returns
    1 if player 1 wins
    2 if player 2 wins
    3 if it's a draw
    0 otherwise
    """
    winner, loc = check_horizontals(mat)
    if winner != 0:
        return winner
    winner, loc = check_horizontals(mat.transpose())
    if winner != 0:
        return winner
    winner, loc = check_diagonals(mat, generate_TD_LR_starting_coords(mat, 4), next_TD_LR_diagonal)
    if winner != 0:
        return winner
    winner, loc = check_diagonals(mat, generate_TD_RL_starting_coords(mat, 4), next_TD_RL_diagonal)
    if winner != 0:
        return winner
    # check for draw
    return 0


def apply_move(game, col, pop):
    """
    Applies a certain move to the game
    Takes a game object, a column value and a boolean pop that represents the move
    It returns a game with an updated board according to that move
    """
    # We can access a 2D array row by row but not column by column,
    #   So we transpose the 2D array such that the columns are now rows
    game_t = game.transpose()
    # Extract the column we want from game_t as game_col
    game_col = game_t[col]
    game_col_len = len(game_col)
    # Depending on whether pop or push, alter game_col accordingly
    if pop:
        game_col = np.insert(game_col[0:-1], 0, 0)
    else:
        for i in range(game_col_len):
            if i == (game_col_len - 1) or game_col[i] == 0 and game_col[i+1] != 0:
                game_col[i] = 1  # toggles between 1 & 2
                break
    # Overwrite game_t[col] with our updated game_col
    game_t[col] = game_col
    # Remember to convert the rows backs into columns
    return game_t.transpose()


def check_move(game, col, pop):
    """
    Checks if a certain move is valid for a game.
    """
    game_t = game.transpose()
    if col >= cols:
        return False
    else:
        game_col = game_t[col]
        if pop:
            return game_col[-1] != 0
        else:  # push
            return game_col[0] == 0
    return "You should not reach this line of check_move()"


def computer_move(game, level):
    """
    Executes a move for the computer on the current state of the board, depending on the computer's level
    """
    return


def display_board(game):
    """
    Displays the board on the console
    """
    print("")
    print(game)
    print("")
    return


def menu():
    """
    Handles the menu interface with the user in the console.
    It's basically the main function that interacts with the user and calls the other functions accordingly
    """
    return


class Game:
    mat = None  # this represents the board matrix
    rows = 0  # this represents the number of rows of the board
    cols = 0  # this represents the number of columns of the board
    turn = 0  # this represents whose turn it is (1 for player 1, 2 for player 2)
    wins = 0  # this represents the number of consecutive disks you need to force in order to win


# Tests
# test for next_TD_RL_diagonal
ra = [1, 0, 0, 0, 0, 0]
rb = [0, 1, 0, 0, 0, 0]
rc = [0, 0, 1, 0, 0, 0]
rd = [0, 0, 0, 1, 0, 0]
re = [0, 0, 1, 0, 1, 0]
rf = [0, 0, 0, 1, 0, 1]
mat = np.array([ra, rb, rc, rd, re, rf])
mat
next_TD_RL_diagonal(mat, 4, 3)

# test for generate_TD_LR_starting_coords()
generate_TD_LR_starting_coords(6, 6, 4)

# test for generate_TD_RL_starting_coords()
generate_TD_RL_starting_coords(6, 6, 4)

# tests for check_diagonal
ra = [1, 1, 1, 1, 0, 0]
rb = [0, 1, 0, 0, 0, 0]
rc = [0, 0, 1, 0, 0, 0]
rd = [0, 0, 0, 1, 0, 0]
re = [0, 0, 1, 0, 1, 0]
rf = [0, 0, 0, 1, 0, 1]
mat = np.array([ra, rb, rc, rd, re, rf])
mat
starting_coords = generate_TD_LR_starting_coords(6, 6, 4)
starting_coords
((winner, score), last) = check_diagonals(mat, starting_coords, next_TD_LR_diagonal)
winner, score, last

# tests for apply_move
r0 = [0, 0, 0, 0, 0]
r1 = [1, 1, 1, 1, 1]
r2 = [1, 1, 1, 1, 1]
r3 = [1, 1, 1, 1, 1]
r4 = [1, 1, 1, 1, 1]
mat = np.array([r0, r1, r2, r3, r4])
mat
mat = apply_move(mat, 1, True)
mat = apply_move(mat, 1, False)
mat
mat = apply_move(mat, 0, False)
mat

mat = None  # this represents the board matrix
rows = 5  # this represents the number of rows of the board
cols = 5  # this represents the number of columns of the board
turn = 0  # this represents whose turn it is (1 for player 1, 2 for player 2)
wins = 4  # this represents the number of consecutive disks you need to force in order to win

mat = np.zeros((rows, cols), dtype=np.int8)

ra = [1, 0, 0, 0, 0, 1]
rb = [0, 1, 0, 0, 0, 1]
rc = [0, 0, 1, 0, 0, 1]
rd = [0, 0, 0, 1, 0, 1]
re = [0, 0, 1, 1, 1, 1]
rf = [0, 0, 0, 1, 0, 1]
mat = np.array([ra, rb, rc, rd, re, rf])
mat


