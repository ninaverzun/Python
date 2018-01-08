def load_board_from_file(file_name):
    board = []
    with open(file_name, "r") as text:
        line = text.readline()
        while line != '':
            board.append([i for i in line if i.isdigit()])
            line = text.readline()
    return board


def check_board(board):
    for x in range(9):
        for y in range(9):
            if board[x][y] == '0' or board[y][x] == '0':
                return False
    return True


def is_input_valid(board, row, col, val):
    if val in board[row]:
        return False
    if val in [board[i][col] for i in range(9)]:
        return False
    return check_square(board, row//3, col//3, val)


def check_square(board, square_row, square_col, val):
    for row in range(square_row*3, square_row*3+3):
        for col in range(square_col*3, square_col*3+3):
            if board[row][col] == val:
                return False
    return True
