import random
import time


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


if __name__ == "__main__":
    random.seed(time.time())

    print("Choose Sudoku size:")
    print("1. 4x4 (2x2 subgrids)")
    print("2. 9x9 (3x3 subgrids)")

    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        size = 4  # 4x4 board
        num_holes = 0
    elif choice == "2":
        size = 9  # 9x9 board
        num_holes = 0
    else:
        print("Invalid choice. Please restart and select 1 or 2.")
        exit()

    sudoku_board = generate_sudoku(size)
    puzzle = remove_numbers(sudoku_board, num_holes, size)
    for row in puzzle:
        print(row)
