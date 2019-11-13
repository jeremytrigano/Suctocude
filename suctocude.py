import numpy as np
from tkinter import *
import tkinter.font as tkFont
import samples as sa


def init_grid(pgrid):
    window = Tk()

    t = 60
    marge = 10
    helv36 = tkFont.Font(family='Helvetica', size=36, weight='bold')

    can = Canvas(window, height=560, width=560, bg='white',
                 borderwidth=0, highlightthickness=0)
    can.pack()

    for k in range(10):
        if k % 3 == 0:
            can.create_line(marge, k*t+marge, 9*t+marge, k*t+marge, width="5")
            can.create_line(k*t+marge, marge, k*t+marge, 9*t+marge, width="5")
        else:
            can.create_line(marge, k*t+marge, 9*t+marge, k*t+marge)
            can.create_line(k*t+marge, marge, k*t+marge, 9*t+marge)

    for l in range(9):
        for c in range(9):
            if pgrid[l][c][0] == 0:
                txt = ""
            else:
                txt = pgrid[l][c][0]
            can.create_text(c*t+2*t/3, l*t+2*t/3, anchor="center",
                            text=txt, font=helv36)
    window.mainloop()


def checker(pgrid):
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


init_grid(sa.grid)
