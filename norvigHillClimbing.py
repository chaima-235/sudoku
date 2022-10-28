## Solve Every Sudoku Puzzle

## See http://norvig.com/sudoku.html

import sys
from itertools import islice

## Throughout this program we have:
##   r is a row,    e.g. 'A'
##   c is a column, e.g. '3'
##   s is a square, e.g. 'A3'
##   d is a digit,  e.g. '9'
##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}
import numpy as np


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]


digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s], [])) - set([s]))
             for s in squares)
box = dict((s, set(sum([units[s][2]],[]))-set([s])) ## Only boxes
             for s in squares)

################ Unit Tests ################

def test():
    "A set of tests that must pass."
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print('All tests pass.')


################ Parse a Grid ################

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False  ## (Fail if we can't assign d to square s.)
    return values


def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


################ Constraint Propagation ################

def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values  ## Already eliminated
    values[s] = values[s].replace(d, '')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False  ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False  ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values


################ Display as 2-D grid ################

def display(values):
    "Display these values as a 2-D grid."
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else ''))
              for c in cols)
        if r in 'CF': print(line)


################ Search ################

def solve(grid): return search(parse_grid(grid))

def convert(a):
    it = iter(a)
    res_dect=dict(zip(it,''))
    return res_dect

def returnValues(values) :
    lst=[]
    for(key,value) in values.items():
        lst.append(value)
        return lst

def unit1(values):
    lst=[3,6,9]
    lst_value = returnValues(values)
    print(lst_value)
    squares_dict = dict()
    list_squares =[]

    for i in lst:
       list_squares.append((units['A'+str(i)][2]))
       list_squares.append((units['D'+str(i)][2]))
       list_squares.append((units['G'+str(i)][2]))
    for i in list_squares:
        for j in i:
            squares_dict.update({j : values[j]})
    return squares_dict

def remplissage(values):
    square_dict = unit1(values)
    square_dict_final = dict()
    lst_digit = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range(0,9):
        square_dict_final= remplissage_square(square_dict,square_dict_final)


    return square_dict_final

def remplissage_square(square_dict,square_dict_final):
    lst_digit = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    lst_already_popped = []
    for index, key in enumerate(square_dict):
        if index < 9:
            square_dict_final[key] = square_dict.get(key)
            lst_already_popped.append(key)
            if square_dict.get(key) in lst_digit:
                lst_digit.remove(square_dict.get(key))
        if index == 9:
            break

    for key in lst_already_popped:
            square_dict.pop(key)

    for index, key in enumerate(square_dict_final):
        if square_dict_final[key] == '.':
            x = random.choice(lst_digit)
            square_dict_final.update({key:str(x)})
            lst_digit.remove(x)
    return square_dict_final

def update_values(square_dict_final, values):
    for key in values:
        if key in square_dict_final:
            values[key] = square_dict_final[key]
    return values

def columns_conflicts(values):
    conflicts = 0
    for column in [cross(rows, c) for c in cols]:
        list_columns = []
        for i in column:
            list_columns.append(values[i])
        items_duplicated = []
        nb_duplicates = []
        for j in list_columns:

            if (list_columns.count(j) > 1):
                nb_duplicates.append(j)
                if not (j in items_duplicated):
                     items_duplicated.append(j)

        conflicts += len(nb_duplicates) - len(items_duplicated)

    return conflicts

def row_conflicts(values):
    conflicts = 0
    for row in [cross(r, cols) for r in rows]:  ## For rows
        list_rows = []

        for s in row:
            list_rows.append(values[s])

        items_duplicated = []
        nb_duplicates = []
        for j in list_rows:
            if (list_rows.count(j) > 1):
                nb_duplicates.append(j)
                if not(j in items_duplicated):
                  items_duplicated.append(j)

        conflicts += len(nb_duplicates) - len(items_duplicated)

    return conflicts

def conflicts_sum(values):
    conflits_total = row_conflicts(values)+columns_conflicts(values)
    return conflits_total


def hill_climbing(values, grid):
    current = values
    lst = []
    previous = []
    conflict = 5000
    nouv_values = None
    list_key_with_valeur = list_return_key_chiffre(grid)
    for s in squares:
        succ = current.copy()
        l = carre_list(remplissage(values))[s]
        filtered = [x for x in l if x not in previous and x not in list_key_with_valeur]
        for i in filtered:
            if (i != s):
                succ[i], succ[s] = succ[s], succ[i]
                lst.append(succ)
        previous.append(s)

    for j in lst:
        if (conflicts_sum(j) < conflict):
          conflict = conflicts_sum(j)
          nouv_values = j

    return nouv_values, conflict


def list_return_key_chiffre(grid):
     values_original = grid_values(grid)
     lst =[]
     for i  in values_original:
         if not(values_original[i] =='.'):
             lst.append(i)
     return lst

def solve_hillClimbing(grid): return hill_climbing(search(parse_grid(grid)),grid)

def carre_list(values):
    squares_and_grid = dict()
    neighbors = dict()
    lst=[]
    list_of_dict = dict()
    list_new =[]
    for key in values:
        lst.append(key)
    split_lst = np.array_split(lst, 9)
    for array in split_lst:
            list_new.append(list(array))

    for i in list_new:
        for j in i:
            copy_values = values.copy()
            l = random.choice(i)
            r = random.choice(i)
            if (l != r):
                copy_values[l], copy_values[r] = copy_values[r], copy_values[l]
                neighbors[l] = r

        for i in list_new:
            for j in i:
                squares_and_grid[j] = i

    return squares_and_grid

def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values  ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d))
                for d in values[s])


################ Utilities ################

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False


def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    return open(filename).read().strip().split(sep)


def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq


################ System test ################

import time, random


def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""

    def time_solve(grid):
        start = time.perf_counter()
        values = solve(grid)
        t = time.perf_counter() - start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print('(%.2f seconds)\n' % t)
        return (t, solved(values))

    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times) / N, N / sum(times), max(times)))


def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."

    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)

    return values is not False and all(unitsolved(unit) for unit in unitlist)


def random_puzzle(N=17):
    """Make a random puzzle with N or more assignments. Restart on contradictions.
    Note the resulting puzzle is not guaranteed to be solvable, but empirically
    about 99.8% of them are solvable. Some have multiple solutions."""
    values = dict((s, digits) for s in squares)
    for s in shuffled(squares):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= 8:
            return ''.join(values[s] if len(values[s]) == 1 else '.' for s in squares)
    return random_puzzle(N)  ## Give up and make a new puzzle


grid1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1 = '.....6....59.....82....8....45........3........6..3.54...325..6..................'

if __name__ == '__main__':
    test()
# solve_all(from_file("top95.txt"), "95sudoku", None)
# solve_all(from_file("easy50.txt", '========'), "easy", None)
# solve_all(from_file("easy50.txt", '========'), "easy", None)
solve_all(from_file("100sudoku.txt"), "hard", None)
# solve_all(from_file("1000sudoku.txt"), "hard", None)
# solve_all(from_file("hardest.txt"), "hardest", None)
# solve_all([random_puzzle() for _ in range(99)], "random", 100.0)


## References used:
## http://www.scanraid.com/BasicStrategies.htm
## http://www.sudokudragon.com/sudokustrategy.htm
## http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
## http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/
