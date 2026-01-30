# student name: Gyan Edbert Zesiro
# student number: 38600060

import multiprocessing as mp


def checkColumn(puzzle: list, column: int):
    """
    param puzzle: a list of lists containing the puzzle
    param column: the column to check (a value between 0 to 8)

    This function checks the indicated column of the puzzle, and
    prints whether it is valid or not.

    As usual, this function must not mutate puzzle
    """
    validValue = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    columnValues = []
    # Extract and store column data
    for row in range(9):
        columnValues.append(puzzle[row][column])
    # Check if the column is valid or not
    if set(columnValues) == validValue:
        print(f"Column {column} valid")
    else:
        print(f"Column {column} not valid")


def checkRow(puzzle: list, row: int):
    """
    param puzzle: a list of lists containing the puzzle
    param row: the row to check (a value between 0 to 8)

    This function checks the indicated row of the puzzle, and
    prints whether it is valid or not.

    As usual, this function must not mutate puzzle
    """
    validValue = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    # Get row data
    rowValues = puzzle[row]

    # Check if row data is valid
    if set(rowValues) == validValue:
        print(f"Row {row} valid")
    else:
        print(f"Row {row} not valid")


def checkSubgrid(puzzle: list, subgrid: int):
    """
    param puzzle: a list of lists containing the puzzle
    param subgrid: the subgrid to check (a value between 0 to 8)
    Subgrid numbering order:    0 1 2
                                3 4 5
                                6 7 8
    where each subgrid itself is a 3x3 portion of the original list

    This function checks the indicated subgrid of the puzzle, and
    prints whether it is valid or not.

    As usual, this function must not mutate puzzle
    """
    validValue = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    # Calculate the starting row and column indices
    # Subgrids 0,1,2 start at row 0; 3,4,5 row 3; 6,7,8 row 6
    startRow = (subgrid // 3) * 3  # Math works out to above
    # Subgrids 0,3,6 starts at col 0; 1,4,7 col 3, 2,5,8 col 6
    startCol = (subgrid % 3) * 3

    subgridItems = []

    # Check through the 3 x 3 grid
    for row in range(startRow, startRow + 3):
        for col in range(startCol, startCol + 3):
            subgridItems.append(puzzle[row][col])

    if set(subgridItems) == validValue:
        print(f"Subgrid {subgrid} valid")
    else:
        print(f"Subgrid {subgrid} not valid")


if __name__ == "__main__":
    # Test 1: default test from Canvas. A completely valid Sudoku puzzle
    test1 = [
        [6, 2, 4, 5, 3, 9, 1, 8, 7],
        [5, 1, 9, 7, 2, 8, 6, 3, 4],
        [8, 3, 7, 6, 1, 4, 2, 9, 5],
        [1, 4, 3, 8, 6, 5, 7, 2, 9],
        [9, 5, 8, 2, 4, 7, 3, 6, 1],
        [7, 6, 2, 3, 9, 1, 4, 5, 8],
        [3, 7, 1, 9, 5, 6, 8, 4, 2],
        [4, 9, 6, 1, 8, 2, 5, 7, 3],
        [2, 8, 5, 4, 7, 3, 9, 1, 6],
    ]
    # Test 2: default test from Canvas
    # Rows are valid (repeating sets), but columns and subgrids are invalid
    test2 = [
        [6, 2, 4, 5, 3, 9, 1, 8, 7],
        [5, 1, 9, 7, 2, 8, 6, 3, 4],
        [8, 3, 7, 6, 1, 4, 2, 9, 5],
        [6, 2, 4, 5, 3, 9, 1, 8, 7],
        [5, 1, 9, 7, 2, 8, 6, 3, 4],
        [8, 3, 7, 6, 1, 4, 2, 9, 5],
        [6, 2, 4, 5, 3, 9, 1, 8, 7],
        [5, 1, 9, 7, 2, 8, 6, 3, 4],
        [8, 3, 7, 6, 1, 4, 2, 9, 5],
    ]

    # Test 3: Contains values out of range (0 and 10)
    # Row 0 has a 0 and a 10.
    test3 = [
        [0, 2, 4, 5, 3, 9, 1, 8, 10],
        [5, 1, 9, 7, 2, 8, 6, 3, 4],
        [8, 3, 7, 6, 1, 4, 2, 9, 5],
        [1, 4, 3, 8, 6, 5, 7, 2, 9],
        [9, 5, 8, 2, 4, 7, 3, 6, 1],
        [7, 6, 2, 3, 9, 1, 4, 5, 8],
        [3, 7, 1, 9, 5, 6, 8, 4, 2],
        [4, 9, 6, 1, 8, 2, 5, 7, 3],
        [2, 8, 5, 4, 7, 3, 9, 1, 6],
    ]

    # Test 4: Contains invalid data types (strings instead of ints)
    # Row 0 has strings '6' and '7'
    test4 = [
        ["6", 2, 4, 5, 3, 9, 1, 8, "7"],
        [5, 1, 9, 7, 2, 8, 6, 3, 4],
        [8, 3, 7, 6, 1, 4, 2, 9, 5],
        [1, 4, 3, 8, 6, 5, 7, 2, 9],
        [9, 5, 8, 2, 4, 7, 3, 6, 1],
        [7, 6, 2, 3, 9, 1, 4, 5, 8],
        [3, 7, 1, 9, 5, 6, 8, 4, 2],
        [4, 9, 6, 1, 8, 2, 5, 7, 3],
        [2, 8, 5, 4, 7, 3, 9, 1, 6],
    ]

    # Test 5: Contains duplicates
    # Row 0 has two 1s (at index 0, 6) and is missing the 6.
    test5 = [
        [1, 2, 4, 5, 3, 9, 1, 8, 7],
        [5, 1, 9, 7, 2, 8, 6, 3, 4],
        [8, 3, 7, 6, 1, 4, 2, 9, 5],
        [1, 4, 3, 8, 6, 5, 7, 2, 9],
        [9, 5, 8, 2, 4, 7, 3, 6, 1],
        [7, 6, 2, 3, 9, 1, 4, 5, 8],
        [3, 7, 1, 9, 5, 6, 8, 4, 2],
        [4, 9, 6, 1, 8, 2, 5, 7, 3],
        [2, 8, 5, 4, 7, 3, 9, 1, 6],
    ]

    testcase = test5  # modify here for other testcases
    SIZE = 9

    processes = []

    print("Starting Multiprocessing Sudoku Validation")

    # Create all 27 process
    for i in range(SIZE):
        # Column checker
        pCol = mp.Process(target=checkColumn, args=(testcase, i))
        processes.append(pCol)

        pRow = mp.Process(target=checkRow, args=(testcase, i))
        processes.append(pRow)

        pSubgrid = mp.Process(target=checkSubgrid, args=(testcase, i))
        processes.append(pSubgrid)

    # Start process
    for process in processes:
        process.start()

    # Join process
    for process in processes:
        process.join()

    print("Part 2 finished")
