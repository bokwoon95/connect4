import numpy as np


class Game:
    mat = None  # this represents the board matrix
    rows = 0  # this represents the number of rows of the board
    cols = 0  # this represents the number of columns of the board
    turn = 0  # this represents whose turn it is (1 for player 1, 2 for player 2)
    wins = 0  # this represents the number of consecutive disks you need to force in order to win

    def check_victory(game):
        """
        Check if victory condition has been reached.
        Takes in a game object as input and returns
        1 if player 1 wins
        2 if player 2 wins
        3 if it's a draw
        0 otherwise
        """

        def check_diagonals(mat, wins):
            """
            Given a list of starting coordinates for diagonals and an iterator function for coordinates,
            scan the matrix until a winning combination is first found,
            then return winner
            else return 0
            """
            def next_diagonal_cell(mat, x, y):
                """
                Given the current x & y coords,
                finds the next VALID Top->Down Left->Right diagonal cell within the matrix
                else returns False
                """
                r, c = mat.shape
                x_new = x + 1
                y_new = y + 1
                # Check if x_new, y_new exceed the matrix bounds
                if x_new < r and y_new < c:
                    return (x_new, y_new)
                else:
                    return False

            p1counter = 0  # keeps track of player 1's score
            p2counter = 0  # keeps track of player 2's score
            result = (0, 0)

            r, c = mat.shape
            # generate a list of starting_coords to loop over
            # starting_coords is a list of tuples representing the initial coordinate of each diagonal
            starting_coords = []
            for i in range(0, r):
                if (r - i) >= wins:
                    starting_coords.append((i, 0))
            for j in range(1, c):
                if (c - j) >= wins:
                    starting_coords.append((0, j))

            for x, y in starting_coords:
                while True:
                    if mat[x][y] == 1:
                        p1counter += 1
                    elif mat[x][y] == 2:
                        p2counter += 1
                    else:
                        p1counter = 0
                        p2counter = 0

                    p1wins = p1counter >= wins
                    p2wins = p2counter >= wins
                    if p1wins or p2wins:
                        if p1wins and p2wins:
                            result = (1, 1)
                        elif p1wins:
                            result = (1, 0)
                        elif p2wins:
                            result = (0, 1)
                        else:
                            result = (0, 0)
                        break

                    # obtain the next diagonal cell based on the current x,y
                    next_cell = next_diagonal_cell(mat, x, y)

                    # if next_cell is valid, unpack the new x & y coords
                    if next_cell:
                        x, y = next_cell
                    # if next_cell is invalid, break out of the while True loop
                    else:
                        p1wins = p1counter >= wins
                        p2wins = p2counter >= wins
                        if p1wins or p2wins:
                            if p1wins and p2wins:
                                result = (1, 1)
                            elif p1wins:
                                result = (1, 0)
                            elif p2wins:
                                result = (0, 1)
                            else:
                                result = (0, 0)
                            break

                # if the winner is found, break out of the for loop
                if result != (0, 0):
                    break
            return result

        def check_horizontals(mat):
            r, c = mat.shape
            p1counter = 0
            p2counter = 0
            result = (0, 0)
            for row in mat:
                for num in row:
                    if num == 1:
                        p1counter += 1
                    if num == 2:
                        p2counter += 1
                    else:
                        p1counter = 0
                        p2counter = 0

                p1wins = p1counter >= wins
                p2wins = p2counter >= wins
                if p1wins or p2wins:
                    if p1wins and p2wins:
                        result = (1, 1)
                    elif p1wins:
                        result = (1, 0)
                    elif p2wins:
                        result = (0, 1)
                    else:
                        result = (0, 0)
                    break

            return result

        ra = [2, 1, 1, 1, 0, 0]
        rb = [0, 2, 0, 0, 0, 0]
        rc = [0, 0, 2, 0, 0, 0]
        rd = [0, 0, 0, 2, 0, 0]
        re = [0, 0, 1, 0, 2, 0]
        rf = [0, 0, 0, 1, 0, 2]
        mat = np.array([ra, rb, rc, rd, re, rf])
        mat
        mat = game.mat

        # check rows for a winner
        row_winner = check_horizontals(mat)
        if row_winner != 0:
            return row_winner

        # check columns for a winner
        col_winner = check_horizontals(mat.transpose())
        if col_winner != 0:
            return col_winner

        # check top->down left->right (td_lr) diagonals for a winner
        td_lr_winner = check_diagonals(mat, wins)
        if td_lr_winner != 0:
            return td_lr_winner

        # check top->down right->left (td_rl) diagonals for a winner
        td_rl_winner = check_diagonals(np.fliplr(mat), wins)
        if td_rl_winner != 0:
            return td_rl_winner

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
# next_TD_RL_diagonal(mat, 4, 3)

# test for generate_TD_LR_starting_coords()
# generate_TD_LR_starting_coords(6, 6, 4)

# test for generate_TD_RL_starting_coords()
# generate_TD_RL_starting_coords(6, 6, 4)

# tests for check_diagonal
ra = [1, 1, 1, 1, 0, 0]
rb = [0, 1, 0, 0, 0, 0]
rc = [0, 0, 1, 0, 0, 0]
rd = [0, 0, 0, 1, 0, 0]
re = [0, 0, 1, 0, 1, 0]
rf = [0, 0, 0, 1, 0, 1]
mat = np.array([ra, rb, rc, rd, re, rf])
mat
# starting_coords = generate_TD_LR_starting_coords(6, 6, 4)
# starting_coords
# winner = check_diagonals(mat, starting_coords, next_TD_LR_diagonal)
# winner

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
