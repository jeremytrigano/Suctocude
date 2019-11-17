import numpy as np
from tkinter import *
import tkinter.font as tkFont
import samples as sa


class Suctocude(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent)

        self.r, self.c = 0, 0

        self.initGrid(sa.grid)

    def initGrid(self, pgrid):

        self.t = 60
        self.marge = 10
        helv36 = tkFont.Font(family='Helvetica', size=36, weight='bold')

        self.can = Canvas(self.parent, height=560, width=560, bg='white',
                          borderwidth=0, highlightthickness=0)
        self.can.pack()
        self.can.bind("<Button-1>", self.cellClicked)

        for k in range(10):
            if k % 3 != 0:
                self.can.create_line(self.marge, k*self.t+self.marge, 9*self.t +
                                     self.marge, k*self.t+self.marge, fill="gray90")
                self.can.create_line(k*self.t+self.marge, self.marge, k*self.t +
                                     self.marge, 9*self.t+self.marge, fill="gray90")
        # double loop to draw above gray lines
        for k in range(10):
            if k % 3 == 0:
                self.can.create_line(self.marge, k*self.t+self.marge, 9*self.t +
                                     self.marge, k*self.t+self.marge, fill="black")
                self.can.create_line(k*self.t+self.marge, self. marge, k*self.t +
                                     self.marge, 9*self.t+self.marge, fill="black")
        for l in range(9):
            for c in range(9):
                if pgrid[l][c][0] == 0:
                    txt = ""
                else:
                    txt = pgrid[l][c][0]
                self.can.create_text(c*self.t+2*self.t/3, l*self.t+2*self.t/3, anchor="center",
                                     text=txt, font=helv36)

    def cellClicked(self, event):
        x, y = event.x, event.y
        x1, x2, y1, y2 = -1, -1, -1, -1
        for k in range(9):
            if k*self.t+self.marge+1 < x < (k+1)*self.t+self.marge-1:
                x1 = k*self.t+self.marge+1
                x2 = (k+1)*self.t+self.marge-1
            if k*self.t+self.marge+1 < y < (k+1)*self.t+self.marge-1:
                y1 = k*self.t+self.marge+1
                y2 = (k+1)*self.t+self.marge-1
        self.can.create_line(x1, y1, x1, y2, fill="blue")
        self.can.create_line(x1, y2, x2, y2, fill="blue")
        self.can.create_line(x2, y2, x2, y1, fill="blue")
        self.can.create_line(x2, y1, x1, y1, fill="blue")

    def checker(self, pgrid):
        # check shape and one number per cell
        if pgrid.shape != (9, 9, 1):
            return False
        # check 0 presence
        for l in range(9):
            for c in range(9):
                if pgrid[l][c][0] == 0:
                    return False
        # check lines
        listNum = []
        for l in range(9):
            listNum = []
            for c in range(9):
                if pgrid[l][c][0] in listNum:
                    return False
                else:
                    listNum.append(pgrid[l][c][0])
        # check columns
        listNum = []
        for c in range(9):
            listNum = []
            for l in range(9):
                if pgrid[l][c][0] in listNum:
                    return False
                else:
                    listNum.append(pgrid[l][c][0])
        # check squares
        for linesquare in range(3):
            for rowsquare in range(3):
                listNum = []
                for l in range(3):
                    for c in range(3):
                        if pgrid[l+3*linesquare][c+3*linesquare][0] in listNum:
                            return False
                        else:
                            listNum.append(pgrid[l+3*linesquare]
                                           [c+3*linesquare][0])
        return True


if __name__ == '__main__':
    window = Tk()
    Suctocude(window)
    window.mainloop()
