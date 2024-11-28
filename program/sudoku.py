import random, time


def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True


def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                numbers = list(range(1, 10))
                random.shuffle(numbers)
                for num in numbers:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def generate_sudoku():
    board = [[0] * 9 for _ in range(9)]
    solve_sudoku(board)
    return board


def remove_numbers(board, num_holes):
    holes = set()
    while len(holes) < num_holes:
        i, j = random.randint(0, 8), random.randint(0, 8)
        if (i, j) not in holes:
            holes.add((i, j))
            board[i][j] = 0
    return board


if __name__ == "__main__":
    random.seed(time.time())
    sudoku_board = generate_sudoku()
    puzzle = remove_numbers(sudoku_board, 0)
    for row in puzzle:
        print(row)
