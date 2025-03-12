# TEAM NAME : QUANTASTIC 4 - 1

# MEMBERS :

1> VIKAS J
2> KARTHIK SRINIVAS
3> JOE KONATH


# Quantum Sudoku Solver using Qiskit

This project demonstrates how to solve a Quantum Sudoku puzzle using a hybrid quantum-classical approach. The puzzle is solved using a combination of quantum measurements, classical backtracking, and basic Sudoku strategies. The quantum Sudoku solver compares performance with a classical backtracking solver.

# Project Overview

Implements a hybrid quantum-classical Sudoku solver using Qiskit.
Solves a Sudoku puzzle by applying quantum measurements to optimize the solving process.
Utilizes classical backtracking and basic Sudoku strategies (e.g., finding singles, hidden singles).
Visualizes the solving steps and puzzle progression.
Compares quantum and classical backtracking solvers in terms of performance.

# Dataset

A Sudoku puzzle is provided as a 9x9 board where each cell contains a number between 1 and 9, or 0 if the cell is empty. The goal is to fill in the empty cells so that each row, column, and 3x3 box contains all the digits from 1 to 9.


# Feature Engineering

Each empty cell is treated as a quantum state in superposition, representing multiple possible values.
Quantum measurements are performed to collapse the states into a single value, with the quantum algorithm helping to narrow down possibilities.
Uses Qiskit's ZZFeatureMap for encoding the Sudoku puzzle and EfficientSU2 for the quantum ansatz.

# Optimizers Used

COBYLA
ADAM
SPSA
Different optimizers are applied to the quantum part of the puzzle-solving process to evaluate the performance of each.

# Training and Evaluation

The quantum Sudoku solver uses a combination of quantum measurements and classical strategies to solve the puzzle.
The classical backtracking algorithm is used for comparison.
The performance of the quantum solver is evaluated based on its speed and accuracy in solving the puzzle.

# Visualization

The solver visualizes the puzzle after each step, showing how the board evolves during the solving process.
Quantum measurements are performed at each step, and their effects on the puzzle are visualized.
The solver also displays the final solved board.

# Results

The quantum solver's performance is compared against the classical backtracking algorithm in terms of speed and accuracy.
The quantum solver is expected to be faster in some cases, especially when it can efficiently collapse quantum states