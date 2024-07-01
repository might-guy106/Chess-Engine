"""
this is our main driver life. ir will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine, SmartMoveFinder
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 512 # 400 is another option
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8 # dimensions of a chess board are 8x8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15 # for animations later on
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''

def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bP", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR", "wP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: we can access an image by saying 'IMAGES['wP']' or 'IMAGES['bP']'

'''
The main driver for our code. This will handle user input and updating the graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages() # only do this once, before the while loop
    running = True
    prevSelection = () # no square is selected, keep track of the last click of the user (tuple: (row, col))
    gameOver = False
    # if gs.whiteToMove:
    #     print("White's Turn")
    # else:
    #     print("Black's Turn")
    moveLogFont = p.font.SysFont("comicsans", 14, False, False)
    validMoves = gs.getValidMoves()
    playerOne = False # if a human is playing white, then this will be True. If an AI is playing, then this will be False
    playerTwo = False # same as above but for black
    AIThinking = False
    moveFinderProcess = None
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    currSelection = (row, col)
                    if prevSelection == currSelection or col >= 8:
                        prevSelection = () # deselect
                    elif prevSelection == ():
                        prevSelection = currSelection
                    elif humanTurn:
                        moveMade = False
                        move = ChessEngine.Move(prevSelection, currSelection, gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i] :
                                print(move.pieceMoved)
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                prevSelection = ()
                                # if gs.whiteToMove:
                                #     print("White's Turn")
                                # else:
                                #     print("Black's Turn")
                        if moveMade:
                            animateMove(gs.moveLog[-1], screen, gs.board, clock)
                            validMoves = gs.getValidMoves()
                            # gs.printUndolog()
                            # if gs.whiteToMove:
                            #     print("White's Turn")
                            # else:
                            #     print("Black's Turn")
                        if not moveMade:
                            # print("Invalid Move")
                            prevSelection = currSelection


            elif e.type == p.KEYDOWN:
                if e.key == p.K_z and (p.key.get_mods() & p.KMOD_CTRL):
                    gs.undoMove()
                    # gs.printUndolog()
                    validMoves = gs.getValidMoves()
                    gameOver = False
                elif e.key == p.K_y and (p.key.get_mods() & p.KMOD_CTRL):
                    gs.redoMove()
                    # gs.printUndolog()
                    validMoves = gs.getValidMoves()
                elif e.key == p.K_r and (p.key.get_mods() & p.KMOD_CTRL):
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    prevSelection = ()
                    gameOver = False
                    # print("New Game")
                    # if gs.whiteToMove:
                    #     print("White's Turn")
                    # else:
                    #     print("Black's Turn")

        # AI move finder logic
        if not gameOver and not humanTurn:
            if len(validMoves) > 0:
                if not AIThinking:
                    AIThinking = True
                    print("Thinking...")
                    returnQueue = Queue() # used to pass data between processes
                    moveFinderProcess = Process(target=SmartMoveFinder.findBestMove, args=(gs, validMoves, returnQueue))
                    moveFinderProcess.start() # call findBestMove(gs, validMoves)

                if not moveFinderProcess.is_alive(): # if the process is done
                    print("Done Thinking")
                    AIMove = returnQueue.get()
                    if AIMove is None:
                        AIMove = SmartMoveFinder.findRandomMove(validMoves)
                    gs.makeMove(AIMove)
                    animateMove(AIMove, screen, gs.board, clock)
                    validMoves = gs.getValidMoves()
                    AIThinking = False
            
        drawGameState(screen, gs, validMoves, prevSelection, moveLogFont)

        if gs.checkmate or gs.stalemate:
            gameOver = True
            if gs.checkmate:
                if gs.whiteToMove:
                    text = "Black wins by checkmate"
                else:
                    text = "White wins by checkmate"
            elif gs.stalemate:
                text = "Stalemate" 
        drawEndGameText(screen, text) if gameOver else None

        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsible for all the graphics within a current game state
'''
def drawGameState(screen, gs, validMoves, prevSelection, moveLogFont):
    drawBoard(screen) # draw squares on the board
    highlightSquares(screen, gs, validMoves, prevSelection)
    drawPieces(screen, gs.board) # draw pieces on top of those squares
    drawMoveLog(screen, gs, moveLogFont)

'''
Draw the squares on the board
'''
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Highlight square selected and moves for piece selected
'''
def highlightSquares(screen, gs, validMoves, prevSelection):
    if prevSelection != ():
        r, c = prevSelection
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): # square selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparency value -> 0 transparent; 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


'''
Draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the move log
'''
def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveText = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i + 1])
        moveText.append(moveString)

    movesPerRow = 2
    padding = 30
    lineSpacing = 2
    textY = 10
    for i in range(0, len(moveText), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveText):
                text += moveText[i + j] + "    "
        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


'''
Draw the end game text
'''
def drawEndGameText(screen, text):

    textColor = p.Color("#D6EAF8")
    backgroundColor = p.Color("#333333")
    fontType = "comicsans"
    textSize = 20

    # Initialize Pygame font
    font = p.font.SysFont(fontType, textSize, False, False)

    # Render the text into an image (surface)
    textSurface = font.render(text, True, textColor)
    textRect = textSurface.get_rect()

    # Position the text
    textRect.topleft = (BOARD_WIDTH/2 - textSurface.get_width()/2, BOARD_HEIGHT/2 - textSurface.get_height()/2)

    # Calculate background box size based on text dimensions (+ some padding)
    backgroundRect = p.Rect(textRect.left - 5, textRect.top - 5, textRect.width + 10, textRect.height + 10)

    # Draw the background box
    p.draw.rect(screen, backgroundColor, backgroundRect, border_radius=10)

    # Draw the text on top of the background box
    screen.blit(textSurface, textRect)


'''
Animating a move
'''
def animateMove(move, screen, board, clock):
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 7 # frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = p.Color("white") if (move.endRow + move.endCol) % 2 == 0 else p.Color("gray")
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece onto rectangle
        if move.pieceCaptured != "--":
            if move.isenpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol*SQ_SIZE, enPassantRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
