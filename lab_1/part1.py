# student name: Gyan Edbert Zesiro
# student number: 38600060

# A command-line 2048 game

import random


board: list[list] = []  # a 2-D list to keep the current status of the game board


def init() -> None:  # Use as is
    """
    initializes the board variable
    and prints a welcome message
    """
    # initialize the board cells with ''
    for _ in range(4):
        rowList = []
        for _ in range(4):
            rowList.append("")
        board.append(rowList)
    # add two starting 2's at random cells
    twoRandomNumbers = random.sample(
        range(16), 2
    )  # randomly choose two numbers between 0 and 15
    # correspond each of the two random numbers to the corresponding cell
    twoRandomCells = (
        (twoRandomNumbers[0] // 4, twoRandomNumbers[0] % 4),
        (twoRandomNumbers[1] // 4, twoRandomNumbers[1] % 4),
    )
    for cell in twoRandomCells:  # put a 2 on each of the two chosen random cells
        board[cell[0]][cell[1]] = 2

    print()
    print("Welcome! Let's play the 2048 game.")
    print()


def displayGame() -> None:  # Use as is
    """displays the current board on the console"""
    print("+-----+-----+-----+-----+")
    for row in range(4):
        for column in range(4):
            cell = board[row][column]
            print(f"|{str(cell).center(5)}", end="")
        print("|")
        print("+-----+-----+-----+-----+")


def promptGamerForTheNextMove() -> str:  # Use as is
    """
    prompts the gamer until a valid next move or Q (to quit) is selected
    (valid move direction: one of 'W', 'A', 'S' or 'D')
    returns the user input
    """
    print("Enter one of WASD (move direction) or Q (to quit)")
    while True:  # prompt until a valid input is entered
        move = input("> ").upper()
        if move in ("W", "A", "S", "D", "Q"):  # a valid move direction or 'Q'
            break
        print(
            'Enter one of "W", "A", "S", "D", or "Q"'
        )  # otherwise inform the user about valid input
    return move


def addANewTwoToBoard() -> None:
    """
    adds a new 2 at an available randomly-selected cell of the board
    """
    # Algorithm:
    # - Get empty cell
    # - Call random on available index
    #
    empty_cells = []
    row_size = len(board)  # Configurable board size in case we're not playing 4x4
    col_size = len(board[0])

    # Get empty cell
    for row in range(row_size):
        for col in range(col_size):
            if board[row][col] == "":
                empty_cells.append((row, col))

    # Choose between available cells
    # random.choice selects randomly in a given array
    if empty_cells:  # if empty_cells is not empty (i.e, there are spots available)
        row_chosen, col_chosen = random.choice(empty_cells)
        board[row_chosen][col_chosen] = 2


def isFull() -> bool:
    """
    returns True if no empty cell is left, False otherwise
    """
    # Algorithm:
    # - check all cell state, similar to addANewTwoToBoard()
    # the only difference is that we can use early exit
    # to make our program faster
    row_size = len(board)
    col_size = len(board[0])

    for row in range(row_size):
        for col in range(col_size):
            if board[row][col] == "":  # if any cell is empty, exit early
                return False

    # If all cells are occupied, return true
    return True


def getCurrentScore() -> int:
    """
    calculates and returns the current score
    the score is the sum of all the numbers currently on the board
    """
    # Algorithm:
    # - same as the 2 previous functions, go through all cell and
    # add the cell content to a number
    # but we need to check for empty cells to avoid error
    current_score = 0
    row_size = len(board)
    col_size = len(board[0])

    for row in range(row_size):
        for col in range(col_size):
            if board[row][col] != "":
                current_score += board[row][col]

    return current_score


def updateTheBoardBasedOnTheUserMove(move: str) -> None:
    """
    updates the board variable based on the move argument by sliding and merging
    the move argument is either 'W', 'A', 'S', or 'D'
    directions: W for up; A for left; S for down, and D for right
    """
    global board
    row_size = len(board)
    col_size = len(board[0])

    # Convert all cases to sliding to the left
    # Once converted to the left, apply the slide and merge left algorithm
    # Convert back to original case (left stays unchanged)
    if move == "A":
        print("test")
        for row_index in range(row_size):
            board[row_index] = slideLeftAndMergeRow(
                board[row_index]
            )  # Slide and merge left algorithm
    elif move == "D":
        for row_index in range(row_size):
            board[row_index].reverse()
            board[row_index] = slideLeftAndMergeRow(board[row_index])
            board[row_index].reverse()
    elif move == "W":
        board = transposeBoard(board)  # Matrix Transpose
        for row_index in range(row_size):
            board[row_index] = slideLeftAndMergeRow(board[row_index])
        board = transposeBoard(board)
    elif move == "S":
        board = transposeBoard(board)
        for row_index in range(row_size):
            board[row_index].reverse()
            board[row_index] = slideLeftAndMergeRow(board[row_index])
            board[row_index].reverse()
        board = transposeBoard(board)
    # Program shouldn't go here, but just in case there will be a logic path error
    else:
        raise RuntimeError("Unexpected logic path")


# up to two new functions allowed to be added (if needed)
# as usual, they must be documented well
# they have to be placed below this line


def slideLeftAndMergeRow(row_array: list) -> list:
    """
    Slide and merge array for the 2048 game to the left
    row_array: one row of the 2048 board
    """
    final_cell = []

    non_empty_cells = [x for x in row_array if x != ""]
    # Same idea as above, just more "pythonic" as they say
    # for index in range(len(row_array)):
    #     if row_array[i] != '':
    #         non_empty_cells.append(row_array[i])

    is_merged = False  # Flag to check if merging occured
    non_empty_array_length = len(non_empty_cells)

    for index in range(non_empty_array_length):
        if is_merged:
            is_merged = False
            continue

        if (
            index + 1 < non_empty_array_length
            and non_empty_cells[index] == non_empty_cells[index + 1]
        ):
            final_cell.append(non_empty_cells[index] * 2)  # merging two adjacent cells
            is_merged = True
        else:
            final_cell.append(non_empty_cells[index])

    # Fill the rest with empty cells
    while len(final_cell) < len(row_array):
        final_cell.append("")

    return final_cell


def transposeBoard(current_board: list[list]) -> list[list]:
    """
    Do a tranpose (swap column and rows)
    current_board: matrix to be tranposed
    """
    new_board = []
    row_size = len(current_board)
    col_size = len(current_board[0])

    for col in range(col_size):
        new_row = []
        for row in range(row_size):
            new_row.append(current_board[row][col])
        new_board.append(new_row)

    return new_board


if __name__ == "__main__":  # Use as is
    init()
    displayGame()
    while True:  # Super-loop for the game
        print(f"Score: {getCurrentScore()}")
        userInput = promptGamerForTheNextMove()
        if userInput == "Q":
            print("Exiting the game. Thanks for playing!")
            break
        updateTheBoardBasedOnTheUserMove(userInput)
        addANewTwoToBoard()
        displayGame()

        if isFull():  # game is over once all cells are taken
            print("Game is Over. Check out your score.")
            print("Thanks for playing!")
            break
