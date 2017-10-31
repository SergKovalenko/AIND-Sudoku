assignments = []

letters = 'ABCDEFGHI'
numbers = '123456789'
blocks_rows = ('ABC', 'DEF', 'GHI')
blocks_nums = ('123', '456', '789')

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
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
    # Eliminate the naked twins as possibilities for their peers

def cross(A, B):
    keys_arr = [letter + num for letter in A for num in B]
    return keys_arr

def get_siblings(key):
    siblings = []

    rows = [cross(letter, numbers) for letter in letters]
    cols = [cross(letters, num) for num in numbers]
    blocks = [cross(rows, cols) for rows in blocks_rows for cols in blocks_nums]

    for row in rows:
        if key in row:
            row.remove(key)
            siblings = siblings + row

    for col in cols:
        if key in col:
            col.remove(key)
            siblings = siblings + col

    for block in blocks:            
        if key in block:
            block.remove(key)
            siblings = siblings + block

    return siblings

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
    empty_value = numbers

    keys_arr = cross(letters, numbers)
    grid_dict = {}

    for num in range(0, len(grid)):
        if grid[num] != '.':
            grid_dict[keys_arr[num]] = grid[num]
        else:
            grid_dict[keys_arr[num]] = empty_value

    return grid_dict


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """

    width = 9
    row_item = 0
    rows = 0
    table = ''

    for key in sorted(values.keys()):
        while len(values[key]) < width + 2:
            values[key] = ' ' + values[key] + ' '

        if row_item == 3 or row_item == 6:
            table = table + '|'

        row_item += 1

        if row_item <= width:
            table = table + values[key]
        else:
            row_item = 1
            table = table + '\n'
            rows += 1
            if rows == 3 or rows == 6:
                table = table + ('-' * width * (width + 2))
                table = table + '\n'     
            table = table + values[key]

    print(table)


def eliminate(values):
    for key, val in values.items():
        if (len(val) == 1):
            siblings = get_siblings(key)

            for s_key in siblings:
                if len(values[s_key]) > 1:
                    values[s_key] = values[s_key].replace(val, '')


    return values

def only_choice(values):
    pass

def reduce_puzzle(values):
    pass

def search(values):
    pass

def solve(grid):
    return eliminate(grid_values(grid))
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

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
