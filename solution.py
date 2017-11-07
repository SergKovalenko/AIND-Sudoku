assignments = []

letters = 'ABCDEFGHI'
numbers = '123456789'
blocks_lets = ('ABC', 'DEF', 'GHI')
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

def cross(A, B):
    keys_arr = [letter + num for letter in A for num in B]
    return keys_arr

rows = [cross(letter, numbers) for letter in letters]
cols = [cross(letters, num) for num in numbers]
blocks = [cross(lets, nums) for lets in blocks_lets for nums in blocks_nums]
diags = [[letters[idx] + numbers[idx] for idx, val in enumerate(numbers)],
         [letters[idx] + numbers[::-1][idx] for idx, val in enumerate(numbers)]]

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for key, val in values.items():
        if (len(val) == 2):
            row, col, block, diag, siblings = get_siblings(key)

            def find_twin_in(keys):
                twin = False

                for key1 in keys:
                    if values[key1] == val:
                        twin = True
                if twin:
                    for key2 in keys:
                        if (len(values[key2]) > 2):
                            for num in val:
                                values[key2] = values[key2].replace(num, '')

            find_twin_in(row)
            find_twin_in(col)
            find_twin_in(block)
            #ToDo
            # find_twin_in(diag)

    return values

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def get_siblings(key):
    all_s = []
    row_s = []
    col_s = []
    block_s = []
    diag_s = []

    for row in rows:
        if key in row:
            row1 = row[:]
            row1.remove(key)
            row_s = row1

    for col in cols:
        if key in col:
            col1 = col[:]
            col1.remove(key)
            col_s = col1

    for block in blocks:            
        if key in block:
            block1 = block[:]
            block1.remove(key)
            block_s = block1

    for diag in diags:            
        if key in diag:
            diag1 = diag[:]
            diag1.remove(key)
            diag_s = diag1

    if key == 'E5':
        diag_s = []
        for diag in diags:
            for item in diag:
                if (item != 'E5'):
                    diag_s.append(item)

    all_s = row_s + col_s + block_s + diag_s
    #ToDo
    all_s = row_s + col_s + block_s
    return row_s, col_s, block_s, diag_s, all_s

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
    display_values = values.copy()

    width = 9
    row_item = 0
    rows = 0
    table = ''

    for key in sorted(display_values.keys()):
        while len(display_values[key]) < width + 2:
            display_values[key] = ' ' + display_values[key] + ' '

        if row_item == 3 or row_item == 6:
            table = table + '|'

        row_item += 1

        if row_item <= width:
            table = table + display_values[key]
        else:
            row_item = 1
            table = table + '\n'
            rows += 1
            if rows == 3 or rows == 6:
                table = table + ('-' * width * (width + 2))
                table = table + '\n'     
            table = table + display_values[key]

    print(table)


def eliminate(values, iteration):
    for key, val in values.items():
        if (len(val) == 1):
            row, col, block, diag, siblings = get_siblings(key)
            for s_key in siblings:
                if len(values[s_key]) > 1:
                    values[s_key] = values[s_key].replace(val, '')


    return values

def only_choice(values, iteration):
    for key, val in values.items():
        if len(val) == 1:
            continue

        
        row, col, block, diag, all_s = get_siblings(key)

        def only(keys, type):
            if len(keys) == 0:
                return

            num_dict = { '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0 }

            for num1 in val:
                num_dict[num1] += 1
            for key1 in keys:
                for num2 in values[key1]:
                    num_dict[num2] +=1
            for num, count in num_dict.items():
                if count == 1 and num in val:
                    # values[key] = num
                    assign_value(values, key, num)

        only(row, 'row')
        only(col, 'col')
        only(block, 'block')
        #ToDo
        # only(diag, 'diag')
    return values

def reduce_puzzle(values):
    def check_nums(data):
        counter = 0

        for key, nums in data.items():
            counter += len(nums)

        return counter
    #ToDo
    # values = grid_values(values)
    old_value = check_nums(values)
    new_value = old_value - 1
    iteration = 0
    while new_value < old_value:

        # print('next')
        # display(values)
        iteration += 1
        old_value = new_value
        values = eliminate(values, iteration)

        values = only_choice(values, iteration)
        values = naked_twins(values)
        new_value = check_nums(values)

        for key, val in values.items():
            if (len(val) == 0):
                return False

    return values


def search(values):
    values = {
        'D9': '123456789', 'G5': '123456789', 'B8': '123456789', 'C1': '123456789',
        'H5': '123456789', 'C9': '123456789', 'I8': '123456789', 'H6': '123456789',
        'I9': '123456789', 'D6': '123456789', 'F7': '123456789', 'I7': '123456789',
        'B3': '123456789', 'B6': '123456789', 'B9': '123456789', 'C5': '123456789',
        'I5': '123456789', 'E2': '123456789', 'B7': '123456789', 'B1': '123456789',
        'A5': '123456789', 'G4': '6', 'A4': '123456789', 'C7': '123456789', 'A8': '123456789',
        'E7': '4', 'F9': '123456789', 'A7': '8', 'E8': '123456789', 'F5': '1', 'E3': '123456789',
        'F4': '123456789', 'H4': '2', 'G8': '7', 'D3': '123456789', 'G1': '123456789',
        'I2': '123456789', 'D2': '2', 'A1': '4', 'F3': '123456789', 'F2': '123456789', 'G9': '123456789',
        'E4': '123456789', 'H7': '123456789', 'E9': '123456789', 'I4': '123456789', 'B4': '123456789',
        'G3': '123456789', 'D7': '123456789', 'A9': '5', 'C8': '123456789', 'F6': '123456789', 'F8': '123456789',
        'E1': '123456789', 'A6': '123456789', 'G2': '123456789', 'I1': '1', 'G7': '123456789', 'G6': '3',
        'A2': '123456789', 'A3': '123456789', 'H1': '5', 'C2': '123456789', 'D1': '123456789',
        'C4': '7', 'H8': '123456789', 'H9': '123456789', 'H3': '123456789', 'D5': '123456789',
        'B2': '3', 'E6': '123456789', 'E5': '8', 'I3': '4', 'F1': '123456789', 'D4': '123456789',
        'B5': '123456789', 'H2': '123456789', 'D8': '6', 'C3': '123456789', 'I6': '123456789', 'C6': '123456789'
    }

    # row, col, block, diag, all_s = get_siblings(key)

    values = reduce_puzzle(values)
    # if values is False:
    #     return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    sorted_values = []

    for key, val in values:

    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        attempt_values = values.copy()
        attempt_values[s] = value
        new_values = search(attempt_values)
        if new_values:
            return new_values

def solve(grid):
    return search(grid)
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
    # reduce_puzzle(diag_sudoku_grid)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
