# SmileyClassAnimationDemo.py
# version 0.5

from Tkinter import *
from basicAnimationClass import BasicAnimationClass
import random


class PlayTetris(BasicAnimationClass):



    def createBoard(self):
#this helperfunction intakes canvas and creates our board
#filled with the original color, light salmon
        rows = self.rows
        cols = self.cols
        originalColor = self.emptyColor
        board = []
        for row in xrange(rows):
            board += [[originalColor]*cols]
        return board


    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.emptyColor = "midnight blue"
        self.margin = 25
        self.cellSize = 25
        self.canvasWidth = 2*self.margin + self.cols*self.cellSize
        self.canvasHeight = 2*self.margin + self.rows*self.cellSize
        super(PlayTetris, self).__init__(self.canvasWidth, self.canvasHeight)
        self.gameOver = False
        self.score=0


    def initAnimation(self):
        self.emptyColor = "midnight blue"
        self.board = self.createBoard()

        self.iPiece = [[False,False,False,False],
                        [True, True, True, True],
                        [False,False,False,False]]
        self.jPiece = [[True, False, False], [True, True, True]]
        self.lPiece = [[False, False, True], [True, True, True]]
        self.oPiece = [[True, True], [True, True]]
        self.sPiece = [[False, True, True], [True, True, False]]
        self.tPiece = [[False, True, False], [True, True, True]]
        self.zPiece = [[True, True, False], [False, True, True]]
        self.tetrisPieces = [self.iPiece,self.jPiece,self.lPiece,
                             self.oPiece,self.sPiece,self.tPiece,
                             self.zPiece]
        self.tetrisPieceColors = ["light salmon", "magenta", "chartreuse",
                                    "gold", "firebrick1", "aquamarine",
                                    "PaleVioletRed1","SpringGreen2", 
                                    "deep pink", "MediumPurple1", "turquoise1",
                                    "DeepSkyBlue2", "cyan2"]
        self.fallingPiece = random.choice(self.tetrisPieces)
        self.fallingPieceColor = random.choice(self.tetrisPieceColors)
        self.newFallingPiece()
        self.firstTime = True
        self.app.setTimerDelay(300)


   
    def drawCell(self, row, col, color):
#this intakes the current row and col, and draws a cell
        startX = self.margin + (col * self.cellSize)
        endX = startX + self.cellSize
        startY = self.margin + (row * self.cellSize)
        endY = startY + self.cellSize
        outlineWidth = 3
        self.canvas.create_rectangle(startX, startY, endX, endY, fill = color,
        outline = "black", width = outlineWidth) 

    def drawBoard(self):
#this function calls drawCell after iterating after all the possible positions
#in the board
        rows = self.rows
        cols = self.cols
        for row in xrange(rows):
            for col in xrange(cols):
                color = self.board[row][col]
                self.drawCell(row, col, color)
    


    def drawFallingPiece(self):

        for row in xrange(len(self.fallingPiece)):
            for col in xrange(len(self.fallingPiece[0])):
     
                if self.fallingPiece[row][col]:

                    rowCellPosition = row + self.fallingPieceRow
                    colCellPosition = col + self.fallingPieceCol
                    self.drawCell(rowCellPosition, colCellPosition, 
                                        self.fallingPieceColor)
                else: pass


    def drawGame(self):
