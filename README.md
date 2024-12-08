# Sudoku Solver Algorithms

This repository explores three algorithms used to solve Sudoku puzzles: **Backtracking**, **Depth-First Search (DFS)**, and **Forward Checking**. Each algorithm is analyzed for performance, including their strengths, weaknesses, and statistical efficiency.

---

## 📜 **Sudoku Overview**
Sudoku is a logic-based number placement game played on a 9x9 grid. The goal is to fill the grid such that:

- Each row, column, and 3x3 subgrid contains the digits 1 through 9.
- Numbers cannot repeat within a row, column, or subgrid.

At the start of the game, some cells are pre-filled with numbers, and the objective is to complete the grid while adhering to these rules.

---

## 🚀 **Implemented Algorithms**

### 1. **Backtracking**
- **How It Works**: 
  - Iterates through each cell and tries numbers 1 through 9.
  - If a number fits the Sudoku rules, it is placed, and the algorithm moves to the next cell.
  - If no number fits, the algorithm backtracks to the previous cell and tries the next option.
- **Pros**: 
  - Simple and reliable approach that guarantees a solution if one exists.
- **Cons**: 
  - Can be slow due to the brute-force nature of testing all possibilities.

#### **Performance Metrics**
- **Minimum Steps**: 227 (State 4)  
- **Maximum Steps**: 4483 (State 7)  
- **Average Steps**: 1203.1  

---

### 2. **Depth-First Search (DFS)**
- **How It Works**: 
  - Uses a stack to explore the grid.
  - Similar to Backtracking, but instead of direct recursion, it creates a copy of the grid for each potential move and pushes it onto the stack.
  - Backtracks by popping the last grid state when stuck.
- **Pros**: 
  - Clear and stack-driven approach.
- **Cons**: 
  - Can still be slow, as it explores many possibilities.

#### **Performance Metrics**
- **Minimum Steps**: 108 (State 8)  
- **Maximum Steps**: 2264 (State 7)  
- **Average Steps**: 671  

---

### 3. **Forward Checking**
- **How It Works**: 
  - Maintains a list of valid numbers for each cell.
  - Before placing a number, it ensures that no other cell will be left without valid options due to the placement.
- **Pros**: 
  - Reduces unnecessary trials by eliminating invalid options upfront.
  - Improves efficiency significantly compared to the other methods.
- **Cons**: 
  - Requires more memory and computation to maintain and update the lists of valid numbers.

#### **Performance Metrics**
- **Minimum Steps**: 45 (States 1, 2, 4, 6, 7, 8, 9, 10)  
- **Maximum Steps**: 61 (State 5)  
- **Average Steps**: 47.8  

---

## 📊 **Algorithm Comparison**

| Algorithm         | Minimum Steps | Maximum Steps | Average Steps | Efficiency Ranking |
|--------------------|---------------|---------------|---------------|--------------------|
| **Backtracking**   | 227           | 4483          | 1203.1        | 🚫 Least Efficient |
| **DFS**            | 108           | 2264          | 671           | ⚠️ Moderate        |
| **Forward Checking** | 45            | 61            | 47.8          | ✅ Most Efficient  |

---

## 🌟 **Key Insights**
- **Forward Checking**: 
  - The most efficient algorithm, showing consistent and low step counts across all states.
- **DFS**: 
  - A better choice than Backtracking, with lower average and maximum steps, but still less efficient than Forward Checking.
- **Backtracking**: 
  - Reliable but the least efficient, with the highest step count variability and longest solution times.

---

## 📚 **Resources**
- [Sudoku Rules](https://en.wikipedia.org/wiki/Sudoku)
- Algorithm details and performance analysis in the repository documentation.
