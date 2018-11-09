for i in range(cols):
    c = i
    r = 0
    lst = []
    while c <= cols - 1 and r <= rows - 1:
        lst.append(mat[r][c])
        c += 1
        r += 1

    counter = 0
    for i in range(len(lst)-1):
        if lst[i] == lst[i+1] and lst[i] != 0:
            counter += 1
            if counter >= wins-1:
                diag_right_win = True
                player = lst[i]
                break
        else:
            counter = 0

    for i in range(1, cols):

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
                x_new = x + 1
                y_new = y + 1
                # Check if x_new, y_new exceed the matrix bounds
                r, c = mat.shape
                if x_new < r and y_new < c:
                    return (x_new, y_new)
                else:
                    return False

            p1counter = 0  # keeps track of player 1's score
            p2counter = 0  # keeps track of player 2's score
            result = (0, 0)

            r, c = mat.shape
            # generate a list of starting_coords to loop over
            starting_coords = []
            for i in range(0, r):
                if (r - i) >= wins:
                    starting_coords.append((i, 0))
            for j in range(1, c):
                if (c - j) >= wins:
                    starting_coords.append((0, j))
            # starting_coords is a list of tuples representing the initial coordinates of each diagonal
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
