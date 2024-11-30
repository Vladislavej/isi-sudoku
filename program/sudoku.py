import tkinter as tk
from tkinter import messagebox
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
                random.shuffle(numbers)  #shuffle numbers
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


def solve_with_backtracking(board, size):
    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                for num in range(1, size + 1):
                    if is_valid(board, row, col, num, size):
                        board[row][col] = num
                        if solve_with_backtracking(board, size):
                            return True
                        board[row][col] = 0
                return False
    return True


def solve_with_dfs(board, size):
    stack = [(board, 0, 0)]  # Stack holds (current board, row, col)
    while stack:
        current_board, row, col = stack.pop()
        if row == size:  # Completed the board
            for r in range(size):
                for c in range(size):
                    board[r][c] = current_board[r][c]
            return True

        next_row, next_col = (row + (col + 1) // size, (col + 1) % size)
        if current_board[row][col] != 0:
            stack.append((current_board, next_row, next_col))
        else:
            for num in range(1, size + 1):
                if is_valid(current_board, row, col, num, size):
                    new_board = [row[:] for row in current_board]
                    new_board[row][col] = num
                    stack.append((new_board, next_row, next_col))
    return False


def solve_with_forward_checking(board, size):
    def forward_check(board, size):
        possibilities = [[[num for num in range(1, size + 1) if is_valid(board, row, col, num, size)]
                          if board[row][col] == 0 else []
                          for col in range(size)] for row in range(size)]
        return possibilities

    def forward_check_solve(board, size, possibilities):
        empty_cells = [(row, col) for row in range(size) for col in range(size) if board[row][col] == 0]
        if not empty_cells:
            return True

        empty_cells.sort(key=lambda cell: len(possibilities[cell[0]][cell[1]]))  # Sort by fewest possibilities
        row, col = empty_cells[0]

        for num in possibilities[row][col]:
            if is_valid(board, row, col, num, size):
                board[row][col] = num
                new_possibilities = forward_check(board, size)
                if forward_check_solve(board, size, new_possibilities):
                    return True
                board[row][col] = 0

        return False

    possibilities = forward_check(board, size)
    return forward_check_solve(board, size, possibilities)


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")

        self.size = 9  # default size (9x9)
        self.board = []
        self.original_board = []

        self.create_widgets()

    def create_widgets(self):
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=10)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack()

        self.generate_button = tk.Button(self.buttons_frame, text="Generate", command=self.generate_board)
        self.generate_button.grid(row=0, column=0, padx=5, pady=5)

        #dropdown for solve algorithms
        self.solve_alg_var = tk.StringVar(value="Backtracking")
        self.solve_alg_menu = tk.OptionMenu(self.buttons_frame, self.solve_alg_var, "Backtracking", "DFS", "Forward Checking")
        self.solve_alg_menu.grid(row=0, column=1, padx=5, pady=5)

        self.solve_button = tk.Button(self.buttons_frame, text="Solve", command=self.solve_board)
        self.solve_button.grid(row=0, column=2, padx=5, pady=5)

        self.check_button = tk.Button(self.buttons_frame, text="Check", command=self.check_board)
        self.check_button.grid(row=0, column=3, padx=5, pady=5)

        # Difficulty and size
        self.difficulty_var = tk.StringVar(value="Easy")
        self.difficulty_menu = tk.OptionMenu(self.buttons_frame, self.difficulty_var, "Easy", "Medium", "Hard")
        self.difficulty_menu.grid(row=1, column=0, columnspan=2, pady=5)

        self.size_var = tk.StringVar(value="9x9")
        self.size_menu = tk.OptionMenu(self.buttons_frame, self.size_var, "4x4", "9x9")
        self.size_menu.grid(row=1, column=2, columnspan=2, pady=5)

    def generate_board(self):
        self.size = 4 if self.size_var.get() == "4x4" else 9
        difficulty = self.difficulty_var.get()
        if self.size == 4:
            num_holes = {"Easy": self.size * 1, "Medium": self.size * 2, "Hard": self.size * 3}[difficulty]
        else:
            num_holes = {"Easy": self.size * 2, "Medium": self.size * 3, "Hard": self.size * 4}[difficulty]


        random.seed(time.time())

        valid_board = False
        while not valid_board:
            self.board = generate_sudoku(self.size)
            self.original_board = [row[:] for row in self.board]
            remove_numbers(self.board, num_holes, self.size)

            valid_board = is_valid_board(self.board, self.size)

        self.display_board()

    def display_board(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.entries = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                entry = tk.Entry(self.grid_frame, width=2, font=("Arial", 18), justify="center")
                entry.grid(row=i, column=j, padx=5, pady=5)
                if self.board[i][j] != 0:
                    entry.insert(0, str(self.board[i][j]))
                    entry.config(state="disabled")
                row.append(entry)
            self.entries.append(row)

    def solve_board(self):
        algorithm = self.solve_alg_var.get()
        solving_methods = {
            "Backtracking": solve_with_backtracking,
            "DFS": solve_with_dfs,
            "Forward Checking": solve_with_forward_checking,
        }
        solving_method = solving_methods[algorithm]

        board_copy = [row[:] for row in self.board]
        if solving_method(board_copy, self.size):
            self.board = board_copy
            self.display_board()
        else:
            messagebox.showerror("Error", f"No solution exists using {algorithm}!")

    def check_board(self):
        for i in range(self.size):
            for j in range(self.size):
                try:
                    value = int(self.entries[i][j].get())
                except ValueError:
                    messagebox.showerror("Error", "Invalid input! All cells must have numbers.")
                    return
                self.board[i][j] = value

        solved_board = [row[:] for row in self.original_board]
        if solve_sudoku(solved_board, self.size) and self.board == solved_board:
            messagebox.showinfo("Success", "Congratulations! The board is solved correctly!")
        else:
            messagebox.showerror("Error", "The board is incorrect!")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
