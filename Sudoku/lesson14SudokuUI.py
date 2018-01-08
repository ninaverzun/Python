from tkinter import *
from tkinter import messagebox

from Sudoku.lesson14Sudoku import *

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board


class SudokuUI(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        self.grid(sticky=W+E+N+S)
        self.winfo_toplevel().title("Nina's Sudoku")
        self.canvas = Canvas(self, height=HEIGHT, width=WIDTH, bg="white")
        self.canvas.grid(sticky=W+E+N+S)
        self.clear_btn = Button(self,
                                text="Reset",
                                command=self.reset_board,
                                ).grid(columnspan=4, sticky=W+E)
        self.orig_board = load_board_from_file("sudoku_template")
        self.board = [i[:] for i in self.orig_board]
        self.row = self.col = 0.0
        left = MARGIN + SIDE * self.col
        top = MARGIN + SIDE * self.row
        self.focus_rec = self.canvas.create_rectangle(left, top, left + SIDE, top + SIDE, fill="white")
        self.canvas.bind("<ButtonPress>", self.on_click)
        self.canvas.bind("<Key>", self.on_button_press)

        self.__draw_grid()
        self.__draw_puzzle(self.board)
        self.selected = FALSE

    def on_button_press(self, event):
        if self.orig_board[int(self.row)][int(self.col)] != '0':
            messagebox.showerror("Invalid input", "Please fill only empty or green colored spots!")
            return
        if not event.char.isdigit() or int(event.char) < 1 or int(event.char) > 9:
            messagebox.showerror("Invalid input", "Please enter a number between 1 and 9!")
            return
        if not is_input_valid(self.board, int(self.row), int(self.col), event.char):
            messagebox.showerror("Invalid input", "Please enter a number that was't yet selected in the same row, "
                                                  "column or 3x3 blue edged square!")
            return
        self.board[int(self.row)][int(self.col)] = event.char
        self.__draw_puzzle(self.board)

    def on_click(self, event):
        self.canvas.focus_set()
        col = (event.x - MARGIN) // SIDE
        row = (event.y - MARGIN) // SIDE
        color = "yellow"
        if (self.orig_board[row][col] != '0') or (self.selected and col == self.col and row == self.row):
            color = "white"
        #else:
        self.row = row
        self.col = col

        self.selected = not self.selected
        self.draw_cursor(color)
        print("clicked: ", "(", self.row, ",", self.col, ")\n")

    def draw_cursor(self, color):
        if 0 > self.row or self.row > 8 or 0 > self.col or self.col > 8:
            return
        left = MARGIN + SIDE * self.col
        top = MARGIN + SIDE * self.row
        self.canvas.coords(self.focus_rec, left, top, left + SIDE, top + SIDE)
        self.canvas.itemconfig(self.focus_rec, fill=color)

    def __draw_puzzle(self, board):
        self.canvas.delete("numbers")
        for row in range(9):
            print()
            for col in range(9):
                print(board[row][col], end="")
                if int(board[row][col]) != 0:
                    color = "black"
                    if self.orig_board[row][col] != board[row][col]:
                        color = "sea green"
                    self.canvas.create_text(MARGIN + SIDE/2 + col*SIDE, MARGIN + SIDE/2 + row*SIDE, text=board[row][col],
                                            tags="numbers", fill=color)
        print()
        if check_board(self.board):
            self.show_win()

    def show_win(self):
        self.canvas.create_oval(MARGIN+30, MARGIN+30, WIDTH-MARGIN-30, WIDTH-MARGIN-30, fill="pink")
        self.canvas.create_text(WIDTH/2, HEIGHT/2, font="Purisa", text="You Won!")

    def reset_board(self):
        self.board = [i[:] for i in self.orig_board]
        self.__draw_puzzle(self.board)
        self.canvas.itemconfig(self.focus_rec, fill="white")

    def __draw_grid(self):
        w = WIDTH
        h = HEIGHT
        m = MARGIN

        blue_gap = (HEIGHT - 2*MARGIN)/3
        grey_gap = blue_gap/3

        for i in range(0, 4):
            blue = m + i * blue_gap
            grey1 = blue + grey_gap
            grey2 = blue + 2 * grey_gap
            #horizontal BLUE lines
            self.canvas.create_line(m, blue, w - m, blue, fill="blue")
            self.canvas.create_line(m, grey1, w - m, grey1, fill="grey")
            self.canvas.create_line(m, grey2, w - m, grey2, fill="grey")
            #vertical BLUE lines
            self.canvas.create_line(blue, m, blue, h - m, fill="blue")
            self.canvas.create_line(grey1, m, grey1, h - m, fill="grey")
            self.canvas.create_line(grey2, m, grey2, h - m, fill="grey")



root = Tk()
sudoku_ui = SudokuUI(root)
root.mainloop()
