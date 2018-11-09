import numpy as np
import pdb
# pdb.set_trace()


class Game:
    mat = None
    rows = 0
    cols = 0
    turn = 0
    wins = 0


def check_victory(game):
    winners = []

    def check_diagonals(game, mat):
        starting_coords = []
        for i in range(0, game.rows):
            starting_coords.append((i, 0))
        for j in range(1, game.cols):
            starting_coords.append((0, j))
        # starting_coords is a list of tuples representing the start of each diagonal
        for (x, y) in starting_coords:
            # collector collects consecutive numbers that are the same
            collector = []
            while x < game.rows and y < game.cols:
                cell_num = mat[x][y]
                if len(collector) == 0 or collector[0] == cell_num:
                    collector.append(cell_num)
                else:
                    collector = []
                    collector.append(cell_num)
                if len(collector) >= game.wins and collector[0] != 0:
                    winners.append(collector[0])
                x += 1
                y += 1
        return winners

    def check_horizontals(game, mat):
        for row in mat:
            collector = []
            for cell_num in row:
                if len(collector) == 0 or collector[0] == cell_num:
                    collector.append(cell_num)
                else:
                    collector = []
                    collector.append(cell_num)
                if len(collector) >= game.wins and collector[0] != 0:
                    winners.append(collector[0])
        return winners

    check_horizontals(game, game.mat)  # check rows
    check_horizontals(game, np.transpose(game.mat))  # check columns
    check_diagonals(game, game.mat)  # check diagonal down
    check_diagonals(game, np.fliplr(game.mat))  # check diagonal up
    if len(winners) == 0:
        winner = 0
    elif game.turn in winners:
        # if the turn player is inside the winner list, winner is the turn player
        winner = game.turn
    else:
        # else take winner as the first player in the winners list
        winner = winners[0]
    return winner


def apply_move(game, col, pop):
    def copy_game(game):
        game2 = Game()
        game2.mat = np.copy(game.mat)
        game2.rows = game.rows
        game2.cols = game.cols
        game2.turn = game.turn
        game2.wins = game.wins
        return game2

    # copy_game() is needed to create duplicate of the game
    # so that the copy can be changed without affecting the original
    game2 = copy_game(game)

    # We can access a 2D array row by row but not column by column,
    # So we transpose the 2D array such that the columns are now rows
    mat = game2.mat.transpose()

    # Extract the column we want from mat as game2_col
    mat_col = mat[col]
    mat_col_len = len(mat_col)
    # Depending on whether pop or push, alter mat_col accordingly
    if pop:
        # shift everything down by one element and insert a 0 at the start
        mat_col = np.insert(mat_col[0:-1], 0, 0)
    else:
        # cascade the pushed player piece down until it hits an obstacle
        for i in range(mat_col_len):
            if i == (mat_col_len - 1) or mat_col[i] == 0 and mat_col[i+1] != 0:
                mat_col[i] = game2.turn
                break
    # Overwrite mat[col] with our updated mat_col
    mat[col] = mat_col
    # Remember to convert the rows backs into columns
    game2.mat = mat.transpose()
    return game2


def check_move(game, col, pop):
    mat = game.mat.transpose()
    if col >= game.cols:
        return False
    else:
        game_col = mat[col]
        if pop:
            return game_col[-1] != 0
        else:
            return game_col[0] == 0


def computer_move(game, level):
    def copy_game(game):
        game2 = Game()
        game2.mat = np.copy(game.mat)
        game2.rows = game.rows
        game2.cols = game.cols
        game2.turn = game.turn
        game2.wins = game.wins
        return game2
    # possible_moves is a list of (col, pop) tuples representing all the valid moves the computer can make
    possible_moves = []
    for i in range(game.cols):
        if check_move(game, i, True):
            possible_moves.append((i, True))
        if check_move(game, i, False):
            possible_moves.append((i, False))
    possible_moves_len = len(possible_moves)
    if level == 1:
        # pick a random move from possible_moves
        i = np.random.randint(0, possible_moves_len)
        print("computer moves randomly")
        return possible_moves[i]

    elif level == 2:
        # check if a winning move exists
        for move in possible_moves:
            col, pop = move
            future_game = apply_move(game, col, pop)
            future_winner = check_victory(future_game)
            if future_winner == future_game.turn:
                print("computer notices a winning move")
                return move
        # if no winning move exists, check if a winning move exists for the opponent
        for move in possible_moves:
            col, pop = move
            # game2 = copy_game(game)
            # game2.turn = 1
            # future_game = apply_move(game2, col, pop)
            game.turn = 1
            future_game = apply_move(game, col, pop)
            game.turn = 2
            future_winner = check_victory(future_game)
            if future_winner != 0 and future_winner != future_game.turn:
                print("computer blocks a winning move")
                return move
        i = np.random.randint(0, possible_moves_len)
        print("computer moves randomly")
        return possible_moves[i]


def display_board(game):
    print()
    print(game.mat)
    print()
    return


def menu():
    def next_turn(game):
        if game.turn == 1:
            game.turn = 2
        elif game.turn == 2:
            game.turn = 1
    game = Game()
    # print("Hello, please answer the following questions:")
    # game.rows = int(input("How many rows?"))
    # game.cols = int(input("How many columns?"))
    # game.wins = int(input("How many pieces in a row to win?"))
    game.mat = np.zeros((6, 6), dtype=np.int8)
    game.wins = 4
    game.turn = 1
    game.rows = 6
    game.cols = 6
    display_board(game)
    while check_victory(game) == 0:
        print("Player {}".format(game.turn))

        # if it's turn 2, the computer moves
        if game.turn == 2:
            col, pop = computer_move(game, 2)
        # if it's turn 1, player gets to move
        else:
            col = int(input("which column? "))
            if col < 1 or col > game.cols:
                print("Sorry, that falls outside the column values of 1 to {}".format(game.cols))
                continue
            else:
                col -= 1
            pop = input("pop? (y/n)")
            pop = True if pop == "y" else False

        if check_move(game, col, pop):
            game = apply_move(game, col, pop)
        else:
            print("That move is not aloud")
        display_board(game)
        next_turn(game)
    print("Player {} wins".format(check_victory(game)))
    return


menu()
