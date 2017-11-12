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
        # iterate all sibligs for each values with len == 2
        if (len(val) == 2):
            row, col, block, diag, siblings = get_siblings(key)


            def find_twin_in(keys):
                # keys is siblings keys

                twin = False

                # iterate to find is there is twin
                for key1 in keys:
                    if values[key1] == val:
                        twin = val

                # second iteration to remove twins values from other siblings
                if twin:
                    for key2 in keys:
                        if (values[key2] != val):
                            for num in val:
                                values[key2] = values[key2].replace(num, '')
                                if (len(values[key2]) == 1):
                                    assign_value(values, key2, values[key2])

            find_twin_in(row)
            find_twin_in(col)
            find_twin_in(block)
            # find_twin_in(diag)

    return values

def get_siblings(key):
    """find all siblings types of current key.
    Args:
        values(strng): string of key value 'A1, A2, B1, B2...'

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
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

    # center key has both diaglonal lines as siblings
    if key == 'E5': 
        diag_s = []
        for diag in diags:
            for item in diag:
                if (item != 'E5'):
                    diag_s.append(item)

    #all siblings
    all_s = row_s + col_s + block_s + diag_s

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

        # add separator greed for cols blocks
        if row_item == 3 or row_item == 6:
            table = table + '|'

        row_item += 1

        if row_item <= width:
            table = table + display_values[key]
        else:
            row_item = 1
            table = table + '\n'
            rows += 1
            # add separators for column blocks
            if rows == 3 or rows == 6:
                table = table + ('-' * width * (width + 2))
                table = table + '\n'     
            table = table + display_values[key]

    print(table)


def eliminate(values):
    """
    Eliminate all values that definitely can't be used to solve puzzle
    Args:
        values(dict): The sudoku in dictionary form
    """
    for key, val in values.items():

        if (len(val) == 1):
            row, col, block, diag, siblings = get_siblings(key)

            for s_key in siblings:
                values[s_key] = values[s_key].replace(val, '')

    return values


def only_choice(values):
    """
    Assighn value to key, if this value is unique among all siblings type
    Args:
        values(dict): The sudoku in dictionary form
    """
    for key, val in values.items():
        if len(val) == 1:
            continue

        row, col, block, diag, all_s = get_siblings(key)

        def only(keys, type):
            if len(keys) == 0:
                return

            # hom many times each number occurs in current (row, col, block, diag)
            num_dict = { '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0 }

            # count numbers from current value
            for num1 in val:
                num_dict[num1] += 1
            # count numbers from siblings
            for key1 in keys:
                for num2 in values[key1]:
                    num_dict[num2] +=1
            for num, count in num_dict.items():
                # unique value
                if count == 1 and num in val:
                    assign_value(values, key, num)

        only(row, 'row')
        only(col, 'col')
        only(block, 'block')
        only(diag, 'diag')

    return values


def reduce_puzzle(values):
    """
    Use 'eliminate' and 'only_choice' function in cycles, till they can reduce puzzle
    Args:
        values(dict): The sudoku in dictionary form
    """
    def check_nums(data):
        counter = 0

        for key, nums in data.items():
            counter += len(nums)

        return counter

    #number of nums in sudoku before current step of reduction
    old_value = check_nums(values)
    #number of nums in sudoku after current step of puzzle reduction (set -1 to old value, just to do first reduction iteration)
    new_value = old_value - 1

    while new_value < old_value:
        old_value = new_value
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        new_value = check_nums(values)

        for key, val in values.items():
            if (len(val) == 0):
                return False

    return values


def search(values):
    """
    Try different nums of not reduced values and check can we solve puzzle with selected num.
    Args:
        values(dict): The sudoku in dictionary form
    """
    values = reduce_puzzle(values)

    if not values:
        return False
    if all(len(values[key]) == 1 for key in values): 
        return values

    sorted_keys = []
    # keys in this dict is longevity of keys that are inside lists
    len_of_values = { 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [] }

    for key, val in values.items():
        if len(val) > 1:
            len_of_values[len(val)].append(key)

    for key in sorted(len_of_values.keys()):
        sorted_keys = sorted_keys + len_of_values[key]

    for num in values[sorted_keys[0]]:
        attempt_values = values.copy()
        attempt_values[sorted_keys[0]] = num

        new_values = search(attempt_values)
        if new_values:
            return new_values


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


if __name__ == '__main__':
    # diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    # diag_sudoku_grid = '......8.68.........7..863.....8............8..8.5.9...1.8..............8.....8.4.' #naked twins test
    # diag_sudoku_grid = '4......5.32.4.......8.....................5..........12......97...6.4.38.......45' #naked twins test 2

    # diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # diag_sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    diag_sudoku_grid = '.....8..1..1............5.......3...6.3..52.....2....3.3...4....6.51....9........' #last check


    display(solve(diag_sudoku_grid))
    # solve(diag_sudoku_grid)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