#this makes the background by filling the canvas with "SteelBlue1", then calls
#drawBoard to make the tetrisBoard.
        width = self.canvas.app.width
        height = self.canvas.app.height
        backgroundColor = "snow"
        self.canvas.create_rectangle(0,0,width,height,fill=backgroundColor, outline = "black")
        self.drawBoard()
        self.drawFallingPiece()


    def newFallingPiece(self):
    #this function randomly chooses a new piece, randomly selects a color, and
    #positions it in the middle of the top row
        self.fallingPiece = random.choice(self.tetrisPieces)
        self.fallingPieceColor = random.choice(self.tetrisPieceColors)
        centerColumn = self.cols / 2
        halfWidthOfPiece = len(self.fallingPiece[0])/2
        self.fallingPieceRow = 0 #we want the piece to start at the top
        self.fallingPieceCol = centerColumn - halfWidthOfPiece
        #this places the piece in the middle by subtracting half of the piece's
        #width from the horizontal center.

    def onTheBoard(self, rowCellPosition, colCellPosition):
        if rowCellPosition >= 0 and rowCellPosition < self.rows:
            if colCellPosition >=0 and colCellPosition < self.cols:
                return True
        return False

    def colorAtLocation(self, rowCellPosition, colCellPosition):
    #this function returns true if the color at given cell is equal to
    #empty color.Otherwise it returns false
        if self.board[rowCellPosition][colCellPosition] == self.emptyColor:
            return True
        return False

    def fallingPieceIsLegal(self):
        for row in xrange(len(self.fallingPiece)):
            for col in xrange(len(self.fallingPiece[0])):
                if self.fallingPiece[row][col]:
                    rowCellPosition = row+self.fallingPieceRow 
                    colCellPosition = col+self.fallingPieceCol
                    #check if its is on theboard and that the 
                    #color at that location on theboard is the empty color
                    if not(self.onTheBoard(rowCellPosition, colCellPosition)):
                            return False
                    if not(self.colorAtLocation(rowCellPosition, 
                        colCellPosition)):
                        return False
        return True

    def moveFallingPiece(self, drow, dcol):
        self.fallingPieceRow += drow
        self.fallingPieceCol += dcol
        if not(self.fallingPieceIsLegal()):
            self.fallingPieceRow -= drow
            self.fallingPieceCol -= dcol
            return False
        return True


    def placeFallingPiece(self):
        for row in xrange(len(self.fallingPiece)):
            for col in xrange(len(self.fallingPiece[0])):
                if self.fallingPiece[row][col]:
                    rowPosition = row + self.fallingPieceRow
                    colPosition = col + self.fallingPieceCol
                    self.board[rowPosition][colPosition]=self.fallingPieceColor
                    self.removeFullRows()

    def onKeyPressed(self,event):
        if event.keysym == "Up":
            self.rotateFallingPiece()
        elif event.keysym == "Down":
            self.moveFallingPiece(1, 0)
        elif event.keysym == "Right":
            self.moveFallingPiece(0, 1)
        elif event.keysym == "Left":
            self.moveFallingPiece(0, -1)
        elif event.char == "r":
            self.initAnimation()
            self.gameOver = False


    


    def fallingPieceCenter(self):
        row = len(self.fallingPiece)
        col = len(self.fallingPiece[0])
        center = ((row)/2, (col)/2)
        return center


    def rotateFallingPiece(self):
        rotatedList = []
        oldSelfFallingPiece = self.fallingPiece
        for row in xrange(len(self.fallingPiece[0])):
            rotatedList += [[False]* len(self.fallingPiece)]
        cRow, cCol = self.fallingPieceCenter()
        for col in xrange(len(self.fallingPiece[0])):
            for row in xrange(len(self.fallingPiece)):
                value = self.fallingPiece[row][col]
                newCol = row
                newRow = len(self.fallingPiece[0]) -1 - col
                rotatedList[newRow][newCol] = value

        self.fallingPiece = rotatedList
        if self.fallingPieceIsLegal() == False:
            self.fallingPiece = oldSelfFallingPiece
            #this brings the fallingpiece back to its former state,
            #essentially undoing the rotation

    def removeFullRows(self):
        emptyRow = [self.emptyColor] * self.cols
        for row in xrange(len(self.board)):
            if self.emptyColor not in self.board[row]:
                self.board.pop(row)
                self.score+= self.cols 
                #your score is how many ever cell you popped :D

                self.board = [emptyRow] + self.board


    def onTimerFired(self):
        if self.firstTime:
            self.firstTime = False
    
        elif not self.gameOver:

            if self.moveFallingPiece(1, 0) == False:
                self.placeFallingPiece()
                self.newFallingPiece()
                if self.fallingPieceIsLegal() == False:
                    self.gameOver =True


    def drawGameOverScreen(self):
        cx = self.canvasWidth/2.0
        cy = self.canvasHeight/2.0
        self.canvas.create_text(cx, 
            cy, text = "GAMEOVER", font = "Arial 40", fill = "white")
       
    def drawScore(self):
        cx = self.canvasWidth/2.0
        cy = self.margin / 2.0
        self.canvas.create_text(cx, cy, text = '''press r to restart! ...score: %d'''%self.score, 
            fill = "black", font = "Arial 12")
        textCx = self.canvasWidth/2.0
        textCy = self.canvasHeight - self.margin / 2.0
        (self.canvas.create_text(textCx, textCy, 
            text = "it's unique, it's quirky... It's the New Tetris."))
    def redrawAll(self):
        canvas = self.canvas
        canvas.delete(ALL)
        if self.gameOver == False:
            self.drawGame()
            self.drawScore()
        else:
            self.drawGame()
            self.drawScore()
            self.drawGameOverScreen()

PlayTetris(20, 15).run()
