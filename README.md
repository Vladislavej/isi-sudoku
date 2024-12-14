# Sudoku Solver Algorithms

This document explains different algorithms used to solve Sudoku puzzles. The algorithms compared are **Backtracking**, **DFS (Depth First Search)**, and **Forward Checking**. Each of these algorithms is evaluated in terms of performance, steps required, and time taken on various Sudoku grid sizes and difficulty levels.

## Sudoku Game Overview

Sudoku is a puzzle game that is usually played on a 9x9 grid, divided into 3x3 subgrids. The goal is to fill in the grid with numbers from 1 to 9 so that:
- Each row contains all numbers from 1 to 9 without repetition.
- Each column contains all numbers from 1 to 9 without repetition.
- Each 3x3 subgrid contains all numbers from 1 to 9 without repetition.

At the start of the game, some numbers are pre-filled into the grid, and the objective is to fill in the remaining cells following these rules.

## Algorithms

### 1. **Backtracking**

Backtracking is a recursive algorithm that explores all possible values for each cell in the grid one by one:
1. **Traverse the grid**: The algorithm searches for an empty cell (marked as 0).
2. **Try values**: For each empty cell, it tests numbers from 1 to 9.
3. **Validate**: If the number satisfies the Sudoku rules (no duplicates in row, column, or 3x3 subgrid), the number is placed in the cell.
4. **Recursion**: The algorithm then proceeds to the next empty cell.
5. **Backtrack**: If no solution is found (i.e., the grid becomes invalid), the algorithm undoes the last step and tries a different number.

### 2. **DFS (Depth First Search)**

DFS is a systematic algorithm that explores the entire solution space:
1. **Try values**: For each empty cell, it tries values from 1 to 9 without checking if they satisfy the Sudoku rules immediately.
2. **Explore further**: It continues exploring other cells, even if some cells might violate the Sudoku rules.
3. **No optimization**: DFS doesn't optimize the search process, meaning it blindly explores all possibilities before determining whether the solution is valid.

### 3. **Forward Checking**

Forward Checking enhances the Backtracking algorithm by performing a preliminary check before making assignments:
1. **Check empty cells**: For each empty cell, the algorithm computes a list of possible valid numbers that can be placed in the cell.
2. **Reduce possibilities**: After each number is assigned to a cell, the algorithm updates the list of possible numbers for all other empty cells.
3. **Validate**: If any cell ends up with no valid options, the algorithm backtracks and tries a different number.
4. **Recursion**: After successfully assigning a number, the algorithm proceeds to the next empty cell.

## Algorithm Comparison

The effectiveness of each algorithm is compared based on different Sudoku grid sizes and difficulty levels.

| **Difficulty** | **Algorithm**       | **Number of Steps** | **Time**   |
|----------|---------------------|---------------------|------------|
| **Easy** | **DFS**             | 101                 | 0.201s     |
| **4x4**  | **Backtracking**    | 4                   | 0.006s     |
|          | **Forward Checking**| 4                   | 0.006s     |
| **Medium** | **DFS**             | 10,133              | 32.633s    |
| **4x4**  | **Backtracking**    | 12                  | 0.021s     |
|          | **Forward Checking**| 10                  | 0.019s     |
| **Hard** | **DFS**             | 43,981              | 141.57s    |
| **4x4**  | **Backtracking**    | 12                  | 0.037s     |
|          | **Forward Checking**| 12                  | 0.038s     |
| **Easy** | **DFS**             | 150,213             | 483.76s    |
| **9x9**  | **Backtracking**    | 31                  | 0.172s     |
|          | **Forward Checking**| 29                  | 0.166s     |
| **Medium** | **DFS**            | 486,179             | 26m 4s     |
| **9x9**  | **Backtracking**    | 131                 | 0.989s     |
|          | **Forward Checking**| 95                  | 0.755s     |
| **Hard** | **DFS**             | 1,429,857,132       | 1283h 8m 24s (estimated) |
| **9x9**  | **Backtracking**    | 975                 | 10.626s    |
|          | **Forward Checking**| 503                 | 5.603s     |

### Notes:
- The **DFS** algorithm is the least efficient, especially for larger puzzles or higher difficulty levels, as it does not check the validity of a solution until all steps are completed.
- **Backtracking** is the simplest to implement but becomes less effective as the number of empty cells increases, especially for larger grids.
- **Forward Checking** is the most efficient of the three algorithms, as it reduces the search space by eliminating invalid options early in the process, though it requires a more complex implementation.

## Conclusion

Each algorithm has its strengths and weaknesses depending on the size and difficulty of the Sudoku puzzle. For small, easy puzzles, **DFS** might suffice, but for larger or harder puzzles, **Forward Checking** is the most efficient algorithm for solving Sudoku. **Backtracking** strikes a balance between simplicity and performance but is generally less optimal than **Forward Checking**.

