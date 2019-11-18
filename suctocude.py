import numpy as np
from tkinter import *
import tkinter.font as tkFont
import samples as sa


class Suctocude(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent)

        self.blueSquare = None
        self.t = 60
        self.marge = 10
        self.ink36 = tkFont.Font(family='Ink Free', size=36)
        self.helv36b = tkFont.Font(family='Helvetica', size=36, weight='bold')

        self.gridCurr = sa.gridOneLeft

        # adding 90 to fixed numbers
        for i in range(len(self.gridCurr)):
            for j in range(len(self.gridCurr[i])):
                if self.gridCurr[i, j] != 0:
                    self.gridCurr[i, j] = self.gridCurr[i, j]+90

        btnCheck = Button(self.parent, text="Check",
                          command=lambda grid=self.gridCurr: self.checkerResponse(grid))
        btnCheck.pack()

        self.initGrid(self.gridCurr)

    def initGrid(self, pgrid):
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
        # todo : fix font on 2nd modif
        for l in range(9):
            for c in range(9):
                if pgrid[l][c][0] > 90:
                    txt = pgrid[l][c][0]-90
                    self.can.create_text(c*self.t+2*self.t/3, l*self.t+2*self.t/3, anchor="center",
                                         text=txt, font=self.helv36b)
                else:
                    if pgrid[l][c][0] == 0:
                        txt = ""
                    else:
                        txt = pgrid[l][c][0]
                    self.can.create_text(c*self.t+2*self.t/3, l*self.t+2*self.t/3, anchor="center",
                                         text=txt, font=self.ink36)

    def cellClicked(self, event):
        x, y = event.x, event.y
        xk, yk, x1, x2, y1, y2 = -1, -1, -1, -1, -1, -1
        self.can.delete("blueSquare")
        for w in self.parent.winfo_children():
            if isinstance(w, Toplevel):
                w.destroy()
        for k in range(9):
            if k*self.t+self.marge+1 < x < (k+1)*self.t+self.marge-1:
                xk = k
                x1 = k*self.t+self.marge+2
                x2 = (k+1)*self.t+self.marge-2
            if k*self.t+self.marge+1 < y < (k+1)*self.t+self.marge-1:
                yk = k
                y1 = k*self.t+self.marge+2
                y2 = (k+1)*self.t+self.marge-2
        if xk != -1 and yk != -1:
            self.blueSquare = self.can.create_rectangle(
                x1, y1, x2, y2, outline="blue", tags="blueSquare")
            self.popup = Toplevel(self.parent, cursor="hand2")
            self.popup.resizable(0, 0)
            self.popup.overrideredirect(True)
            # set popup "5" position on cursor position
            self.popup.geometry(
                f'+{self.parent.winfo_x()+x-20}+{self.parent.winfo_y()+y-10}')
            for i in range(1, 10):
                btnNumber = Button(
                    self.popup, text=i, command=lambda t=i: self.cellFill(xk, yk, t))
                btnNumber.grid(row=(i-1) // 3, column=(i-1) % 3)
            btnM = Button(self.popup, text="M")
            btnM.grid(row=3, column=0)
            btnX = Button(self.popup, text="X", command=self.popup.destroy)
            btnX.grid(row=3, column=2)

    def cellFill(self, cellCol, cellRow, num):
        self.gridCurr[cellRow, cellCol] = num
        self.can.destroy()
        self.popup.destroy()
        self.initGrid(self.gridCurr)

    def checker(self, pgrid):
        # reset to -90 fixed numbers
        for i in range(len(self.gridCurr)):
            for j in range(len(self.gridCurr[i])):
                if self.gridCurr[i, j] > 90:
                    self.gridCurr[i, j] = self.gridCurr[i, j]-90
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

    def checkerResponse(self, pgrid):
        if self.checker(pgrid):
            print('ok')
        else:
            print('ko')


if __name__ == '__main__':
    window = Tk()
    Suctocude(window)
    window.mainloop()
