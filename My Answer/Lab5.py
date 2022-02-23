from random import choice
from math import inf
import time

XPLAYER = +1
OPLAYER = -1
EMPTY = 0

board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]

def printBoard(brd):
    chars = {XPLAYER: 'X', OPLAYER: 'O', EMPTY: ' '}
    for x in brd:
        for y in x:
            ch = chars[y]
            print(f'| {ch} |', end='')
        print('\n' + '---------------')
    print('===============')

def clearBoard(brd):
    for x, row in enumerate(brd):
        for y, col in enumerate(row):
            brd[x][y] = EMPTY

def winningPlayer(brd, player):
    winningStates = [[brd[0][0], brd[0][1], brd[0][2]],
                     [brd[1][0], brd[1][1], brd[1][2]],
                     [brd[2][0], brd[2][1], brd[2][2]],
                     [brd[0][0], brd[1][0], brd[2][0]],
                     [brd[0][1], brd[1][1], brd[2][1]],
                     [brd[0][2], brd[1][2], brd[2][2]],
                     [brd[0][0], brd[1][1], brd[2][2]],
                     [brd[0][2], brd[1][1], brd[2][0]]]

    if [player, player, player] in winningStates:#if pleyer has won
        return 1
    
    if [-player, -player, -player] in winningStates:#if other player has won
        return -1

    #draw
    return 0

def gameWon(brd):
    return winningPlayer(brd, XPLAYER) !=0

def printResult(brd):
    if winningPlayer(brd, XPLAYER)==1:
        print('X has won! ' + '\n')

    elif winningPlayer(brd, OPLAYER)==1:
        print('O\'s have won! ' + '\n')

    else:
        print('Draw' + '\n')

def emptyCells(brd):
    emptyC = []
    for x, row in enumerate(brd):
        for y, col in enumerate(row):
            if brd[x][y] == EMPTY:
                emptyC.append([x, y])

    return emptyC

def boardFull(brd):
    if len(emptyCells(brd)) == 0:
        return True
    return False

def setMove(brd, x, y, player):
    brd[x][y] = player

def playerMove(brd):
    e = True
    moves = {1: [0, 0], 2: [0, 1], 3: [0, 2],
             4: [1, 0], 5: [1, 1], 6: [1, 2],
             7: [2, 0], 8: [2, 1], 9: [2, 2]}
    while e:
        try:
            move = int(input('Pick a position(1-9): '))
            if move < 1 or move > 9:
                print('Invalid location! ')
            elif not (moves[move] in emptyCells(brd)):
                print('Location filled')
            else:
                setMove(brd, moves[move][0], moves[move][1], XPLAYER)
                printBoard(brd)
                e = False
        except(KeyError, ValueError):
            print('Please pick a number!')

def getScore(brd):
    if winningPlayer(brd, XPLAYER):
        return 10

    elif winningPlayer(brd, OPLAYER):
        return -10

    else:
        return 0

def MiniMaxAB(brd, depth, alpha, beta, player):#returns (x,y)
    #print(maximize(brd,depth,alpha,beta))
    #time.sleep(20)
    new_brd,_ = maximize(brd,depth,alpha,beta)
    for i in range(3):
        for j in range(3):
            if new_brd[i][j]!=brd[i][j]:
                x,y=i,j
                break
    return (x,y)
  
def maximize(brd,depth,alpha,beta):
    if depth ==0:#if terminal state
        return (None,winningPlayer(brd, OPLAYER))

    max_child,max_utility = None,-inf
    
    #generate children
    children = []
    for i in range(3):
        for j in range(3):
            if brd[i][j] ==0 :
                brd[i][j]=-1
                children.append([row[:] for row in brd])                
                brd[i][j]=0

    for child in children:
        (_,utillity) = minimize(child, depth-1, alpha, beta)
        
        if utillity > max_utility: #إذا وجدت سيناريو افضل (بالنسبة إلي) من الي وجدتو
            max_child,max_utility = child,utillity
            
        if max_utility >= beta:
            break
        
        if max_utility > alpha:
            alpha = max_utility
              
    return max_child,max_utility

def minimize(brd,depth,alpha,beta):
    if depth ==0:#if terminal state
        return (None,winningPlayer(brd, OPLAYER))

    min_child,min_utility = None,inf
    
    #generate children
    children = []
    for i in range(3):
        for j in range(3):
            if brd[i][j] ==0 :
                brd[i][j]=1
                children.append([row[:] for row in brd])                
                brd[i][j]=0

    for child in children:
        (_,utillity) = maximize(child, depth-1, alpha, beta)
        
        if utillity <min_utility:#إذا وجدت سيناريو افضل (بالنسبة إلي) من الي وجدتو 
            min_child,min_utility = child,utillity
            
        if min_utility <= alpha:
            break
        
        if min_utility < beta:
            beta = min_utility
              
    return min_child,min_utility

def AIMove(brd):
    if len(emptyCells(brd)) == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
        setMove(brd, x, y, OPLAYER)
        printBoard(brd)

    else:
        result = MiniMaxAB(brd, len(emptyCells(brd)), -inf, inf, OPLAYER)
        setMove(brd, result[0], result[1], OPLAYER)
        printBoard(brd)

def AI2Move(brd):
    if len(emptyCells(brd)) == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
        setMove(brd, x, y, XPLAYER)
        printBoard(brd)

    else:
        result = MiniMaxAB(brd, len(emptyCells(brd)), -inf, inf, XPLAYER)
        setMove(brd, result[0], result[1], XPLAYER)
        printBoard(brd)

def makeMove(brd, player, mode):
    if mode == 1:
        if player == XPLAYER:
            playerMove(brd)
        else:
            AIMove(brd)
    else:
        if player == XPLAYER:
            AIMove(brd)
        else:
            AI2Move(brd)

def playerVSai():

    clearBoard(board)
    currentPlayer = XPLAYER

    while not (boardFull(board) or gameWon(board)):
        makeMove(board, currentPlayer, 1)
        currentPlayer *= -1

    printResult(board)

def main():
    playerVSai()

if __name__ == '__main__':
    main()