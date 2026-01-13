# student name:
# student number:

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
    row_size = len(board)
    col_size = len(board[0])

    # Get empty cell
    for row in range(row_size):
        for col in range(col_size):
            if board[row][col] == "c":
                empty_cells.append((row, col))

    # Choose between available cells
    # random.choice selects randomly in a given array
    if empty_cells:  # if empty_cells is not empty (i.e, there are spots available)
        row_chosen, col_chosen = random.choice(empty_cells)
        board[row_chosen, col_chosen] = 2


def isFull() -> bool:
    """
    returns True if no empty cell is left, False otherwise
    """
    pass  # to implement


def getCurrentScore() -> int:
    """
    calculates and returns the current score
    the score is the sum of all the numbers currently on the board
    """
    pass  # to implement


def updateTheBoardBasedOnTheUserMove(move: str) -> None:
    """
    updates the board variable based on the move argument by sliding and merging
    the move argument is either 'W', 'A', 'S', or 'D'
    directions: W for up; A for left; S for down, and D for right
    """
    pass  # to implement


# up to two new functions allowed to be added (if needed)
# as usual, they must be documented well
# they have to be placed below this line


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
