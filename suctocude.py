from tkinter import *
import tkinter.font as tkFont
import samples as sa
import copy
from random import *


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

        self.gridCurr = sa.gridEmpty
        self.cbmParentState = False
        self.cbmPopUpState = False

        listGrid = ('Easy', 'Medium', 'Hard')
        defaultVal = StringVar()
        defaultVal.set('Choose difficulty')
        omSelect = OptionMenu(self.parent, defaultVal,
                              *listGrid, command=self.gridSelect)
        omSelect.config(width=15)
        omSelect.grid(row=0, column=0)
        btnCheck = Button(self.parent, text="Check",
                          command=self.checkerResponse)
        btnCheck.grid(row=0, column=1)
        btnSolve = Button(self.parent, text="Solve", command=self.solverMsg)
        btnSolve.grid(row=0, column=2)
        btnReset = Button(self.parent, text="Reset", command=self.reset)
        btnReset.grid(row=0, column=3)
        self.cbMultiParent = Checkbutton(self.parent, text="Multi",
                                         command=self.checkMultiParent)
        self.cbMultiParent.grid(row=0, column=4)

        self.fixStartingNumbers()
        self.initGrid()

        x = int(self.parent.winfo_screenwidth()/2 - self.canW/2)
        y = int(self.parent.winfo_screenheight()/2 - self.canH/2)

        self.parent.geometry(f"+{x}+{y}")

    def gridSelect(self, value):
        self.gridCurr = sa.gridEmpty
        self.reset()
        self.generateLvl(value)
        self.fixStartingNumbers()
        self.initGrid()

    def generateLvl(self, level):
        self.generate()
        if level == 'Easy':
            occurMin = 40
            occurMax = 49
        elif level == 'Medium':
            occurMin = 50
            occurMax = 59
        elif level == 'Hard':
            occurMin = 60
            occurMax = 79
        else:
            occurMin = 1
            occurMax = 0
            self.gridCurr = sa.gridEmpty
        i = 0
        occur = 0
        while occur <= occurMin and i < 81:
            gridLeveled = copy.deepcopy(self.gridCurr)
            listNumbered = []
            for row in range(len(gridLeveled)):
                for col in range(len(gridLeveled[row])):
                    if gridLeveled[row][col] != [0]:
                        listNumbered.append((row, col))
            choiced = choice(listNumbered)
            gridLeveled[choiced[0]][choiced[1]] = [0]
            tupleSolver = self.solver(gridLeveled)
            gridSolved = tupleSolver[0]
            occur = tupleSolver[1]
            if self.checker(gridSolved) and occur <= occurMax:
                self.gridCurr = copy.deepcopy(gridLeveled)
            i += 1

    def fixStartingNumbers(self):
        for row in range(len(self.gridCurr)):
            for col in range(len(self.gridCurr[row])):
                if len(self.gridCurr[row][col]) == 1 and self.gridCurr[row][col][0] != 0 and self.gridCurr[row][col][0] < 90:
                    self.gridCurr[row][col][0] = self.gridCurr[row][col][0]+90

    def initGrid(self):
        self.can = Canvas(self.parent, height=self.canH, width=self.canW, bg='white',
                          borderwidth=0, highlightthickness=0)
        self.can.grid(row=1, column=0, columnspan=5)
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

    def clearTopLevel(self):
        for w in self.parent.winfo_children():
            if isinstance(w, Toplevel):
                w.destroy()

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
        self.clearTopLevel()
        self.popup = Toplevel(self.parent, cursor="hand2")
        self.popup.wm_attributes('-alpha', 0.9)
        self.popup.resizable(0, 0)
        self.popup.overrideredirect(True)
        # set popup "5" position on cursor position
        self.popup.geometry(
            f'+{self.parent.winfo_x()+x-20}+{self.parent.winfo_y()+y-10}')
        for i in range(1, 10):
            if i in self.gridCurr[yk][xk]:
                btnNumber = Button(
                    self.popup, text=i, relief=SUNKEN,
                    command=lambda t=i: self.cellFill(xk, yk, t, x, y))
            else:
                btnNumber = Button(
                    self.popup, text=i,
                    command=lambda t=i: self.cellFill(xk, yk, t, x, y))
            btnNumber.grid(row=(i-1) // 3, column=(i-1) % 3)
        self.cbMultiPopUp = Checkbutton(self.popup, text="M",
                                        command=self.checkMultiPopUp)
        if self.cbmParentState:
            self.cbMultiPopUp.select()
        else:
            self.cbMultiPopUp.deselect()
        self.cbMultiPopUp.grid(row=3, column=0, columnspan=2)
        btnTick = Button(self.popup, text="✓", command=self.popup.destroy)
        btnTick.grid(row=3, column=2)

    def cellFill(self, cellCol, cellRow, num, x, y):
        self.gridCurr[cellRow][cellCol] = [
            value for value in self.gridCurr[cellRow][cellCol] if value != 0]
        if num in self.gridCurr[cellRow][cellCol]:
            self.gridCurr[cellRow][cellCol] = [
                value for value in self.gridCurr[cellRow][cellCol] if value != num]
            if len(self.gridCurr[cellRow][cellCol]) == 0:
                self.gridCurr[cellRow][cellCol].append(0)
        else:
            self.gridCurr[cellRow][cellCol].append(num)
        self.can.destroy()
        if self.cbmPopUpState or self.cbmParentState:
            self.popup.destroy()
            self.initPopUp(x, y, cellCol, cellRow)
        else:
            self.popup.destroy()
        self.initGrid()

    def checkMultiParent(self):
        self.cbmParentState = not self.cbmParentState
        self.cbmPopUpState = self.cbmParentState
        if self.cbmParentState:
            self.cbMultiParent.select()
        else:
            self.cbMultiParent.deselect()

    def checkMultiPopUp(self):
        self.cbmPopUpState = not self.cbmPopUpState
        self.cbmParentState = self.cbmPopUpState
        if self.cbmPopUpState:
            self.cbMultiPopUp.select()
            self.cbMultiParent.select()
        else:
            self.cbMultiPopUp.deselect()
            self.cbMultiParent.deselect()

    def checker(self, *args):
        if len(args) > 0:
            gridToCheck = args[0]
        else:
            gridToCheck = copy.deepcopy(self.gridCurr)
        if not isinstance(gridToCheck, list):
            self.gridCurr = sa.gridEmpty
            return False
        # check shape and one number per cell
        if len(gridToCheck) != 9:
            return False
        for row in range(len(gridToCheck)):
            if len(gridToCheck[row]) != 9:
                return False
        for row in range(len(gridToCheck)):
            for col in range(len(gridToCheck[row])):
                if len(gridToCheck[row][col]) != 1:
                    return False
        # check 0 presence
        for row in range(len(gridToCheck)):
            for col in range(len(gridToCheck[row])):
                if gridToCheck[row][col][0] == 0:
                    return False
                if len(gridToCheck[row][col]) > 1:
                    return False
        # reset to -90 fixed numbers
        for row in range(len(gridToCheck)):
            for col in range(len(gridToCheck[row])):
                if gridToCheck[row][col][0] > 90:
                    gridToCheck[row][col][0] = gridToCheck[row][col][0] - 90
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

    def checkerResponse(self):
        if self.checker():
            title = "Correct !"
            txt1 = "Félicitations !"
            txt2 = "Grille terminée"
        else:
            title = "Faux !"
            txt1 = "Désolé,"
            txt2 = "votre grille n'est pas valide"
        self.clearTopLevel()
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

        self.popup.geometry(f"+{x}+{y}")

    def reset(self):
        for row in range(len(self.gridCurr)):
            for col in range(len(self.gridCurr[row])):
                if self.gridCurr[row][col][0] < 90:
                    self.gridCurr[row][col] = [0]
        self.initGrid()

    def impossPossNum(self, row, col, grid):
        listImpossibleNum = []
        for colF in range(len(grid[row])):
            if len(grid[row][colF]) == 1 and grid[row][colF][0] != 0 and colF != col:
                if grid[row][colF][0] > 90:
                    listImpossibleNum.append(
                        grid[row][colF][0]-90)
                else:
                    listImpossibleNum.append(grid[row][colF][0])
        for rowF in range(len(grid)):
            if len(grid[rowF][col]) == 1 and grid[rowF][col][0] != 0 and rowF != row:
                if grid[rowF][col][0] > 90:
                    listImpossibleNum.append(
                        grid[rowF][col][0]-90)
                else:
                    listImpossibleNum.append(grid[rowF][col][0])
        rowStartSqr = row // 3 * 3
        colStartSqr = col // 3 * 3
        for rowF in range(rowStartSqr, rowStartSqr+3):
            for colF in range(colStartSqr, colStartSqr+3):
                if len(grid[rowF][colF]) == 1 and grid[rowF][colF][0] != 0 and (rowF, colF) != (row, col):
                    if grid[rowF][colF][0] > 90:
                        listImpossibleNum.append(
                            grid[rowF][colF][0]-90)
                    else:
                        listImpossibleNum.append(
                            grid[rowF][colF][0])
        listImpossibleNum = list(dict.fromkeys(listImpossibleNum))
        listPossibleNum = []
        for j in range(1, 10):
            if j not in listImpossibleNum:
                listPossibleNum.append(j)
        return listImpossibleNum, listPossibleNum

    def solver(self, grid):
        gridToSolve = copy.deepcopy(grid)
        flagChanges = 1
        loopcounter = 0
        while flagChanges != 0:
            flagChanges = 0
            for row in range(len(gridToSolve)):
                for col in range(len(gridToSolve[row])):
                    if len(gridToSolve[row][col]) > 1 or gridToSolve[row][col][0] == 0:
                        gridToSolve[row][col] = self.impossPossNum(row, col, gridToSolve)[
                            1]
                        if len(gridToSolve[row][col]) == 1:
                            flagChanges = 1
                            loopcounter += 1
                        if len(gridToSolve[row][col]) == 0:
                            gridToSolve[row][col].append(0)
            # if no number find, for every cell check if a possible value is
            # alone on its row, cell, square
            if flagChanges == 0:
                for row in range(len(gridToSolve)):
                    for col in range(len(gridToSolve[row])):
                        if len(gridToSolve[row][col]) > 1:
                            listTmp = []
                            for colF in range(len(gridToSolve[row])):
                                if colF != col:
                                    if gridToSolve[row][colF][0] != 0:
                                        if gridToSolve[row][colF][0] > 90:
                                            listTmp.append(
                                                gridToSolve[row][colF][0]-90)
                                        else:
                                            if len(gridToSolve[row][colF]) == 1:
                                                listTmp.append(
                                                    gridToSolve[row][colF][0])
                                            else:
                                                listTmp.extend(
                                                    gridToSolve[row][colF])
                            listTmp = list(dict.fromkeys(listTmp))
                            listTmp2 = [i for i in range(
                                1, 10) if i not in listTmp]
                            if len(listTmp2) == 1 and listTmp2[0] in gridToSolve[row][col]:
                                gridToSolve[row][col] = listTmp2
                                flagChanges = 1
                                loopcounter += 1
                            listTmp = []
                            for rowF in range(len(gridToSolve)):
                                if rowF != row:
                                    if gridToSolve[rowF][col][0] != 0:
                                        if gridToSolve[rowF][col][0] > 90:
                                            listTmp.append(
                                                gridToSolve[rowF][col][0]-90)
                                        else:
                                            if len(gridToSolve[rowF][col]) == 1:
                                                listTmp.append(
                                                    gridToSolve[rowF][col][0])
                                            else:
                                                listTmp.extend(
                                                    gridToSolve[rowF][col])
                            listTmp = list(dict.fromkeys(listTmp))
                            listTmp2 = [i for i in range(
                                1, 10) if i not in listTmp]
                            if len(listTmp2) == 1 and listTmp2[0] in gridToSolve[row][col]:
                                gridToSolve[row][col] = listTmp2
                                flagChanges = 1
                                loopcounter += 1
                            listTmp = []
                            rowStartSqr = row // 3 * 3
                            colStartSqr = col // 3 * 3
                            for rowF in range(rowStartSqr, rowStartSqr+3):
                                for colF in range(colStartSqr, colStartSqr+3):
                                    if (rowF, colF) != (row, col):
                                        if gridToSolve[rowF][colF][0] != 0:
                                            if gridToSolve[rowF][colF][0] > 90:
                                                listTmp.append(
                                                    gridToSolve[rowF][colF][0]-90)
                                            else:
                                                if len(gridToSolve[rowF][colF]) == 1:
                                                    listTmp.append(
                                                        gridToSolve[rowF][colF][0])
                                                else:
                                                    listTmp.extend(
                                                        gridToSolve[rowF][colF])
                            listTmp = list(dict.fromkeys(listTmp))
                            listTmp2 = [i for i in range(
                                1, 10) if i not in listTmp]
                            if len(listTmp2) == 1 and listTmp2[0] in gridToSolve[row][col]:
                                gridToSolve[row][col] = listTmp2
                                flagChanges = 1
                                loopcounter += 1
        return gridToSolve, loopcounter

    def solverMsg(self):
        tupleSolver = self.solver(self.gridCurr)
        self.gridCurr = tupleSolver[0]
        self.initGrid()
        title = "Résolution..."
        if self.checker():
            txt = "Résolution terminé !"
        else:
            txt = "Résolution impossible pour le moment..."
        self.clearTopLevel()
        self.popup = Toplevel(self.parent)
        self.popup.title(title)
        self.popup.resizable(0, 0)

        lMsg = Label(self.popup, text=txt, font=self.helv18, bd=10)
        lMsg.grid(row=0, column=0)
        btnOK = Button(self.popup, text="OK", command=self.popup.destroy)
        btnOK.grid(row=1, column=0)

        self.popup.update()
        x = int(self.parent.winfo_x() + self.canW //
                2 - self.popup.winfo_width()//2)
        y = int(self.parent.winfo_y() + self.canH //
                2 - self.popup.winfo_height()//2)

        self.popup.geometry(f"+{x}+{y}")

    def generator(self):
        maxloop = 0
        gridToCreate = copy.deepcopy(sa.gridEmpty)
        while maxloop < 100:
            flagDoublePoss = 0
            for row in range(len(gridToCreate)):
                for col in range(len(gridToCreate[row])):
                    if len(gridToCreate[row][col]) == 2 and flagDoublePoss == 0:
                        gridToCreate[row][col] = [
                            choice(gridToCreate[row][col])]
                        flagDoublePoss = 1
            if flagDoublePoss != 1:
                row = randint(0, 8)
                col = randint(0, 8)
                if len(gridToCreate[row][col]) > 1:
                    listPossibleNum = self.impossPossNum(
                        row, col, gridToCreate)[1]
                    if len(listPossibleNum) > 0:
                        num = choice(listPossibleNum)
                        gridToCreate[row][col] = [num]
            gridToCreate = self.solver(gridToCreate)[0]
            zeroCell = 0
            for row in range(len(gridToCreate)):
                for col in range(len(gridToCreate[row])):
                    if len(gridToCreate[row][col]) == 1 and gridToCreate[row][col][0] == 0:
                        zeroCell += 1
            if zeroCell == 0:
                self.gridCurr = gridToCreate
            else:
                gridToCreate = copy.deepcopy(self.gridCurr)
            maxloop += 1
            if self.checker(gridToCreate):
                return gridToCreate
        if maxloop == 100:
            return sa.gridEmpty

    def generate(self):
        ntry = 0
        while ntry < 10:
            self.gridCurr = self.generator()
            if self.checker():
                break
            ntry += 1
        if ntry == 10:
            self.gridCurr = sa.gridEmpty


if __name__ == '__main__':
    window = Tk()
    Suctocude(window)
    window.mainloop()
