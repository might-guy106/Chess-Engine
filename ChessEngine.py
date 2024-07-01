"""

This class is responsible for storing all the information about the current state of a class game.
It will be responsible for determing the valid moves at current state. It will also kee; move log
"""

class GameState():
    def __init__(self):
        # board is 8x8 2d list , each element of the list has 2 characters
        # first character represents the color of the piece, 'b' or 'w'
        # second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N', 'P'
        # "--" represents an empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.whiteToMove = True
        self.moveLog = []
        self.undomoveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.enpassantPossible = () # coordinates for the square where en passant capture is possible
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(True,True,True,True)] # history of castling rights


    '''
    Takes a move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        self.undomoveLog = [] # clear the undomoveLog
        # update the king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # pawn promotion
        if move.ispawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # en passant move
        if move.isenpassantMove:
            self.board[move.startRow][move.endCol] = "--"
        
        # update enpassantPossible variable
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

        # castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: # king side castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] # moves the rook
                self.board[move.endRow][move.endCol + 1] = "--" # erase old rook
            else: # queen side castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2] # moves the rook
                self.board[move.endRow][move.endCol - 2] = "--" # erase old rook

        # update enpassant rights log
        self.enpassantPossibleLog.append(self.enpassantPossible)

        # update castling rights log
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs, self.currentCastlingRights.bks, self.currentCastlingRights.bqs))

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.undomoveLog.append(move)

            self.board[move.startRow][move.startCol] = move.pieceMoved # put the piece back to the start square
            self.board[move.endRow][move.endCol] = move.pieceCaptured # put the captured piece back to the end square

            # undo en passant move 
            if move.isenpassantMove:
                self.board[move.startRow][move.endCol] = move.pieceCaptured # bring the captured pawn back
                self.board[move.endRow][move.endCol] = "--" # remove the attacking pawn from its ending position

            # undo en passant rights
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[len(self.enpassantPossibleLog) - 1]
            
            
            # undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: # king side castle
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"
                else: # queen side castle
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"

            # undo castling rights
            self.castleRightsLog.pop() # get rid of the new castle rights from the move we are undoing
            newRights = self.castleRightsLog[len(self.castleRightsLog) - 1] # set the current castle rights to the last one in the list
            self.currentCastlingRights = CastleRights(newRights.wks, newRights.wqs, newRights.bks, newRights.bqs)

            # update the king's location if moved
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            # update the checkmate and stalemate variables
            self.checkmate = False
            self.stalemate = False

            self.whiteToMove = not self.whiteToMove # switch turns back

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: # left rook
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: # left rook
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastlingRights.bks = False

        # if a rook is captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.bks = False
                

    def printUndolog(self):
        print("size of move log is ",len(self.moveLog))
        print("size of undo log is ", len(self.undomoveLog))

    def redoMove(self):
        if len(self.undomoveLog) != 0:
            move = self.undomoveLog.pop()
            tempUndomoveLog = list(self.undomoveLog) # we dont want to clear the undomovelog if it is a redo move so we are storing it in a temp variable
            self.makeMove(move)
            # update the king's location if moved
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.endRow, move.endCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.endRow, move.endCol)
            self.undomoveLog = tempUndomoveLog

    '''
    All moves considering current check status
    '''
    def getValidMoves(self):
        # if len(self.moveLog) != 0:
        #     print("Valid Moves after move: ",self.moveLog[len(self.moveLog)-1].getChessNotation())
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        # if self.inCheck:
        #     for i in range(len(self.checks)):
        #         print("Check from ",self.checks[i])
        #     for i in range(len(self.pins)):
        #         print("Pinned piece at ",self.pins[i])

        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                # to move out of check, we must capture the attacking piece, block the check with another piece, or move the king
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                # print("Single check case is due to ",pieceChecking)
                validSquares = [] # squares that pieces can move to
                # if check is by knight,then it must be captured or we should move king as it cannot be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) # check[2] and check[3] are the directions to move to get out of check
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: # once you capture the piece that is checking, you are done
                            break
                for i in range(len(moves) - 1, -1, -1): # go through the list backwards when you are removing from it
                    if moves[i].pieceMoved[1] != 'K': # as all King moves are valid so we check for other pieces
                        if not (moves[i].endRow, moves[i].endCol) in validSquares: # if any move does not block or capture target,we remove it
                            moves.remove(moves[i])
            else:
                self.getKingMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            moves = self.getAllPossibleMoves()

        if len(moves) == 0:
            if self.inCheck:
                self.checkmate = True
                # print("Checkmate")
            else:
                self.stalemate = True
                # print("Stalemate")
        else:
            self.checkmate = False
            self.stalemate = False
        
        return moves

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)) # 8 directions from king to another piece
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = kingRow + d[0] * i
                endCol = kingCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        continue
                    elif endPiece[0] == self.board[kingRow][kingCol][0] and endPiece[1] != 'K': # same color piece           
                        if possiblePin == (): # first piece found along the direction
                            # print("ally piece is ",endPiece , " at location ",endRow,endCol)
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: # 2nd piece found, so no pin or check from this direction
                            break
                    elif endPiece[0] != self.board[kingRow][kingCol][0]: # enemy piece
                        type = endPiece[1]
                        
                        if (0 <= j <= 3 and type == 'R') or (4 <= j <= 7 and type == 'B') or (i == 1 and type == 'P' and ((not self.whiteToMove and 6 <= j <= 7) or (self.whiteToMove and 4 <= j <= 5))) or (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == (): # no piece blocking, so check
                                inCheck = True
                                # print("enemy piece is ",endPiece , " at location ",endRow,endCol)
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: # piece blocking so pin 
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break # off board
        # check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = kingRow + m[0]
            endCol = kingCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != self.board[kingRow][kingCol][0] and endPiece[1] == 'N': # enemy knight attacking the king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
                    
        return inCheck, pins, checks
    

    '''
    Determine if enemy can attack the square (r, c) , done by first moving the piece to the square and then checking for attacks then undoing the move
    '''
    def squareUnderAttack(self,move):
        tempenpassantPossible = self.enpassantPossible
        tempundomoveLog = list(self.undomoveLog)
        self.makeMove(move)
        squareRow = move.endRow
        squareCol = move.endCol
        attack = False
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            for i in range(1, 8):
                endRow = squareRow + d[0] * i
                endCol = squareCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        continue
                    elif endPiece[0] == self.board[squareRow][squareCol][0] and endPiece[1] != 'K':
                        break
                    elif endPiece[0] != self.board[squareRow][squareCol][0]:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == 'R') or (4 <= j <= 7 and type == 'B') or (i == 1 and type == 'P' and ((self.whiteToMove and 6 <= j <= 7) or (not self.whiteToMove and 4 <= j <= 5))) or (type == 'Q') or (i == 1 and type == 'K'):
                            attack = True
                            break
                        else:
                            break
        self.undoMove()
        self.undomoveLog = tempundomoveLog
        self.enpassantPossible = tempenpassantPossible
        return attack
    
    '''
    All moves without considering check status in current state
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                piece = self.board[r][c][1]
                if (self.whiteToMove and turn == 'w') or (not self.whiteToMove and turn == 'b'):
                    if piece == 'P':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
        return moves
    
    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''
    # # modified    
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirections = []

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirections.append((self.pins[i][2], self.pins[i][3]))
                pinDirections.append((-self.pins[i][2], -self.pins[i][3]))
                self.pins.remove(self.pins[i])
                break
        
        if self.whiteToMove:
            move_amount = -1
            start_row = 6
            enemy_color = "b"
            king_row, king_col = self.whiteKingLocation
        else:
            move_amount = 1
            start_row = 1
            enemy_color = "w"
            king_row, king_col = self.blackKingLocation

        if self.board[r + move_amount][c] == "--":
            if not piecePinned or (move_amount, 0) in pinDirections:
                moves.append(Move((r, c), (r + move_amount, c), self.board))
                if r == start_row and self.board[r + 2 * move_amount][c] == "--":
                    moves.append(Move((r, c), (r + 2 * move_amount, c), self.board))

        if c - 1 >= 0: # captures to the left
            d = (move_amount, -1)
            if not piecePinned or d in pinDirections:
                if self.board[r + move_amount][c - 1][0] == enemy_color:
                    moves.append(Move((r, c), (r + move_amount, c - 1), self.board))
                if (r + move_amount, c - 1) == self.enpassantPossible:
                    attacking_piece = False # 
                    blocking_piece = False # if the pawn is pinned, it cannot attack the square directly in front of the enemy king
                    if king_row == r:
                        if king_col < c: # king is left to the pawn
                            # inside: between king and the pawn
                            # outside: between pawn and border
                            inside_range = range(king_col + 1,c - 2)
                            outside_range = range(c + 1,8)
                        else: # king is right to the pawn
                            inside_range = range(c + 1,king_col)
                            outside_range = range(0,c - 2)

                        for i in inside_range:
                            if self.board[r][i] != "--": # that means there is a piece in between king and pawn so that after enpassant move king does not come to check
                                blocking_piece = True
                        
                        for i in outside_range:
                            square = self.board[r][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True

                    if not attacking_piece or blocking_piece:
                        # print("Enpassant move is possible at left side")
                        moves.append(Move((r, c), (r + move_amount, c - 1), self.board, isenpassantMove = True))

        if c + 1 <= 7: # captures to the right
            d = (move_amount, 1)
            if not piecePinned or d in pinDirections:
                if self.board[r + move_amount][c + 1][0] == enemy_color:
                    moves.append(Move((r,c),(r + move_amount,c + 1),self.board))
                if (r + move_amount, c + 1) == self.enpassantPossible:
                    attacking_piece = False
                    blocking_piece = False
                    if king_row == r:
                        if king_col < c:
                            inside_range = range(king_col,c - 1)
                            outside_range = range(c + 2,8)
                        else:
                            inside_range = range(c + 2,king_col)
                            outside_range = range(0,c)

                        for i in inside_range:
                            if self.board[r][i] != "--":
                                blocking_piece = True
                        
                        for i in outside_range:
                            square = self.board[r][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    
                    if not attacking_piece or blocking_piece:
                        # print("Enpassant move is possible at right side")
                        moves.append(Move((r, c), (r + move_amount, c + 1), self.board, isenpassantMove = True))
 

        

    '''
    Get all the rook moves for the rook located at row, col and add these moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirections = []

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirections.append((self.pins[i][2], self.pins[i][3]))
                pinDirections.append((-self.pins[i][2], -self.pins[i][3]))
                if self.board[r][c][1] != 'Q': # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            if not piecePinned or d in pinDirections:
                for i in range(1, 8):
                    endRow = r + d[0] * i
                    endCol = c + d[1] * i
                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        if self.board[endRow][endCol] == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif self.board[endRow][endCol][0] != self.board[r][c][0]:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
    
    '''
    Get all the knight moves for the knight located at row, col and add these moves to the list
    '''
    def getKnightMoves(self, r, c, moves):
        piecePinned = False

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                break

        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    if self.board[endRow][endCol] == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif self.board[endRow][endCol][0] != self.board[r][c][0]:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
    
    '''
    Get all the bishop moves for the bishop located at row, col and add these moves to the list
    '''
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirections = []

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirections.append((self.pins[i][2], self.pins[i][3]))
                pinDirections.append((-self.pins[i][2], -self.pins[i][3]))
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        for d in directions:
            if not piecePinned or d in pinDirections:
                for i in range(1, 8):
                    endRow = r + d[0] * i
                    endCol = c + d[1] * i
                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        if self.board[endRow][endCol] == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif self.board[endRow][endCol][0] != self.board[r][c][0]:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
    
    '''
    Get all the queen moves for the queen located at row, col and add these moves to the list
    '''
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
    Get all the king moves for the king located at row, col and add these moves to the list
    '''
    def getKingMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endpiece = self.board[endRow][endCol]
                if endpiece == "--" or endpiece[0] != allyColor:
                    move = Move((r, c), (endRow, endCol), self.board)
                    if not self.squareUnderAttack(move):
                        moves.append(move)

        self.getCastleMoves(r, c, moves)


    '''
    Get all the castle moves for the king located at (r,c) and add these moves to the list
    '''
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(Move((r, c), (r, c), self.board)):
            return # can't castle while we are in check
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.kingSideCastle(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.queenSideCastle(r, c, moves)

    '''
    Get the king side castle move for the king located at (r,c) and add this move to the list
    '''
    def kingSideCastle(self, r, c, moves):
        if self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--":
            if not self.squareUnderAttack(Move((r, c), (r, c + 1), self.board)) and not self.squareUnderAttack(Move((r, c), (r, c + 2), self.board)):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove = True))
        
    '''
    Get the queen side castle move for the king located at (r,c) and add this move to the list
    '''
    def queenSideCastle(self, r, c, moves):
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--":
            if not self.squareUnderAttack(Move((r, c), (r, c - 1), self.board)) and not self.squareUnderAttack(Move((r, c), (r, c - 2), self.board)):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove = True))


class CastleRights():
    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs



class Move():
    # maps keys to values
    # key : value
    # (row, col) : (row, col)
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isenpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # pawn promotion
        self.ispawnPromotion = ((self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7))
        # en passant
        self.isenpassantMove = isenpassantMove
        if self.isenpassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'
        # castle move
        self.isCastleMove = isCastleMove
        self.isCaptureMove = self.pieceCaptured != "--"

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        """
        Overriding the equals method.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        # you can add to make this real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
    # overide the str method
    def __str__(self):
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"
        
        endSquare = self.getRankFile(self.endRow, self.endCol)

        # if a pawn is moved, we don't need to specify the piece
        if self.pieceMoved[1] == 'P':
            if self.pieceCaptured != "--":
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare
        
        # if a piece other than pawn is moved, we need to specify the piece
        moveString = self.pieceMoved[1]
        if self.pieceCaptured != "--": 
            moveString += "x"
        return moveString + endSquare
        
        # pawn promotion

        # en passant

        # adding + or # for check or checkmate

        # two of the same type of piece can move to the same square, so we need to specify the start file or rank
    
            
