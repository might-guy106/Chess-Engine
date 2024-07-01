import random

pieceScore = {"K": 20000, "Q": 900, "R": 500, "B": 330, "N": 320, "P": 100}

knightScores = [[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
                [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
                [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
                [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
                [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
                [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
                [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]

bishopScores = [[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
                [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
                [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
                [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
                [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
                [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]

rookScores =   [[ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
                [ 0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
                [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
                [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
                [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
                [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
                [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
                [ 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0]]

queenScores =  [[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
                [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
                [ 0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
                [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
                [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
                [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]

kingScores =   [[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                [2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
                [2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]]

pawnScores =   [[0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
                [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
                [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
                [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
                [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
                [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
                [0.5,  1.0,  1.0, -2.0, -2.0,  1.0,  1.0,  0.5],
                [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]

positionScalingFactors = {
    "P": 0.1,    # Pawns: positioning is quite important
    "N": 0.08,   # Knights: positioning is very important
    "B": 0.07,   # Bishops: positioning is important
    "R": 0.06,   # Rooks: positioning matters, but less than for minor pieces
    "Q": 0.04,   # Queen: very mobile, so positioning is less critical
    "K": 0.15    # King: position can be crucial, especially in endgame
}

piecePositionScores = {"N": knightScores, "B": bishopScores, "R": rookScores, "Q": queenScores, "K": kingScores, "P": pawnScores}

CHECKMATE = 100000
STALEMATE  = 0
DEPTH = 4


def findRandomMove(validmoves):
    global nextMove, counter
    nextMove = validmoves[random.randint(0, len(validmoves) - 1)]


'''
helper method to make the first recursive call
'''
def findBestMove(gs, validMoves, returnQueue):
    global nextMove, counter
    nextMove = None
    counter = 0
    # findRandomMove(validMoves)
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    # temp = findMoveNegaMax(gs, validMoves, DEPTH,1 if gs.whiteToMove else -1)
    temp = findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    print("best move score" , temp)
    returnQueue.put(nextMove)


def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    # move ordering - implement later
    ordered_moves = order_moves(gs, validMoves)

    maxScore = -CHECKMATE
    for move in ordered_moves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

def findMoveNegaMaxAlphaBeta2(gs, validMoves, depth, alpha, beta, isMaximizingPlayer):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return scoreBoard(gs)
    
    # move ordering - implement later
    ordered_moves = order_moves(gs, validMoves)

    if isMaximizingPlayer:
        maxScore = -CHECKMATE
        for move in ordered_moves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveNegaMaxAlphaBeta2(gs, nextMoves, depth - 1, alpha, beta, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
        return maxScore
    else:
        minScore = CHECKMATE
        for move in ordered_moves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveNegaMaxAlphaBeta2(gs, nextMoves, depth - 1, alpha, beta, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
            if minScore < beta:
                beta = minScore
            if alpha >= beta:
                break
        return minScore
'''
A positive score is good for white, a negative score is good for black
'''
def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE # black wins
        else:
            return CHECKMATE # white wins
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                if square[0] == 'w':
                    score +=  pieceScore[square[1]] + (piecePositionScores[square[1]][row][col] * positionScalingFactors[square[1]] * 0)
                if square[0] == 'b':
                    score -= pieceScore[square[1]] + (piecePositionScores[square[1]][7-row][col] * positionScalingFactors[square[1]] * 0)
    return score

def evaluate_backup(gs, move):
    return 0 # Implement later

def order_moves(gs, valid_moves):
    # Initialize a list to store moves with their scores
    scored_moves = []
    
    for move in valid_moves:
        score = 0
        
        # Capture moves
        if move.isCaptureMove:
            # MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
            victim = move.pieceCaptured
            attacker = move.pieceMoved
            score += 10 * pieceScore[victim[1]] - pieceScore[attacker[1]]
        
        # Promotion moves
        if move.ispawnPromotion:
            score += 800  # Slightly less than a queen's value
        
        # Castling
        if move.isCastleMove:
            score += 60
        
        # Check moves
        gs.makeMove(move)
        if gs.inCheck:
            score += 50
        
        # # New logic: Check if the move provides backup
        score += evaluate_backup(gs, move)

        gs.undoMove()
        
        # Central pawn moves (assuming standard chess board)
        if move.pieceMoved[1] == "P" and move.endCol in [2, 3, 4, 5]:
                score += 10
        
        # Piece development (moving pieces off the first rank)
        if move.startRow in [0, 7] and move.endRow not in [0, 7]:
            score += 5

        
        scored_moves.append((move, score))
    
    # Sort moves by score in descending order
    scored_moves.sort(key=lambda x: x[1], reverse=True)
    
    # Return only the moves, without the scores
    return [move for move, score in scored_moves]
