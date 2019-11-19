import numpy as np
from tkinter import *
import tkinter.font as tkFont
import samples as sa


class Suctocude(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent)

        self.parent.title("Suctocude")
        self.blueSquare = None
        self.canH = 560
        self.canW = 560
        self.t = 60
        self.marge = 10
        self.ink36 = tkFont.Font(family='Ink Free', size=36)
        self.ink10 = tkFont.Font(family='Ink Free', size=10)
        self.helv36b = tkFont.Font(family='Helvetica', size=36, weight='bold')
        self.helv18 = tkFont.Font(family='Helvetica', size=18)

        self.gridCurr = sa.gridMulti

        # adding 90 to fixed numbers
        for row in range(len(self.gridCurr)):
            for col in range(len(self.gridCurr[row])):
                if len(self.gridCurr[row][col]) == 1 and self.gridCurr[row][col][0] != 0:
                    self.gridCurr[row][col][0] = self.gridCurr[row][col][0]+90

        btnCheck = Button(self.parent, text="Check",
                          command=lambda grid=self.gridCurr: self.checkerResponse(grid))
        btnCheck.pack()

        self.initGrid()

        x = int(self.parent.winfo_screenwidth()/2 - self.canW/2)
        y = int(self.parent.winfo_screenheight()/2 - self.canH/2)

        self.parent.geometry(f"+{x}+{y}")

    def initGrid(self):
        self.can = Canvas(self.parent, height=self.canH, width=self.canW, bg='white',
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
        self.initGridFill()

    def initGridFill(self):
        for row in range(len(self.gridCurr)):
            for col in range(len(self.gridCurr[row])):
                if len(self.gridCurr[row][col]) == 1:
                    if self.gridCurr[row][col][0] > 90:
                        txt = self.gridCurr[row][col][0]-90
                        self.can.create_text(col*self.t+2*self.t/3,
                                             row*self.t+2*self.t/3,
                                             anchor="center",
                                             text=txt,
                                             font=self.helv36b)
                    else:
                        if self.gridCurr[row][col][0] == 0:
                            txt = ""
                        else:
                            txt = self.gridCurr[row][col][0]
                        self.can.create_text(col*self.t+2*self.t/3,
                                             row*self.t+2*self.t/3,
                                             anchor="center",
                                             text=txt,
                                             font=self.ink36)
                else:
                    for i in range(9):
                        if (i+1) in self.gridCurr[row][col]:
                            x = col * self.t + 20 + (self.t // 3) * (i % 3)
                            y = row * self.t + 20 + (self.t // 3) * (i // 3)
                            self.can.create_text(x, y, anchor="center",
                                                 text=(i+1), font=self.ink10)

    def cellClicked(self, event):
        x, y = event.x, event.y
        xk, yk, x1, x2, y1, y2 = -1, -1, -1, -1, -1, -1
        self.can.delete("blueSquare")
        for k in range(9):
            if k*self.t+self.marge+1 < x < (k+1)*self.t+self.marge-1:
                xk = k
                x1 = k*self.t+self.marge+2
                x2 = (k+1)*self.t+self.marge-2
            if k*self.t+self.marge+1 < y < (k+1)*self.t+self.marge-1:
                yk = k
                y1 = k*self.t+self.marge+2
                y2 = (k+1)*self.t+self.marge-2
        if self.gridCurr[yk][xk][0] < 10:
            if xk != -1 and yk != -1:
                self.blueSquare = self.can.create_rectangle(
                    x1, y1, x2, y2, outline="blue", tags="blueSquare")
            self.initPopUp(x, y, xk, yk)

    def initPopUp(self, x, y, xk, yk):
        for w in self.parent.winfo_children():
            if isinstance(w, Toplevel):
                w.destroy()
        self.popup = Toplevel(self.parent, cursor="hand2")
        self.popup.resizable(0, 0)
        self.popup.overrideredirect(True)
        # set popup "5" position on cursor position
        self.popup.geometry(
            f'+{self.parent.winfo_x()+x-20}+{self.parent.winfo_y()+y-10}')
        for i in range(1, 10):
            if self.gridCurr[yk][xk] == i:
                btnNumber = Button(
                    self.popup, text=i, relief=SUNKEN,
                    command=lambda t=i: self.cellFill(xk, yk, t))
            else:
                btnNumber = Button(
                    self.popup, text=i,
                    command=lambda t=i: self.cellFill(xk, yk, t))
            btnNumber.grid(row=(i-1) // 3, column=(i-1) % 3)
        cbMulti = Checkbutton(self.popup, text="M")
        cbMulti.grid(row=3, column=0, columnspan=2)
        btnX = Button(self.popup, text="X", command=self.popup.destroy)
        btnX.grid(row=3, column=2)

    def cellFill(self, cellCol, cellRow, num):
        self.gridCurr[cellRow][cellCol] = [
            value for value in self.gridCurr[cellRow][cellCol] if value != 0]
        if num in self.gridCurr[cellRow][cellCol]:
            self.gridCurr[cellRow][cellCol] = [
                value for value in self.gridCurr[cellRow][cellCol] if value != num]
        else:
            self.gridCurr[cellRow][cellCol].append(num)
        self.can.destroy()
        self.popup.destroy()
        self.initGrid()

    def checker(self, pgrid):
        gridToCheck = pgrid.copy()
        # reset to -90 fixed numbers
        for row in range(len(gridToCheck)):
            for col in range(len(gridToCheck[row])):
                if gridToCheck[row, col] > 90:
                    gridToCheck[row, col] = gridToCheck[row, col]-90
        # check shape and one number per cell
        if gridToCheck.shape != (9, 9, 1):
            return False
        # check 0 presence
        for row in range(len(gridToCheck)):
            for col in range(len(gridToCheck[row])):
                if gridToCheck[row][col][0] == 0:
                    return False
        # check lines
        listNum = []
        for row in range(len(gridToCheck)):
            listNum = []
            for col in range(len(gridToCheck[row])):
                if gridToCheck[row][col][0] in listNum:
                    return False
                else:
                    listNum.append(gridToCheck[row][col][0])
        # check columns
        listNum = []
        for col in range(len(gridToCheck)):
            listNum = []
            for row in range(len(gridToCheck[col])):
                if gridToCheck[row][col][0] in listNum:
                    return False
                else:
                    listNum.append(gridToCheck[row][col][0])
        # check squares
        for linesquare in range(3):
            for rowsquare in range(3):
                listNum = []
                for row in range(3):
                    for col in range(3):
                        if gridToCheck[row+3*linesquare][col+3*linesquare][0] in listNum:
                            return False
                        else:
                            listNum.append(gridToCheck[row+3*linesquare]
                                           [col+3*linesquare][0])
        return True

    def checkerResponse(self, pgrid):
        if self.checker(pgrid):
            title = "Correct !"
            txt1 = "Félicitations !"
            txt2 = "Grille terminée"
        else:
            title = "Faux !"
            txt1 = "Désolé,"
            txt2 = "votre grille n'est pas valide"
        for w in self.parent.winfo_children():
            if isinstance(w, Toplevel):
                w.destroy()
        self.popup = Toplevel(self.parent)
        self.popup.title(title)
        self.popup.resizable(0, 0)

        lMsg = Label(self.popup, text=txt1, font=self.helv18, bd=10)
        lMsg.grid(row=0, column=0)
        lMsg = Label(self.popup, text=txt2, font=self.helv18, bd=10)
        lMsg.grid(row=1, column=0)
        btnOK = Button(self.popup, text="OK", command=self.popup.destroy)
        btnOK.grid(row=2, column=0)

        self.popup.update()
        x = int(self.parent.winfo_x() + self.canW //
                2 - self.popup.winfo_width()//2)
        y = int(self.parent.winfo_y() + self.canH //
                2 - self.popup.winfo_height()//2)
        print(self.parent.winfo_x(), self.canW, self.popup.winfo_width())

        self.popup.geometry(f"+{x}+{y}")


if __name__ == '__main__':
    window = Tk()
    Suctocude(window)
    window.mainloop()
