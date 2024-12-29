from random import sample, randint
from enum import Enum
from collections.abc import Sequence
from typing import LiteralString


class Difficulty(Enum):
    """Represents Difficulties that can be chosen from while creating a new Sudoku game"""

    EASY = 1
    MEDIUM = 2
    HARD = 3


class Colors(Enum):
    """
    This Enumeration collects some well chosen ansi escape sequences for graphic rendition 
    parameters using control sequence introducer commands to generate colored output in console,
    like described in: https://en.wikipedia.org/wiki/ANSI_escape_code
    """
    WHITE = '\033[97m'
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    GREY = '\033[90m'
    CROSSED = '\033[9m'
    INVERTED = '\033[7m'
    BLINKING = '\033[5m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    BOLD = '\033[1m'
    END = '\033[0m'


class Sudoku(object):
    """Represents the players' sudoku field

    >>> s = Sudoku(size=9)
    >>> s.create(difficulty=Difficulty.EASY)
    >>> s.is_valid()
    True
    >>> s.is_filled()
    False
    >>> value = s.values[0][0]
    >>> s.remove(0,0)
    >>> Sudoku.is_empty(s.values,0,0)
    True
    >>> s.set(0,0,value)
    >>> s.solve()
    >>> s.values = s.solution
    >>> s.is_solved()
    True
    """

    def __init__(self, size: int = 9, values: list[list[int]] = ...):
        """Initializes objects of sudoku class with default size of 9 fields as height and width.
        Each field has a grid which is per default 3x3

        >>> s = Sudoku(5) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
            ...
        ValueError: This size can not be taken as a valid sudoku size, because it is not a square number!

        >>> s = Sudoku(-1) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
            ...
        ValueError: This size can not be taken as a valid sudoku size, because it is to small!
        """
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

        if values is ...:
            # filling with some values, later the create function should be called to generate a solvable field
            self.values: list[list[int]] = [
                [x for x in range(1, size + 1)] for i in range(1, size + 1)
            ]
        else:
            self.values = values

        self.solution: list[list[int]] = []

    def create(self, difficulty: Difficulty = ...):
        """Creates a new sudoku that is solvable and has some empty entries depending on difficulty (easy, medium or hard)
        The used algorithm can be found in web, e.g. here:
        https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python

        The Difficulty is being represented as Enum. A suitable call of this function would be 'field.create(Difficulty.MEDIUM)' for example.

        >>> s = Sudoku(size=9)
        >>> s.create(difficulty=Difficulty.HARD)
        >>> s.values != []
        True
        >>> s.is_valid()
        True
        >>> s.solution != []
        True
        """
        self._generate()
        self._remove_numbers(difficulty)

    def _generate(self):
        """Generates new random numbers, so the sudoku field is completely filled and solved

        >>> s = Sudoku(size=9)
        >>> s._generate()
        >>> s.values != []
        True
        >>> s.is_solved()
        True
        >>> s.solution == s.values
        True
        """
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

        >>> s = Sudoku(size=9)
        >>> x = s._shuffle()
        >>> x in [[0,1,2],[0,2,1],[1,2,0],[1,0,2],[2,0,1],[2,1,0]]
        True

        """
        if l is ...:
            l = range(self.grid)
        return sample(l, len(l))

    def _remove_numbers(self, difficulty: Difficulty):
        """Removes numbers based on given difficulty that can be null.
        If it is easy around a quarter will be removed, with medium around two quarters and otherwise three quarters.
        The default difficulty is hard.

        >>> s = Sudoku(size=9)
        >>> s._generate()
        >>> s._remove_numbers(Difficulty.EASY)
        >>> s.is_solved()
        False
        >>> s.solution != s.values
        True
        """
        squares = self.size**2

        empties = squares * 3 // 4
        if difficulty is Difficulty.EASY:
            empties = squares * 1 // 4
        elif difficulty is Difficulty.MEDIUM:
            empties = squares * 2 // 4

        for p in sample(range(squares), empties):
            self.values[p // self.size][p % self.size] = 0

    def set(self, x: int, y: int, new_value: int):
        """Sets specified new_value in a the sudoku field with coordinates x and y and allows 'empty' value 0

        >>> s = Sudoku(size=9)
        >>> s.set(1,1,10) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
            ...
        Exception: You are trying to set an invalid value or one that is outside of the Sudoku field!
        """
        if self.is_valid_coordinate(x, y) and self.is_valid_value(new_value):
            self.values[x][y] = new_value
        else:
            raise Exception(
                "You are trying to set an invalid value or one that is outside of the Sudoku field!"
            )

    def is_empty(values: list[list[int]], x: int, y: int) -> bool:
        """Checks if entry of given coordinates x and y is empty

        >>> Sudoku.is_empty([[2, 3, 6, 7, 0, 0, 8, 0, 0], [9, 8, 0, 0, 3, 6, 0, 7, 0], [7, 0, 5, 0, 8, 1, 3, 2, 6], [3, 1, 9, 4, 6, 2, 5, 8, 0], [4, 6, 2, 8, 5, 7, 1, 3, 9], [8, 5, 0, 0, 1, 9, 6, 4, 0], [1, 7, 0, 0, 9, 3, 2, 0, 4], [6, 9, 0, 5, 0, 4, 7, 1, 8], [5, 2, 4, 1, 0, 8, 9, 6, 3]],0,3)
        False
        >>> Sudoku.is_empty([[2, 3, 6, 7, 0, 0, 8, 0, 0], [9, 8, 0, 0, 3, 6, 0, 7, 0], [7, 0, 5, 0, 8, 1, 3, 2, 6], [3, 1, 9, 4, 6, 2, 5, 8, 0], [4, 6, 2, 8, 5, 7, 1, 3, 9], [8, 5, 0, 0, 1, 9, 6, 4, 0], [1, 7, 0, 0, 9, 3, 2, 0, 4], [6, 9, 0, 5, 0, 4, 7, 1, 8], [5, 2, 4, 1, 0, 8, 9, 6, 3]],0,4)
        True

        """
        return values[x][y] == 0

    def is_valid_value(self, value: int):
        """Checks if given value is valid, which implies that its value is not negative
            and is not greater than the Sudoku field size

        >>> s = Sudoku(size=9)
        >>> s.is_valid_value(10)
        False
        >>> s.is_valid_value(-1)
        False
        >>> s.is_valid_value(1)
        True
        """
        return 0 <= value and value <= self.size

    def is_valid_coordinate(self, x: int, y: int) -> bool:
        """Checks if given coordinates x and y lie in a sudoku field

        >>> s = Sudoku(size=9)
        >>> s.is_valid_coordinate(9,8)
        False
        >>> s.is_valid_coordinate(-1,1)
        False
        >>> s.is_valid_coordinate(0,0)
        True
        """
        return 0 <= x and x < self.size and 0 <= y and y < self.size

    def solve(self):
        """Returns solution that was created in the 'create()' method after '_generate()' and before '_remove_numbers()',
        if it exists. Otherwise a backtracking algorithm solves given Sudoku or throws an exception in case the sudoku
        is not solvable.
        After calling this method the solution will be saved in the 'self.solution' attribute and the 'self.values'
        parameter will stay the same.

        >>> s = Sudoku(size=9,values=[[3, 5, 4, 2, 6, 8, 1, 9, 7], [2, 8, 6, 1, 9, 7, 3, 4, 5], [1, 7, 9, 3, 4, 5, 2, 6, 8], [7, 4, 3, 5, 2, 6, 8, 1, 9], [5, 6, 2, 8, 1, 9, 7, 3, 4], [8, 9, 1, 7, 3, 4, 5, 2, 6], [9, 3, 7, 4, 5, 2, 6, 8, 1], [6, 1, 8, 9, 7, 3, 4, 5, 2], [4, 2, 5, 6, 8, 1, 9, 7, 3]])
        >>> s.solution = []
        >>> s.solve()
        >>> s.values == s.solution
        True


        >>> s.values = [[5, 5, 0, 2, 0, 8, 1, 9, 7], [2, 8, 6, 1, 9, 7, 3, 4, 5], [1, 7, 9, 3, 4, 5, 2, 6, 8], [7, 0, 3, 0, 2, 6, 8, 1, 0], [5, 6, 0, 8, 1, 9, 7, 0, 4], [8, 9, 1, 7, 3, 0, 5, 2, 6], [0, 3, 7, 4, 0, 2, 0, 0, 1], [6, 1, 8, 9, 7, 0, 4, 0, 2], [0, 0, 0, 6, 8, 1, 9, 0, 0]]
        >>> s.solution = []
        >>> s.solve() # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
            ...
        Exception: Oh no! Seems like this Sudoku is unsolvable :(
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
        """Returns Deep Copy of two-dimensional list, such as the 'self.values' or 'self.solution' attribute

        >>> source = [[1, 2, 3], [4, 5, 6]]
        >>> dest = Sudoku._deep_copy(source)
        >>> dest
        [[1, 2, 3], [4, 5, 6]]
        >>> source == dest
        True
        >>> source is dest
        False
        >>> source[0] == dest[0]
        True
        >>> source[0] is dest[0]
        False
        """
        return [row[:] for row in source]

    def _backtrack_sudoku(self, index) -> bool:
        """Solves complete sudoku game through a backtracking algorithm and returns if the game is solvable.
        But Caution, it is recursive, so 'self.size' should be not more than 36 otherwise the program gets slow!

        >>> s = Sudoku(size=9,values=[[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 6, 1, 9, 7, 3, 4, 5], [1, 0, 9, 3, 4, 5, 2, 6, 8], [7, 4, 0, 5, 2, 6, 8, 1, 9], [5, 6, 2, 0, 1, 9, 7, 3, 4], [8, 9, 1, 7, 0, 4, 5, 2, 6], [9, 3, 7, 4, 5, 0, 6, 8, 1], [6, 1, 8, 9, 7, 3, 0, 5, 2], [4, 2, 5, 6, 8, 1, 9, 0, 3]])
        >>> s._backtrack_sudoku(0)
        True
        >>> s.values == [[3, 5, 4, 2, 6, 8, 1, 9, 7], [2, 8, 6, 1, 9, 7, 3, 4, 5], [1, 7, 9, 3, 4, 5, 2, 6, 8], [7, 4, 3, 5, 2, 6, 8, 1, 9], [5, 6, 2, 8, 1, 9, 7, 3, 4], [8, 9, 1, 7, 3, 4, 5, 2, 6], [9, 3, 7, 4, 5, 2, 6, 8, 1], [6, 1, 8, 9, 7, 3, 4, 5, 2], [4, 2, 5, 6, 8, 1, 9, 7, 3]]
        True

        >>> s.values = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        >>> s._backtrack_sudoku(0)
        True
        >>> s.values == [[1, 2, 3, 4, 5, 6, 7, 8, 9], [4, 5, 6, 7, 8, 9, 1, 2, 3], [7, 8, 9, 1, 2, 3, 4, 5, 6], [2, 1, 4, 3, 6, 5, 8, 9, 7], [3, 6, 5, 8, 9, 7, 2, 1, 4], [8, 9, 7, 2, 1, 4, 3, 6, 5], [5, 3, 1, 6, 4, 2, 9, 7, 8], [6, 4, 2, 9, 7, 8, 5, 3, 1], [9, 7, 8, 5, 3, 1, 6, 4, 2]]
        True

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
        """Checks if the sudoku field is already completely filled

        >>> s = Sudoku(size=9,values=[[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]])
        >>> s.is_filled()
        True
        >>> s.values[0][0] = 0
        >>> s.is_filled()
        False
        """
        for row in self.values:
            # If there is an empty value it is represented as '0'
            if not all(i != 0 for i in row):
                return False
        return True

    def is_valid(self) -> bool:
        """Checks if all sudoku field entries are valid.
        According to the rules there must not be any duplicate in every row and column, as well as in each grid

        >>> s = Sudoku(size=9,values=[[8, 0, 5, 7, 3, 4, 6, 1, 9], [4, 0, 3, 6, 9, 0, 2, 8, 5], [0, 0, 9, 2, 5, 0, 7, 4, 3], [6, 9, 8, 0, 0, 2, 3, 7, 1], [7, 3, 0, 9, 8, 6, 5, 2, 0], [0, 5, 4, 3, 1, 7, 9, 6, 8], [3, 1, 0, 8, 2, 9, 0, 5, 7], [0, 8, 2, 0, 7, 5, 1, 3, 6], [0, 4, 0, 1, 0, 3, 8, 0, 0]])
        >>> s.is_valid()
        True
        >>> s.values[0][0] = 5
        >>> s.is_valid()
        False
        """
        return (
            self._is_valid_in_every_row()
            and self._is_valid_in_every_column()
            and self._is_valid_in_every_grid()
        )

    def _is_valid_in_every_row(self) -> bool:
        """Checks if all sudoku field entries are valid in every row

        >>> s = Sudoku(size=9,values=[[8, 0, 5, 7, 3, 4, 6, 1, 9], [4, 0, 3, 6, 9, 0, 2, 8, 5], [0, 0, 9, 2, 5, 0, 7, 4, 3], [6, 9, 8, 0, 0, 2, 3, 7, 1], [7, 3, 0, 9, 8, 6, 5, 2, 0], [0, 5, 4, 3, 1, 7, 9, 6, 8], [3, 1, 0, 8, 2, 9, 0, 5, 7], [0, 8, 2, 0, 7, 5, 1, 3, 6], [0, 4, 0, 1, 0, 3, 8, 0, 0]])
        >>> s._is_valid_in_every_row()
        True
        >>> s.values[0][0] = 5
        >>> s._is_valid_in_every_row()
        False
        """
        for row in self.values:
            if not Sudoku._is_valid_sudoku_list(row):
                return False
        return True

    def _is_valid_in_every_column(self) -> bool:
        """Checks if all sudoku field entries are valid in every column

        >>> s = Sudoku(size=9,values=[[8, 0, 5, 7, 3, 4, 6, 1, 9], [4, 0, 3, 6, 9, 0, 2, 8, 5], [0, 0, 9, 2, 5, 0, 7, 4, 3], [6, 9, 8, 0, 0, 2, 3, 7, 1], [7, 3, 0, 9, 8, 6, 5, 2, 0], [0, 5, 4, 3, 1, 7, 9, 6, 8], [3, 1, 0, 8, 2, 9, 0, 5, 7], [0, 8, 2, 0, 7, 5, 1, 3, 6], [0, 4, 0, 1, 0, 3, 8, 0, 0]])
        >>> s._is_valid_in_every_column()
        True
        >>> s.values[0][6] = 2
        >>> s._is_valid_in_every_column()
        False
        """
        for col in range(0, self.size):
            filled_vals = []
            for row in self.values:
                if row[col] != 0 and row[col] in filled_vals:
                    return False
                filled_vals.append(row[col])
        return True

    def _is_valid_in_every_grid(self) -> bool:
        """Checks if all sudoku field entries are valid in every grid

        >>> s = Sudoku(size=9,values=[[8, 0, 5, 7, 3, 4, 6, 1, 9], [4, 0, 3, 6, 9, 0, 2, 8, 5], [0, 0, 9, 2, 5, 0, 7, 4, 3], [6, 9, 8, 0, 0, 2, 3, 7, 1], [7, 3, 0, 9, 8, 6, 5, 2, 0], [0, 5, 4, 3, 1, 7, 9, 6, 8], [3, 1, 0, 8, 2, 9, 0, 5, 7], [0, 8, 2, 0, 7, 5, 1, 3, 6], [0, 4, 0, 1, 0, 3, 8, 0, 0]])
        >>> s._is_valid_in_every_grid()
        True
        >>> s.values[1][1] = 8
        >>> s._is_valid_in_every_grid()
        False
        """
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

        return True

    def _is_valid_sudoku_list(l: list) -> bool:
        """A valid sudoku list should not contain duplicates, but empty entries that are represented as 0 are allowed

        >>> Sudoku._is_valid_sudoku_list([7, 6, 9, 1, 2, 5, 8, 9, 4])
        False
        >>> Sudoku._is_valid_sudoku_list([0, 0, 0, 0, 0, 0, 0, 0, 0])
        True
        >>> Sudoku._is_valid_sudoku_list([7, 6, 0, 1, 2, 5, 8, 9, 4])
        True
        """
        l_without_zero = [item for item in l if item !=
                          0]  # Remove empty 0 cells
        # Check duplicates
        return len(l_without_zero) == len(set(l_without_zero))

    def is_solved(self) -> bool:
        """Checks if the sudoku field is completely solved

        >>> s = Sudoku(size=9,values=[[7, 2, 8, 3, 4, 6, 5, 1, 9], [5, 9, 1, 2, 8, 7, 6, 4, 3], [6, 3, 4, 9, 1, 5, 7, 8, 2], [1, 6, 3, 5, 9, 8, 4, 2, 7], [4, 7, 2, 6, 3, 1, 8, 9, 5], [8, 5, 9, 7, 2, 4, 1, 3, 6], [2, 8, 5, 4, 7, 3, 9, 6, 1], [9, 1, 6, 8, 5, 2, 3, 7, 4], [3, 4, 7, 1, 6, 9, 2, 5, 8]])
        >>> s.is_solved()
        True

        >>> s.values[0][0] = 0
        >>> s.is_solved()
        False
        """
        return self.is_filled() and self.is_valid()

    def remove(self, x: int, y: int):
        """Removes an entry in a sudoku field and replaces it by invalid value 0

        >>> s = Sudoku(size=9,values=[[5, 1, 3, 6, 4, 8, 9, 2, 7], [0, 4, 8, 2, 0, 9, 3, 5, 0], [0, 7, 9, 5, 1, 3, 8, 6, 0], [1, 3, 2, 0, 8, 5, 6, 7, 9], [0, 8, 5, 7, 0, 6, 0, 1, 3], [0, 0, 6, 0, 3, 2, 5, 0, 8], [9, 6, 4, 0, 2, 7, 1, 8, 5], [3, 2, 7, 0, 5, 1, 4, 9, 6], [8, 0, 1, 9, 6, 0, 0, 0, 0]])
        >>> s.remove(0,0)
        >>> Sudoku.is_empty(s.values,0,0)
        True
        >>> Sudoku.is_empty(s.values,0,1)
        False
        """
        self.set(x, y, 0)

    def _get_a_hint(self) -> tuple[int, int, int]:
        """ Returns the value of an empty field according to the following pattern: (x, y, value)

        >>> s = Sudoku()
        >>> s.create(difficulty=Difficulty.EASY)
        >>> x, y, value = s._get_a_hint()
        >>> s.values[x][y] == 0
        True
        >>> s.solution[x][y] == value
        True

        >>> s.values = s.solution
        >>> s._get_a_hint() # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
            ...
        Exception: The Sudoku is already solved!
        """
        self.solve()
        if self.is_solved():
            raise Exception("The Sudoku is already solved!")
        pos_x = randint(0, self.size - 1)
        pos_y = randint(0, self.size - 1)
        while self.values[pos_x][pos_y] != 0:
            pos_x = randint(0, self.size - 1)
            pos_y = randint(0, self.size - 1)
        return pos_x, pos_y, self.solution[pos_x][pos_y]

    def show_and_set_hint(self) -> LiteralString | str:
        # TODO Write Docs and Test
        return self.show_and_set_value(*self._get_a_hint(), highlighted_color=Colors.CYAN)

    def show_and_set_value(self, x: int, y: int, value: int, highlighted_color: Colors) -> LiteralString | str:
        # TODO Write Docs and Test
        self.set(x, y, value)
        return self.show_value(x, y, highlighted_color)

    def show_value(self, x: int, y: int, highlighted_color: Colors) -> LiteralString | str:
        # TODO Write Docs and Test
        highlighted_list = [[0 for i in range(self.size)]
                            for j in range(self.size)]
        highlighted_list[x][y] = self.values[x][y]
        if self.values[x][y] == 0:
            highlighted_list[x][y] = '_'
        return self.__str__(highlighted_values=highlighted_list, highlighted_color=highlighted_color)

    def show_blinking_cell(self, x: int, y: int) -> LiteralString | str:
        # TODO Write Docs and Test
        return s.show_value(x, y, Colors.BLINKING)

    def show_wrong_fields(self) -> LiteralString | str:
        """ Gets a string representation of current sudoku field values with wrong ones marked through ansi sequences

        >>> s = Sudoku()
        >>> s.create(difficulty=Difficulty.EASY)
        >>> s.values[0][0] = 5
        >>> s.values[0][1] = 5
        >>> "\x1b[91m5\x1b[0m" in s.show_wrong_fields() # Note that the expression in quotation marks is a red 5 (also noticeable in the tests output)
        True
        """
        wrong_fields = self._get_wrong_fields()
        return self.__str__(wrong_fields, Colors.RED)

    def _get_wrong_fields(self) -> list[list[int]]:
        """ Compares current values to one possible solution and returns a field containing every different number

        >>> s = Sudoku()
        >>> s.create(difficulty=Difficulty.EASY)
        >>> s.values[0][0] = 5
        >>> s.values[0][1] = 5
        >>> wrong_fields = s._get_wrong_fields()
        >>> wrong_fields[0][0] != 0 or wrong_fields[0][1] != 0
        True
        """
        self.solve()
        wrong_fields = []
        for row in range(0, self.size):
            value_row = []
            for col in range(0, self.size):
                if self.values[row][col] != self.solution[row][col]:
                    value_row.append(self.values[row][col])
                else:
                    value_row.append(0)
            wrong_fields.append(value_row)
        return wrong_fields

    def __str__(self, highlighted_values: list[list[int | str]] = ..., highlighted_color: Colors = ...) -> LiteralString | str:
        """String representation of a sudoku field as a formatted matrix

        >>> s = Sudoku(size=9,values=[[8, 0, 0, 5, 1, 7, 6, 9, 3], [9, 3, 6, 4, 8, 0, 5, 1, 7], [1, 7, 5, 6, 9, 0, 4, 8, 2], [0, 4, 9, 8, 2, 0, 0, 0, 0], [7, 6, 1, 0, 3, 4, 8, 0, 5], [2, 5, 8, 1, 7, 0, 9, 0, 4], [4, 8, 3, 0, 5, 0, 0, 6, 9], [0, 0, 7, 3, 0, 8, 2, 0, 1], [5, 1, 2, 7, 6, 9, 3, 4, 8]])
        >>> print(s)
         -  -  -  -  -  -  -  -  - 
        | 8       | 5  1  7 | 6  9  3 |
        | 9  3  6 | 4  8    | 5  1  7 |
        | 1  7  5 | 6  9    | 4  8  2 |
         -  -  -  -  -  -  -  -  - 
        |    4  9 | 8  2    |         |
        | 7  6  1 |    3  4 | 8     5 |
        | 2  5  8 | 1  7    | 9     4 |
         -  -  -  -  -  -  -  -  - 
        | 4  8  3 |    5    |    6  9 |
        |       7 | 3     8 | 2     1 |
        | 5  1  2 | 7  6  9 | 3  4  8 |
        <BLANKLINE>

        """
        rep = ""
        for i in range(0, self.size):
            # After every row of self.grid many fields there is a horizontal line
            if i % self.grid == 0:
                rep += " - " * self.size + "\n"

            for j in range(0, self.size):
                # After every column of self.grid many fields there is a vertical line
                if j % self.grid == 0:
                    rep += "|"

                if highlighted_values is ... or highlighted_color is ... or Sudoku.is_empty(highlighted_values, i, j):
                    # Cell should not be highlighted
                    if self.values[i][j] == 0:
                        # Zero represents an empty cell
                        rep += "   "
                    else:
                        # Actual number values of the sudoku field
                        rep += " " + str(self.values[i][j]) + " "
                else:
                    # Colored output of those values of highlighted_values that are not empty
                    rep += " " + highlighted_color.value + \
                        str(highlighted_values[i][j]
                            ) + Colors.END.value + " "
            rep += "|\n"
        return rep


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
