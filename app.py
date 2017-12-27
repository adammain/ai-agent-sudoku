assignments = []


def cross(strA, strB):
    # Concatinate letter a from string A with letter B from str B
    # ...creates cols/row ID (A1, A2, etc.) for each box on board
    return [char_a + char_b for char_a in strA for char_b in strB]

cols = '123456789'
rows = 'ABCDEFGHI'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
diagonal_units = [[(rd + str(cd + 1)) for cd, rd in enumerate(rows)],
                  [(rd + str(cd + 1)) for cd, rd in enumerate(reversed(rows))]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any
    # values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    for unit in unitlist:
        seen = set()
        dup_boxes = []
        potential_twins = [pt for pt in unit if len(values[pt]) == 2]

        # if box values in unit have length of 2, check values are equal
        if len(potential_twins) > 1:
            for pt in potential_twins:
                if values[pt] not in seen:
                    seen.add(values[pt])
                else:
                    dup_boxes.append(pt)

        # Eliminate the naked twins values from peer values
        if len(dup_boxes) > 0:
            dup_value = values[dup_boxes[0]]
            for d in dup_value:
                for u in unit:
                    if d in values[u] and dup_value != values[u]:
                        old_val = values[u]
                        new_value = old_val.replace(d, '')
                        assign_value(values, u, new_value)
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    new_grid = []

    for b in grid:
        if b == '.':
            new_grid.append(cols)
        else:
            new_grid.append(b)
    assert len(new_grid) == 81, "Input grid must be a string of length 81 (9x9)"
    return dict(zip(boxes, new_grid))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if values:
        width = 1 + max(len(values[s]) for s in boxes)
        line = '+'.join(['-' * (width * 3)] * 3)
        for r in rows:
            print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                          for c in cols))
            if r in 'CF':
                print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    # Get solved boxes (boxes with only 1 value left)
    solved_boxes = dict([(box, values[box])
                         for box in values if len(values[box]) == 1])

    # Remove the solved boxes's value from its peers (row/col/diag)
    for sb in solved_boxes:
        for p in peers[sb]:
            old_value = values[p]
            new_value = old_value.replace(solved_boxes[sb], '')
            assign_value(values, p, new_value)
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            only_choices = []

            for box in unit:
                if digit in values[box]:
                    only_choices.append(box)

            if len(only_choices) == 1:
                assign_value(values, only_choices[0], digit)
    return values


def reduce_puzzle(values):
    """
    Iterate naked_twins(), eliminate(), and only_choice().
    If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    # Continue running all strategy functions until puzzle solved or stuck:
    stalled = False
    while not stalled:
        solved_boxes_before = [box for box in values if len(values[box]) == 1]
        values = naked_twins(only_choice(eliminate(values)))
        solved_boxes_after = [box for box in values if len(values[box]) == 1]
        stalled = len(solved_boxes_before) == len(solved_boxes_after)
        dead_end = [box for box in values if len(values[box]) == 0]

        if dead_end:
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # # First, reduce the puzzle using the strategy functions
    values = reduce_puzzle(values)

    # Check if search branch is dead end
    if values == False:
        return False  # search branch dead end

    # Return solved puzzle
    solved_boxes = [box for box in boxes if len(values[box]) == 1]
    all_boxes_solved = len(solved_boxes) == 81
    if all_boxes_solved:
        return values

    # # Choose one of the unfilled squares with the fewest possibilities
    box_len, start_search_box = min((len(values[box]), box)
                                    for box in values if len(values[box]) > 1)

    # # Recursion to solve each one of the resulting sudokus
    # if one returns a value (not False), return answer
    for digit in values[start_search_box]:
        values_copy = values.copy()
        values_copy[start_search_box] = digit
        attempt = search(values_copy)

        # attempt solution
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solution = search(values)
    if solution:
        return solution
    else:
        return False

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    diag_sudoku_grid3 = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'

    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a \
             problem! It is not a requirement.')
