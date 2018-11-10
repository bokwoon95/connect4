import numpy as np


class Game:
    mat = None
    rows = 0
    cols = 0
    turn = 0
    wins = 0


def copy_game(game):
    game2 = Game()
    game2.mat = np.copy(game.mat)
    game2.rows = game.rows
    game2.cols = game.cols
    game2.turn = game.turn
    game2.wins = game.wins
    return game2


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

    def check_draw(game, mat):
        for row in mat:
            for cell_num in row:
                if cell_num == 0:
                    return False
        return True

    if check_draw(game, game.mat):
        return 3

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
    # copy_game() is needed to create duplicate of the game
    # so that the copy can be changed without affecting the original
    game2 = copy_game(game)

    # We can access a 2D array row by row but not column by column,
    # So we transpose the 2D array such that the columns are now rows
    mat = game2.mat.transpose()

    # Depending on whether pop or push, alter mat_col accordingly
    if pop:
        # shift everything down by one element and insert a 0 at the start
        mat[col] = np.insert(mat[col][0:-1], 0, 0)
    else:
        # cascade the pushed player piece down until it hits an obstacle
        for i in range(len(mat[col])):
            if i == (len(mat[col]) - 1) or mat[col][i] == 0 and mat[col][i+1] != 0:
                mat[col][i] = game2.turn
                break
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
            return game_col[-1] == game.turn
        else:
            return game_col[0] == 0


def computer_move(game, level):

    def generate_possible_moves(game):
        possible_moves = []
        for i in range(game.cols):
            if check_move(game, i, True):
                possible_moves.append((i, True))
            if check_move(game, i, False):
                possible_moves.append((i, False))
        return possible_moves

    # possible_moves[] is a list of (col, pop) tuples representing all the valid moves the computer can make
    possible_moves = generate_possible_moves(game)
    possible_moves_avoid_direct_loss = []
    possible_moves_avoid_future_loss = []

    if level == 1:
        # pick a random move from possible_moves
        i = np.random.randint(0, len(possible_moves))
        print("computer moves randomly")
        return possible_moves[i]

    elif level == 2:
        for move in possible_moves:
            col, pop = move
            future_game = apply_move(game, col, pop)
            future_game.turn = 1
            future_winner = check_victory(future_game)

            if future_winner == 2:
                print("computer notices a winning move")
                return move

            # if the human player doesn't win as an outcome of this computer move,
            # add it to the list of moves that avoid direct loss
            if future_winner != 1:
                possible_moves_avoid_direct_loss.append(move)

            # if nobody wins as an outcome of this computer move,
            # and the human also won't be able to win on their next turn,
            # add it to the list of moves that avoid future loss
            if future_winner == 0:
                human_wins = False
                possible_countermoves = generate_possible_moves(future_game)
                for countermove in possible_countermoves:
                    ccol, cpop = countermove
                    future_future_game = apply_move(future_game, ccol, cpop)
                    if check_victory(future_future_game) == 1:
                        human_wins = True
                        break
                if not human_wins:
                    possible_moves_avoid_future_loss.append(move)

        if len(possible_moves_avoid_future_loss) != 0:
            # If there exists a move that avoids future loss, play it
            i = np.random.randint(0, len(possible_moves_avoid_future_loss))
            move = possible_moves_avoid_future_loss[i]
            print(possible_moves_avoid_future_loss)
            print("computer moves {}".format(move))
            return move
        else:
            # Otherwise play a random move that avoids direct loss
            i = np.random.randint(0, len(possible_moves_avoid_direct_loss))
            move = possible_moves_avoid_direct_loss[i]
            print("computer moves randomly {}".format(move))
            print(possible_moves_avoid_direct_loss)
            return move


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
            try:
                col = int(input("which column? "))
            except ValueError:
                print("Only integers are accepted")
                continue
            if col < 1 or col > game.cols:
                print("Sorry, that falls outside the column values of 1 to {}".format(game.cols))
                continue
            else:
                # the player uses 1-based indexing so subtract 1 to get 0-based index
                col -= 1
            pop = input("pop (y/n)? ")
            pop = True if pop == "y" else False

        if check_move(game, col, pop):
            game = apply_move(game, col, pop)
        else:
            print("That move is not aloud")
            continue
        display_board(game)
        next_turn(game)

    # check if game is draw
    if check_victory(game) == 3:
        print("The game is a draw")
        return

    print("Player {} wins".format(check_victory(game)))
    return


menu()
