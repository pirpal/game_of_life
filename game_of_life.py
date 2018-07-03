#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk


class GameOfLife(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.geometry("800x600+100+100")
        self.title("Conway's Game Of Life")
        self.size = 80
        self.cell_sz = 5
        self.colors = {0: "#1f2433", 1: "#2ab922"}
        self.grid = [[0 for i in range(self.size)] for i in range(self.size)]
        self.generation_nb = tk.IntVar(0)
        self.initUi()
        self.cells = self.initCells()
        self.animation_on = False
        self.can.bind("<Button-1>", self.click)
        self.can.bind("<Motion>", self.move)
        self.can.bind("<Leave>", self.can.delete("preview"))
        self.bind("<space>", self.toggleAnimation_space)

    def initUi(self):
        # Canvas
        self.can_fr = tk.Frame(self, height=400)
        self.can_fr.grid(row=0, column=0)

        self.can = tk.Canvas(
            self.can_fr, width=400, height=400, bg=self.colors[0])
        self.can.grid()

        # Generation number display
        self.data_fr = tk.Frame(self, height=100, padx=20, pady=20)
        self.data_fr.grid(row=1, column=0)

        self.generation_nb_ent = tk.Entry(
            self.data_fr,
            textvariable=self.generation_nb,
            width=6,
            state=tk.DISABLED,
            bg="white")
        self.generation_nb_ent.grid(row=0, column=0)

        # Commands : play/pause, step, clear
        self.cmd_fr = tk.Frame(self, height=100)
        self.cmd_fr.grid(row=2, column=0)

        self.bt_clear = tk.Button(
            self.cmd_fr, text="Clear", command=self.clear)
        self.bt_clear.grid(row=0, column=0)

        self.bt_play = tk.Button(
            self.cmd_fr, text="Play", command=self.toggleAnimation_button)
        self.bt_play.grid(row=0, column=1)

        self.bt_step = tk.Button(self.cmd_fr, text="Step +1", command=self.step)
        self.bt_step.grid(row=0, column=2)

    def initCells(self):
        cells = []
        for x in range(self.size):
            line = []
            for y in range(self.size):
                line.append(
                    self.can.create_rectangle(
                        y * self.cell_sz,
                        x * self.cell_sz,
                        y * self.cell_sz + self.cell_sz,
                        x * self.cell_sz + self.cell_sz,
                        fill=self.colors[self.grid[x][y]]
                    )
                )
            cells.append(line)
        return cells

    def click(self, evt):
        x, y = evt.y // self.cell_sz, evt.x // self.cell_sz
        self.grid[x][y] = {0: 1, 1: 0}[self.grid[x][y]]
        self.can.itemconfigure(
            self.cells[x][y], fill=self.colors[self.grid[x][y]])

    def move(self, evt):
        x, y = evt.y // self.cell_sz, evt.x // self.cell_sz
        self.can.delete("preview")
        self.can.create_rectangle(
            y * self.cell_sz,
            x * self.cell_sz,
            y * self.cell_sz + self.cell_sz,
            x * self.cell_sz + self.cell_sz,
            fill="white",
            tag="preview"
        )

    def clear(self):
        self.animation_on = False
        self.bt_play.configure(text=">")
        self.grid = [[0 for i in range(self.size)] for i in range(self.size)]
        self.generation_nb.set(0)
        for x in range(self.size):
            for y in range(self.size):
                self.can.itemconfigure(self.cells[x][y], fill=self.colors[0])

    def copyGrid(self, grid):
        new_grid = []
        for x in range(len(grid)):
            line = []
            for y in range(len(grid[x])):
                line.append(grid[x][y])
            new_grid.append(line)
        return new_grid

    def inBoundaries(self, x, y):
        return x in range(self.size) and y in range(self.size)

    def countNeighbrs(self, grid, x, y):
        count = 0
        for n in [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]:
            if self.inBoundaries(x + n[0], y + n[1]):
                if grid[x + n[0]][y + n[1]] == 1:
                    count += 1
        return count

    def toggleAnimation_space(self, evt):
        self.animation_on = not self.animation_on
        if self.animation_on:
            self.animate()
            self.bt_play.configure(text="||")
        else:
            self.bt_play.configure(text=">")

    def toggleAnimation_button(self):
        self.animation_on = not self.animation_on
        if self.animation_on:
            self.animate()
            self.bt_play.configure(text="||")
        else:
            self.bt_play.configure(text=">")

    def animate(self):
        if self.animation_on:
            self.can.delete("preview")
            new_grid = self.copyGrid(self.grid)
            for x in range(self.size):
                for y in range(self.size):
                    neighbrs = self.countNeighbrs(self.grid, x, y)
                    if self.grid[x][y] == 0 and neighbrs == 3:
                        new_grid[x][y] = 1
                        self.can.itemconfigure(
                            self.cells[x][y], fill=self.colors[1])
                    elif self.grid[x][y] == 1 and neighbrs not in range(2, 4):
                        new_grid[x][y] = 0
                        self.can.itemconfigure(
                            self.cells[x][y], fill=self.colors[0])
            self.grid = self.copyGrid(new_grid)
            self.generation_nb.set(self.generation_nb.get() + 1)
            self.after(50, self.animate)

    def step(self):
        self.animation_on = False
        self.can.delete("preview")
        new_grid = self.copyGrid(self.grid)
        for x in range(self.size):
            for y in range(self.size):
                neighbrs = self.countNeighbrs(self.grid, x, y)
                if self.grid[x][y] == 0:
                    if neighbrs == 3:
                        new_grid[x][y] = 1
                        self.can.itemconfigure(
                            self.cells[x][y], fill=self.colors[1])
                else:
                    if neighbrs not in range(2, 4):
                        new_grid[x][y] = 0
                        self.can.itemconfigure(
                            self.cells[x][y], fill=self.colors[0]
                        )
        self.grid = self.copyGrid(new_grid)
        self.generation_nb.set(self.generation_nb.get() + 1)

    def debug(self, evt):
        x, y = evt.y // self.cell_sz, evt.x // self.cell_sz
        print(self.countNeighbrs(x, y))


if __name__ == "__main__":
    app = GameOfLife(None)
    app.mainloop()
