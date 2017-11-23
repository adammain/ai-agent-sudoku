assignments = []
cols = '123456789'
rows = 'ABCDEFGHI'


def cross(strA, strB):
    # Concatinate letter a from string A with letter B from str B
    # ...creates cols/row ID (A1, A2, etc.) for each box on board
    return [char_a + char_b for char_a in strA for char_b in strB]

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
    new_grid = []

    for b in grid:
        if b == '.':
            new_grid.append(cols)
        else:
            new_grid.append(b)
    assert len(new_grid) == 81, "Input grid must be a string of length 81 (9x9)"
    return pass


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
