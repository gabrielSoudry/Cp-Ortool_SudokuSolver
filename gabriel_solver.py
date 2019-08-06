"""
Soudry Gabriel
Sudoku solver using Google OR TOOL Cp solver
Learning Constraint Optimization
Project engineering School
"""

from ortools.sat.python import cp_model
import numpy
import random


def display_sudoku(sudoku):
    (i, j) = (0, 0)
    for i in range(9):
        for j in range(9):
            print(sudoku[i, j], end=" ")
        print("")


# Allow to put initial constraint of the Sudoku
def initialize_sudoku(model_or_tool, sudoku_init, sudoku_to_do):
    for i in range(9):
        for j in range(9):
            if sudoku_to_do[i][j] != 0:  # If case of sudoku is filled
                sudoku_init[i][j] = model_or_tool.NewIntVar(int(sudoku_to_do[i][j]), int(sudoku_to_do[i][j]),
                                                            'column: %i' % i)
    return sudoku_init


def solveSudoku(sudoku):
    model = cp_model.CpModel()
    sudoku2 = [[model.NewIntVar(1, 9, 'column: %i' % i) for i in range(9)] for j in range(9)]
    sudoku = initialize_sudoku(model, sudoku2, sudoku)

    # Constraint in line
    for i in range(9):
        line = []
        for j in range(9):
            line.append(sudoku[i][j])
        model.AddAllDifferent(line)

    # Constraint in column
    for i in range(9):
        column = []
        for j in range(9):
            column.append(sudoku[j][i])
        model.AddAllDifferent(column)

    # Constraint in sector
    for index in range(9):
        sector = []
        for i in [(index // 3) * 3, (index // 3) * 3 + 1, (index // 3) * 3 + 2]:
            for j in [(index % 3) * 3, (index % 3) * 3 + 1, (index % 3) * 3 + 2]:
                sector.append(sudoku[i][j])
                model.AddAllDifferent(sector)

    # Initialize the solver
    solver = cp_model.CpSolver()

    # Solving
    status = solver.Solve(model)

    print("==================")
    if status == cp_model.FEASIBLE:
        for i in range(9):
            for j in range(9):
                print(solver.Value(sudoku[i][j]), end=" ")
            print()


# Example of solving :

sudoku_to_solve = numpy.array([[0, 0, 4, 1, 0, 0, 7, 9, 3],
                               [0, 9, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 7, 2, 0, 0, 8, 0, 0],
                               [6, 0, 9, 0, 4, 0, 0, 0, 0],
                               [0, 3, 0, 5, 0, 9, 0, 6, 0],
                               [0, 0, 0, 0, 3, 0, 2, 0, 9],
                               [0, 0, 6, 0, 0, 8, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 3, 0],
                               [5, 8, 2, 0, 0, 6, 9, 0, 0]])

display_sudoku(sudoku_to_solve)
print("==================")
solveSudoku(sudoku_to_solve)
