def main():
    board = [
        ' ', ' ', ' ',
        ' ', ' ', ' ',
        ' ', ' ', ' '
    ]

    currentPlayer = 1
    gameOver = False
    moveCount = 0

    while not gameOver:
        printBoard(board)
        print("Player 1's Turn" if currentPlayer == 1 else "Player 2's Turn")
        cell = int(input("Enter Board Spot: "))

        validMove = placeOnBoard(board, cell, currentPlayer)

        if not validMove:
            continue
        moveCount += 1
        currentPlayer += 1
        currentPlayer %= 2

        winner = checkWinner(board)

        if winner is not None:
            print(winner, "wins!")
            exit()
        if moveCount == 9:
            gameOver = True
            print("The game is a cat's game (tie)!")


def printBoard(board):
    for i in range(0, 9, 3):
        print(f"{board[i]} | {board[i + 1]} | {board[i + 2]}")

        if i < 6:
            print("--+---+--")
def placeOnBoard(board, cell, currentPlayer):
    if cell < 1 or cell > 9:
        print("Invalid Cell")
        return False

    cell -= 1

    if board[cell] != ' ':
        print("Cell already taken!")
        return False

    board[cell] = "X" if currentPlayer == 1 else "O"
    return True
def checkWinner(board):
    winningLines = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for first, second, third in winningLines:
        if (
            board[first] != ' '
            and board[first] == board[second]
            and board[second] == board[third]
        ):
            return board[first]

    return None


main()