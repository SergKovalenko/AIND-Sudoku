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
                        twin = val
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
    # all_s = row_s + col_s + block_s

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
    print('this')
    print(values)
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


def eliminate(values):
    for key, val in values.items():

        if (len(val) == 1):
            row, col, block, diag, siblings = get_siblings(key)

            for s_key in siblings:
                values[s_key] = values[s_key].replace(val, '')

    return values

def only_choice(values):
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
                    assign_value(values, key, num)

        only(row, 'row')
        only(col, 'col')
        only(block, 'block')
        only(diag, 'diag')

    return values

def reduce_puzzle(values):
    # display(values)
    def check_nums(data):
        counter = 0

        for key, nums in data.items():
            counter += len(nums)

        return counter

    old_value = check_nums(values)
    new_value = old_value - 1
    iteration = 0
    while new_value < old_value:
        # print('before')
        # display(values)
        iteration += 1
        old_value = new_value
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        new_value = check_nums(values)
        # print('after')
        # display(values)
        for key, val in values.items():
            if (len(val) == 0):
                # print('reduce')
                # print('FAAAAAALSeeeeee')
                return False

    return values

def search(values):
    values = reduce_puzzle(values)

    if not values:
        # print('search')
        return False
    if all(len(values[key]) == 1 for key in values): 
        return values

    sorted_keys = []
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
    return search(grid_values(grid))
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

if __name__ == '__main__':
    # diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    # diag_sudoku_grid = '......8.68.........7..863.....8............8..8.5.9...1.8..............8.....8.4.' #naked twins test
    # diag_sudoku_grid = '4......5.32.4.......8.....................5..........12......97...6.4.38.......45' #naked twins test 2

    # diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # diag_sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    diag_sudoku_grid = '.....8..1..1............5.......3...6.3..52.....2....3.3...4....6.51....9........' #last check


    # value = {"D9": "47", "E4": "2", "I2": "2345678", "C2": "1234568", "B9":
    # "124578", "F4": "9", "D6": "5", "C6": "236789", "G9": "24578", "D2":
    # "9", "E9": "3", "E1": "567", "B4": "345678", "I7": "1", "I1":
    # "2345678", "C3": "1234569", "F8": "58", "A5": "1", "A7": "234568",
    # "G6": "1236789", "E2": "567", "E8": "1", "A3": "7", "B1": "2345689",
    # "G5": "23456789", "D8": "2", "I4": "345678", "C9": "124578", "H8":
    # "345678", "F7": "58", "F6": "37", "G4": "345678", "F9": "6", "H3":
    # "1234569", "A4": "34568", "A8": "345689", "B2": "1234568", "D5": "36",
    # "D7": "47", "H4": "345678", "B7": "2345678", "H5": "23456789", "G1":
    # "23456789", "G8": "345678", "A6": "23689", "F3": "24", "A2": "234568",
    # "E6": "4", "I3": "23456", "C4": "345678", "A1": "2345689", "H1":
    # "23456789", "B5": "23456789", "G7": "2345678", "G3": "1234569", "B8":
    # "3456789", "F5": "37", "C1": "2345689", "C8": "3456789", "C7":
    # "2345678", "E7": "9", "H9": "24578", "I8": "345678", "D3": "8", "F1":
    # "1", "A9": "2458", "H6": "1236789", "I9": "9", "C5": "23456789", "G2":
    # "12345678", "D1": "36", "I5": "2345678", "D4": "1", "F2": "24", "E3":
    # "56", "I6": "23678", "H2": "12345678", "B6": "236789", "H7":
    # "2345678", "E5": "678", "B3": "1234569"}

    # {"H6": "23568", "I7": "9", "I2": "123568", "G7": "1234568", "C9":
    #     "13456", "A5": "3468", "C3": "4678", "G9": "12345678", "G3": "245678",
    #     "E6": "23568", "F6": "23568", "I9": "1235678", "C6": "368", "A4": "5",
    #     "E9": "12345678", "B6": "1", "D6": "23568", "B2": "2", "C1": "4678",
    #     "F4": "23468", "I5": "35678", "I1": "123678", "E2": "123568", "A9":
    #     "2346", "B4": "46", "E8": "12345679", "A3": "1", "D8": "1235679",
    #     "A8": "2346", "G4": "23678", "A6": "7", "D4": "23678", "I4": "23678",
    #     "E1": "123689", "D3": "25689", "A2": "9", "B7": "7", "D7": "123568",
    #     "I6": "4", "B1": "5", "D1": "123689", "F9": "1234568", "B5": "46",
    #     "A1": "2468", "H5": "35678", "F3": "25689", "E4": "234678", "E5":
    #     "13456789", "D9": "1235678", "C4": "9", "C7": "13456", "E7":
    #     "1234568", "H7": "234568", "C8": "13456", "D2": "4", "F5": "1345689",
    #     "G6": "9", "B8": "8", "G5": "35678", "B3": "3", "E3": "25689", "F2":
    #     "7", "H2": "23568", "F7": "1234568", "G8": "1234567", "H1": "2346789",
    #     "D5": "1356789", "H9": "2345678", "H4": "1", "A7": "2346", "F8":
    #     "1234569", "B9": "9", "G1": "1234678", "H3": "2456789", "C2": "68",
    #     "G2": "123568", "C5": "2", "I8": "123567", "I3": "25678", "H8":
    #     "234567", "F1": "123689"}

    # display(value)
    # print('after')
    # display(naked_twins(value))

    display(solve(diag_sudoku_grid))
    # solve(diag_sudoku_grid)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
