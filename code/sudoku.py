from random import sample
from enum import Enum
from collections.abc import Sequence
from typing import LiteralString


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Sudoku(object):
    """Represents the players' sudoku field"""

    def __init__(self, size: int = 9):
        """Initializes objects of sudoku class with default size of 9 fields as height and width.
        Each field has a grid which is per default 3x3"""
        self.size: int = size
        temp_grid = size ** (1 / 2)
        if size < 4:
            raise ValueError(
                "This size can not be taken as a valid sudoku size, because it is to small!"
            )
        if int(temp_grid) ** 2 != self.size:
            raise ValueError(
                "This size can not be taken as a valid sudoku size, because it is not a square number!"
            )
        self.grid: int = int(temp_grid)

        # filling with some values, later the create function should be called to generate a solvable field
        self.values: list[list[int]] = [
            [x for x in range(1, size + 1)] for i in range(1, size + 1)
        ]

        self.solution: list[list[int]] = []

    def create(self, difficulty: Difficulty = ...):
        """Creates a new sudoku that is solvable and has some empty entries depending on difficulty (easy, medium or hard)
        The used algorithm can be found in web, e.g. here:
        https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python

        The Difficulty is being represented as Enum. A suitable call of this function would be 'field.create(Difficulty.MEDIUM)' for example.
        """
        self._generate()
        self._remove_numbers(difficulty)

    def _generate(self):
        """Generates new random numbers, so the sudoku field is completely filled and solved"""
        rows = []
        for g in self._shuffle():
            for r in self._shuffle():
                rows.append(g * self.grid + r)
        cols = []
        for g in self._shuffle():
            for r in self._shuffle():
                cols.append(g * self.grid + r)
        nums = self._shuffle(range(1, self.grid * self.grid + 1))

        self.values = []
        for r in rows:
            b = []
            for c in cols:
                b.append(
                    nums[(self.grid * (r % self.grid) +
                          r // self.grid + c) % self.size]
                )
            self.values.append(b)
        self.solution = Sudoku._deep_copy(self.values)

    def _shuffle(self, l: Sequence[int] = ...) -> list[int]:
        """Returns a randomized permutation of list input, e.g. [0,1,2] -> [0,2,1]
        If no Sequence Object is given the l parameter will be set to the grid size, which is 3 per default
        """
        if l is ...:
            l = range(self.grid)
        return sample(l, len(l))

    def _remove_numbers(self, difficulty: Difficulty):
        """Removes numbers based on given difficulty that can be null.
        If it is easy around a quarter will be removed, with medium around two quarters and otherwise three quarters.
        The default difficulty is hard."""
        squares = self.size**2

        empties = squares * 3 // 4
        if difficulty is Difficulty.EASY:
            empties = squares * 1 // 4
        elif difficulty is Difficulty.MEDIUM:
            empties = squares * 2 // 4

        for p in sample(range(squares), empties):
            self.values[p // self.size][p % self.size] = 0

    def set(self, x: int, y: int, new_value: int):
        """Sets specified new_value in a the sudoku field with coordinates x and y and allows 'empty' value 0"""
        if self.is_valid_coordinate(x, y) and self.is_valid_value(new_value):
            self.values[x][y] = new_value
        else:
            raise Exception(
                "You are trying to access a value that is outside of the Sudoku field!"
            )

    def is_empty(values: list[list[int]], x: int, y: int) -> bool:
        ''' Checks if entry of given coordinates x and y is empty '''
        return values[x][y] == 0

    def is_valid_value(self, value: int):
        return 0 <= value and value <= self.size

    def is_valid_coordinate(self, x: int, y: int) -> bool:
        """Checks if given coordinates x and y lie in a sudoku field"""
        return 0 <= x and x < self.size and 0 <= y and y < self.size

    def solve(self):
        """Returns solution that was created in the 'create()' method after '_generate()' and before '_remove_numbers()',
        if it exists. Otherwise a backtracking algorithm solves given Sudoku or throws an exception in case the sudoku
        is not solvable.
        After calling this method the solution will be saved in the 'self.solution' attribute and the 'self.values'
        parameter will stay the same.
        """
        if self.solution:
            return
        if self.is_solved():
            # The self.values attribute already is a solution, so everything left to do is to copy it to self.solution
            self.solution = Sudoku._deep_copy(self.values)
            return

        # Deep Copy of self.values is necessary because it will be used and changed in _backtrack_sudoku() later on
        temp = Sudoku._deep_copy(self.values)

        if self.size >= 36:
            raise Exception(
                "\nHi, it's me your Pc. You are working with such high numbers... \n...that is too strenuous for me! \nFunfact: Already the normal Sudoku field with self.size = 9 has 81! permutations, but a lot of those would not pass my is_valid() method. This is why there are 'only' around 6.67 * 10²¹ possible fields! [https://rp-online.de/panorama/wissen/wie-viele-sudokus-sind-moeglich_aid-17351685]"
            )
        if self._backtrack_sudoku(0):
            self.solution = self.values
            self.values = temp
            return
        else:
            raise Exception("Oh no! Seems like this Sudoku is unsolvable :( ")

    def _deep_copy(source: list[list[int]]) -> list[list[int]]:
        """Returns Deep Copy of two-dimensional list, such as the 'self.values' or 'self.solution' attribute"""
        return [row[:] for row in source]

    def _backtrack_sudoku(self, index) -> bool:
        """Solves complete sudoku game through a backtracking algorithm and returns if the game is solvable.
        But Caution, it is recursive, so 'self.size' should be not more than 36 otherwise the program gets slow!
        """
        if index == self.size * self.size:
            return self.is_solved()
        row = index // self.size
        col = index % self.size
        if self.values[row][col] == 0:
            # print(index // self.size,index % self.size)
            for j in range(1, self.size + 1):
                self.values[row][col] = j
                # print(self)
                if self.is_valid() and self._backtrack_sudoku(index + 1):
                    return True
                self.values[row][col] = 0
            return False
        return self._backtrack_sudoku(index + 1)

    def is_filled(self) -> bool:
        """Checks if the sudoku field is already completely filled"""
        for row in self.values:
            # If there is an empty value it is represented as '0'
            if not all(i != 0 for i in row):
                return False
        return True

    def is_valid(self) -> bool:
        """Checks if all sudoku field entries are valid.
        According to the rules there must not be any duplicate in every row and column, as well as in each grid
        """
        return (
            self._is_valid_in_every_row()
            and self._is_valid_in_every_column()
            and self._is_valid_in_every_grid()
        )

    def _is_valid_in_every_row(self) -> bool:
        """Checks if all sudoku field entries are valid in every row"""
        for row in self.values:
            if not Sudoku._is_valid_sudoku_list(row):
                return False
        return True

    def _is_valid_in_every_column(self) -> bool:
        """Checks if all sudoku field entries are valid in every column"""
        for col in range(0, self.size):
            filled_vals = []
            for row in self.values:
                if row[col] != 0 and row[col] in filled_vals:
                    return False
                filled_vals.append(row[col])
        return True

    def _is_valid_in_every_grid(self) -> bool:
        """Checks if all sudoku field entries are valid in every grid"""
        grids = []
        for row in self.values:
            for j in range(0, self.grid):
                test = []
                for i in range(0, self.grid):
                    test.append(row[i + self.grid * j])
                grids.append(test)
        new = {}
        i = 0
        for el in range(0, self.size * self.grid):
            if el % self.size == 0 and el != 0:
                i += self.grid
            if (el % self.grid) + i not in new:
                new[(el % self.grid) + i] = grids[el]
            else:
                new[(el % self.grid) + i].extend(grids[el])

        for val in new.values():
            if not Sudoku._is_valid_sudoku_list(val):
                return False
        # TODO add example

        return True

    def _is_valid_sudoku_list(l: list) -> bool:
        """A valid sudoku list should not contain duplicates, but empty entries that are represented as 0 are allowed"""
        l_without_zero = [item for item in l if item !=
                          0]  # Remove empty 0 cells
        # Check duplicates
        return len(l_without_zero) == len(set(l_without_zero))

    def is_solved(self) -> bool:
        """Checks if the sudoku field is completely solved"""
        return self.is_filled() and self.is_valid()

    def remove(self, x: int, y: int):
        """Removes an entry in a sudoku field and replaces it by invalid value 0"""
        self.set(x, y, 0)

    def __str__(self) -> LiteralString | str:
        """String representation of a sudoku field as a formatted matrix"""
        rep = ""
        for i in range(0, self.size):
            # After every row of self.grid many fields there is a horizontal line
            if i % self.grid == 0:
                rep += " - " * self.size + "\n"

            for j in range(0, self.size):
                # After every column of self.grid many fields there is a vertical line
                if j % self.grid == 0:
                    rep += "|"

                if self.values[i][j] == 0:
                    # Zero represents an empty value
                    rep += "   "
                else:
                    # Actual number values of the sudoku field
                    rep += " " + str(self.values[i][j]) + " "
            rep += "|\n"
        return rep


# Some experimental Code to test functions

# f = Sudoku(36)
# f.create(Difficulty.EASY)
# print(f)
# print(f.is_valid())
# temp = Sudoku._deep_copy(f.solution)
# f.solution = []

# f.solve()
# f.values = f.solution
# print(f)


# f.set(1, 1, 3)
# f.set(2, 2, 3)

# print(f.is_valid())
# print(f)
# print(f.is_filled())

# board = [
#         [7, 8, 0, 4, 0, 0, 1, 2, 0],
#         [6, 0, 0, 0, 7, 5, 0, 0, 9],
#         [0, 0, 0, 6, 0, 1, 0, 7, 8],
#         [0, 0, 7, 0, 4, 0, 2, 6, 0],
#         [0, 0, 1, 0, 5, 0, 9, 3, 0],
#         [9, 0, 4, 0, 6, 0, 0, 0, 5],
#         [0, 7, 0, 3, 0, 0, 0, 1, 2],
#         [1, 2, 0, 0, 0, 7, 4, 0, 0],
#         [0, 4, 9, 2, 0, 6, 0, 0, 7]
# ]
# print(f.is_valid())
# f.values = board
# print(f)
# print(f.is_valid())
# print(f.is_solved())
