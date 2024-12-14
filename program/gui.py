import random
import time
import tkinter as tk
from tkinter import messagebox

from program.logic import generate_sudoku, remove_numbers, is_valid_board, solve_sudoku, solve_with_backtracking, solve_with_dfs, solve_with_forward_checking

CELL_SIZE = 40
LINE_WIDTH = 3

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")

        self.root.geometry("450x600")
        self.root.resizable(False, False)

        self.size = 9
        self.board = []
        self.original_board = []
        self.initial_board = []
        self.delay = 100  # default delay in milliseconds
        self.start_time = None
        self.timer_running = False
        self.last_updated_cell = None

        self.create_widgets()
        self.generate_board()

    def create_widgets(self):
        self.grid_frame = tk.Frame(self.root, bg="lightgray")
        self.grid_frame.pack(pady=10)

        self.buttons_frame = tk.Frame(self.root, bg="lightgray")
        self.buttons_frame.pack()

        self.generate_button = tk.Button(self.buttons_frame, text="Generate", command=self.generate_board, bg="white")
        self.generate_button.grid(row=0, column=0, padx=5, pady=5)

        self.solve_alg_var = tk.StringVar(value="Backtracking")
        self.solve_alg_menu = tk.OptionMenu(self.buttons_frame, self.solve_alg_var, "Backtracking", "DFS", "Forward Checking")
        self.solve_alg_menu.config(bg="white")
        self.solve_alg_menu.grid(row=1, column=1, padx=5, pady=5)

        self.solve_button = tk.Button(self.buttons_frame, text="Solve", command=self.solve_board, bg="lightgreen")
        self.solve_button.grid(row=1, column=0, padx=5, pady=5)

        self.check_button = tk.Button(self.buttons_frame, text="Check", command=self.check_board, bg="white")
        self.check_button.grid(row=0, column=3, padx=5, pady=5)

        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_board, bg="lightcoral")
        self.reset_button.grid(row=0, column=4, padx=5, pady=5)

        self.difficulty_var = tk.StringVar(value="Easy")
        self.difficulty_menu = tk.OptionMenu(self.buttons_frame, self.difficulty_var, "Easy", "Medium", "Hard")
        self.difficulty_menu.config(bg="white")
        self.difficulty_menu.grid(row=0, column=2, pady=5)

        self.size_var = tk.StringVar(value="9x9")
        self.size_menu = tk.OptionMenu(self.buttons_frame, self.size_var, "4x4", "9x9")
        self.size_menu.config(bg="white")
        self.size_menu.grid(row=0, column=1, pady=5)

        self.delay_scale = tk.Scale(self.buttons_frame, from_=0, to=200, orient=tk.HORIZONTAL, label="Delay (ms)", command=self.update_delay, bg="white")
        self.delay_scale.set(self.delay)
        self.delay_scale.grid(row=1, column=2, columnspan=4, pady=5)

        self.time_label = tk.Label(self.buttons_frame, text="Time: 0s", bg="white")
        self.time_label.grid(row=2, column=0, padx=10, pady=10)

        self.step_label = tk.Label(self.buttons_frame, text="Steps: 0", bg="white")
        self.step_label.grid(row=2, column=1, padx=10, pady=10)

    def update_delay(self, value):
        self.delay = int(value)

    def generate_board(self):
        self.last_updated_cell = None
        self.size = 4 if self.size_var.get() == "4x4" else 9
        num_holes = self.get_num_holes()

        random.seed(time.time())

        valid_board = False
        while not valid_board:
            self.board = generate_sudoku(self.size)
            self.original_board = [row[:] for row in self.board]
            remove_numbers(self.board, num_holes, self.size)

            valid_board = is_valid_board(self.board, self.size)

        self.initial_board = [row[:] for row in self.board]
        self.display_board()

    def get_num_holes(self):
        difficulty = self.difficulty_var.get()
        if self.size == 4:
            return {"Easy": self.size * 1, "Medium": self.size * 2, "Hard": self.size * 3}[difficulty]
        else:
            return {"Easy": self.size * 3, "Medium": self.size * 5, "Hard": self.size * 7}[difficulty]

    def reset_board(self):
        self.board = [row[:] for row in self.initial_board]
        self.display_board()

    def display_board(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.entries = []
        subgrid_size = int(self.size ** 0.5)

        canvas = tk.Canvas(self.grid_frame, width=self.size * CELL_SIZE, height=self.size * CELL_SIZE)
        canvas.grid(row=0, column=0, columnspan=self.size, rowspan=self.size)

        for i in range(self.size):
            row = []
            for j in range(self.size):
                entry = tk.Entry(self.grid_frame, width=2, font=("Arial", 18), justify="center", bg="lightyellow")
                entry.place(x=j * CELL_SIZE + 2, y=i * CELL_SIZE + 2, width=36, height=36)
                if self.board[i][j] != 0:
                    entry.insert(0, str(self.board[i][j]))
                    entry.config(state="disabled", disabledbackground="white")
                row.append(entry)
            self.entries.append(row)

        for i in range(self.size):
            width = LINE_WIDTH if i % subgrid_size == 0 else 1
            canvas.create_line(0, i * CELL_SIZE, self.size * CELL_SIZE, i * CELL_SIZE, width=width)
            canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, self.size * CELL_SIZE, width=width)

    def update_board(self, board):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != board[i][j]:
                    if self.last_updated_cell:
                        last_i, last_j = self.last_updated_cell
                        self.entries[last_i][last_j].config(bg="lightyellow")  # Reset the last updated cell color

                    self.entries[i][j].delete(0, tk.END)
                    if board[i][j] != 0:
                        self.entries[i][j].insert(0, str(board[i][j]))
                    self.entries[i][j].config(bg="red")
                    self.last_updated_cell = (i, j)  # Update the last updated cell

    def update_step_label(self, steps):
        self.step_label.config(text=f"Steps: {steps[0]}")
        self.update_time_label()

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_time_label()

    def update_time_label(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            seconds = int(elapsed_time)
            milliseconds = int((elapsed_time - seconds) * 1000)
            self.time_label.config(text=f"{seconds}.{milliseconds:03d}s")

    def solve_board(self):
        algorithm = self.solve_alg_var.get()
        solving_methods = {
            "Backtracking": solve_with_backtracking,
            "DFS": solve_with_dfs,
            "Forward Checking": solve_with_forward_checking,
        }
        solving_method = solving_methods[algorithm]

        board_copy = [row[:] for row in self.board]
        steps = [0]
        self.start_timer()

        if solving_method(board_copy, self.size, self, self.delay, steps):
            self.board = board_copy
            self.display_board()
            messagebox.showinfo("Statistics", f"Finished using {algorithm}!")
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