from tkinter import *
from logic import *
from random import *

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
STATUS_COLOR = "#ababab"
BACKGROUND_COLOR_DICT = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", \
                            32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", \
                            512:"#edc850", 1024:"#edc53f", 2048:"#edc22e" }
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                    32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                    512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" }
FONT = ("Verdana", 40, "bold")
STATUS_FONT = ("Verdana", 20, "bold")

KEY_UP = "'Up'"
KEY_DOWN = "'Down'"
KEY_LEFT = "'Left'"
KEY_RIGHT = "'Right'"

class GameGrid(Frame):
    def __init__(self, regime):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.commands = {   KEY_UP: up, KEY_DOWN: down, KEY_LEFT: left, KEY_RIGHT: right }

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="news")
        self.grid_cells = []
        self.score = 15
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()

        if regime == "masnual":
            self.mainloop()
        else:
            while game_state(self.matrix) != 'lose':
                #ODAVDE KRECE LOGIKA
                depth = 0
                if(len(get_empty_tiles(self.matrix)) < 5):
                    depth = 6
                else:
                    depth = 4
                grid = [row[:] for row in self.matrix]
                self.matrix, done = move(self.matrix, getBestMove(grid, depth))
                if done:
                    self.matrix = add_new(self.matrix)
                    self.update_grid_cells()
                #ZAMENA ZA MAINLOOP
                self.update()
            self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/GRID_LEN, height=SIZE/GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

        self.statusbar = Label(self, text="Score:"+str(self.score), relief='sunken', anchor=W)
        self.statusbar.grid(row=5, column=0, columnspan=5, sticky='we')
        for x in range(4):
            self.grid_columnconfigure(x, weight=1)
        for y in range(5):
            self.grid_rowconfigure(y, weight=1)
        


    def gen(self):
        return randint(0, GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = new_game(4)

        self.matrix=add_two(self.matrix)
        self.matrix=add_two(self.matrix)

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number], fg=CELL_COLOR_DICT[new_number])
        self.update_idletasks()
        
    def key_down(self, event):
        if event.keysym == 'Escape':
            quit()
        key = repr(event.keysym)
        self.score=self.score + 2 # TEST LINIJA
        self.statusbar['text'] = "Score:"+str(self.score) # I OVA, TREBA POSLE DOLE DA SE PREBACI KAD SE ODRADI SCORE
        if key in self.commands:
            self.matrix,done = self.commands[repr(event.keysym)](self.matrix)
            if done:
                self.matrix = add_new(self.matrix)
                self.update_grid_cells()
                done=False
                '''if game_state(self.matrix)=='win':
                    self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!",bg=BACKGROUND_COLOR_CELL_EMPTY)
                if game_state(self.matrix)=='lose':
                    self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!",bg=BACKGROUND_COLOR_CELL_EMPTY)'''


    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2



gamegrid = GameGrid("manual")