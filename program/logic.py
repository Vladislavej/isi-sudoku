import random

def is_valid(board, row, col, num, size):
    subgrid_size = int(size ** 0.5)
    for i in range(size):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = subgrid_size * (row // subgrid_size), subgrid_size * (col // subgrid_size)
    for i in range(start_row, start_row + subgrid_size):
        for j in range(start_col, start_col + subgrid_size):
            if board[i][j] == num:
                return False
    return True


def solve_sudoku(board, size):
    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                numbers = list(range(1, size + 1))
                random.shuffle(numbers)
                for num in numbers:
                    if is_valid(board, row, col, num, size):
                        board[row][col] = num
                        if solve_sudoku(board, size):
                            return True
                        board[row][col] = 0
                return False
    return True


def generate_sudoku(size):
    board = [[0] * size for _ in range(size)]
    solve_sudoku(board, size)
    return board


def remove_numbers(board, num_holes, size):
    holes = set()
    while len(holes) < num_holes:
        i, j = random.randint(0, size - 1), random.randint(0, size - 1)
        if (i, j) not in holes:
            holes.add((i, j))
            board[i][j] = 0
    return board


def is_valid_board(board, size):
    return solve_sudoku([row[:] for row in board], size)

def is_valid_solution(board, size):
    def is_valid_row(row):
        return len(set(row)) == len(row) - row.count(0)

    def is_valid_col(col):
        col_values = [board[row][col] for row in range(size)]
        return len(set(col_values)) == len(col_values) - col_values.count(0)

    def is_valid_box(start_row, start_col):
        box_values = []
        box_size = int(size ** 0.5)
        for r in range(start_row, start_row + box_size):
            for c in range(start_col, start_col + box_size):
                box_values.append(board[r][c])
        return len(set(box_values)) == len(box_values) - box_values.count(0)

    for i in range(size):
        if not is_valid_row(board[i]) or not is_valid_col(i):
            return False

    box_size = int(size ** 0.5)
    for r in range(0, size, box_size):
        for c in range(0, size, box_size):
            if not is_valid_box(r, c):
                return False

        return True

def solve_with_backtracking(board, size, gui, delay, steps):
    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                for num in range(1, size + 1):
                    if is_valid(board, row, col, num, size):
                        board[row][col] = num
                        gui.update_board(board)
                        gui.root.update_idletasks()
                        gui.root.after(delay)
                        steps[0] += 1
                        gui.update_step_label(steps)
                        if solve_with_backtracking(board, size, gui, delay, steps):
                            return True
                        board[row][col] = 0
                        gui.update_board(board)
                        gui.root.update_idletasks()
                        gui.root.after(delay)
                        steps[0] += 1
                return False
    return True


def solve_with_dfs(board, size, gui, delay, steps):
    def dfs(row, col):
        if row == size:
            return is_valid_solution(board, size)

        next_row, next_col = (row + (col + 1) // size, (col + 1) % size)

        if board[row][col] != 0:
            return dfs(next_row, next_col)

        for num in range(1, size + 1):
            board[row][col] = num

            gui.update_board(board)
            gui.root.update_idletasks()
            gui.root.after(delay)
            steps[0] += 1
            gui.update_step_label(steps)
            if dfs(next_row, next_col):
                return True

            board[row][col] = 0

        return False

    return dfs(0, 0)


def solve_with_forward_checking(board, size, gui, delay, steps):
    return False