"""
Soudry Gabriel
Sudoku solver using Google OR TOOL Cp solver
Project engineering School
"""

from ortools.sat.python import cp_model
import numpy
import random

sudoku_3_3 = numpy.array([[0, 1, 3],
                          [0, 8, 2],
                          [7, 4, 0]])


def display_sudoku(sudoku):
    (i, j) = (0, 0)
    for i in range(3):
        for j in range(3):
            print(sudoku[i, j], end=" ")
        print("")


class SolutionPrinter(cp_model.CpSolverSolutionCallback):

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def SolutionCount(self):
        return self.__solution_count


# Allow to put initial constraint of the Sudoku
def initialize_sudoku(model_or_tool, sudoku_init, sudoku_to_do):
    for i in range(3):
        for j in range(3):
            if sudoku_to_do[i][j] != 0:  # If case of sudoku is filled
                sudoku_init[i][j] = model_or_tool.NewIntVar(int(sudoku_to_do[i][j]), int(sudoku_to_do[i][j]),
                                                            'column: %i' % i)
    return sudoku_init


def solveSudoku(sudoku):
    model = cp_model.CpModel()
    sudoku2 = [[model.NewIntVar(1, 9, 'column: %i' % i) for i in range(3)] for j in range(3)]
    sudoku = initialize_sudoku(model, sudoku2, sudoku)
    for i in range(3):
        line = []
        for j in range(3):
            line.append(sudoku[i][j])
        model.AddAllDifferent(line)

    for index in range(1):
        sector = []
        for i in [(index // 3) * 3, (index // 3) * 3 + 1, (index // 3) * 3 + 2]:
            for j in [(index % 3) * 3, (index % 3) * 3 + 1, (index % 3) * 3 + 2]:
                sector.append(sudoku[i][j])
                model.AddAllDifferent(sector)

        solver = cp_model.CpSolver()
        status = solver.Solve(model)

    print("==================")
    if status == cp_model.FEASIBLE:
        for i in range(3):
            for j in range(3):
                print(solver.Value(sudoku[i][j]), end=" ")
            print()

display_sudoku(sudoku_3_3)
print("==================")
solveSudoku(sudoku_3_3)
