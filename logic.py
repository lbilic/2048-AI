from random import *
from copy import deepcopy
from time import sleep

WEIGHT = [
        [ 6,  5,  4,  1],
        [ 5,  4,  1,  0],
        [ 4,  1,  0, -1],
        [ 1, 0, -1, -2]
]

MOVES = ["up", "left", "down", "right"]

def score(mat):
    score = 0
    for i in range(0, 3):
        for j in range(0, 3):
            score += WEIGHT[i][j] * mat[i][j]
    return score

def penalty(mat):
    penalty = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if(j < 3):
                if(mat[i][j+1] !=0):
                    penalty += abs(mat[i][j] - mat[i][j+1])
            if(j > 0):
                if(mat[i][j-1] !=0):
                    penalty += abs(mat[i][j] - mat[i][j-1])
            if(i < 3):
                if(mat[i+1][j] !=0):
                    penalty += abs(mat[i][j] - mat[i+1][j])
            if(i > 0):
                if(mat[i-1][j] !=0):
                    penalty += abs(mat[i][j] - mat[i-1][j])
    return penalty

def heur(mat):
    return score(mat) - penalty(mat) + len(get_empty_tiles(mat))*400

def new_game(n):
    matrix = []

    for i in range(n):
        matrix.append([0] * n)
    return matrix

def add_two(mat):
    a=randint(0,len(mat)-1)
    b=randint(0,len(mat)-1)
    while(mat[a][b]!=0):
        a=randint(0,len(mat)-1)
        b=randint(0,len(mat)-1)
    mat[a][b]=2
    return mat

def add_new(mat):
    a=randint(0,len(mat)-1)
    b=randint(0,len(mat)-1)
    while(mat[a][b]!=0):
        a=randint(0,len(mat)-1)
        b=randint(0,len(mat)-1)
    mat[a][b]=choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
    return mat

def game_state(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j]==2048:
                return 'win'
    for i in range(len(mat)-1): #intentionally reduced to check the row on the right and below
        for j in range(len(mat[0])-1): #more elegant to use exceptions but most likely this will be their solution
            if mat[i][j]==mat[i+1][j] or mat[i][j+1]==mat[i][j]:
                return 'not over'
    for i in range(len(mat)): #check for any zero entries
        for j in range(len(mat[0])):
            if mat[i][j]==0:
                return 'not over'
    for k in range(len(mat)-1): #to check the left/right entries on the last row
        if mat[len(mat)-1][k]==mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1): #check up/down entries on last column
        if mat[j][len(mat)-1]==mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'

def get_empty_tiles(mat):
    retVal = []
    for i in range(0, 3):
        for j in range(0, 3):
            if(mat[i][j] == 0):
                retVal.append((i, j))
    return retVal

def expectimax(grid, depth, agent):
    if depth == 0:
        return heur(grid)
    elif agent is "BOARD":
        score = 0
        empty_tiles = get_empty_tiles(grid)
        number_of_empty = len(empty_tiles)
        for tile in empty_tiles:
            newGrid = [row[:] for row in grid]
            newGrid[tile[0]][tile[1]] = 2
            newScore = expectimax(newGrid, depth - 1, "PLAYER")
            if newScore == -99999:
                score += 0
            else:
                score += (0.9 * newScore)

            newGrid = [row[:] for row in grid]
            newGrid[tile[0]][tile[1]] = 4
            newScore = expectimax(newGrid, depth - 1, "PLAYER")
            if newScore == -99999:
                score += 0
            else:
                score += (0.1 * newScore)
        if(number_of_empty == 0):
            return heur(grid)
        else:
            return score/number_of_empty
    elif agent is "PLAYER":
        score = -99999
        for dir in MOVES:
            newGrid = [row[:] for row in grid]
            nextLevel = [row[:] for row in grid]
            move(nextLevel, dir)
            if newGrid == nextLevel:
                continue
            score = max([score, expectimax(newGrid, depth-1, "BOARD")])
        return score

def getBestMove(grid, depth):
    score = -999999
    bestMove = "none"

    for m in MOVES:
        newGrid = [row[:] for row in grid]
        #if newGrid == move([row[:] for row in grid], m)[0]:
        if newGrid == move(newGrid, m)[0]:
            continue
        
        newScore = expectimax(newGrid, depth - 1, "BOARD")

        if newScore > score:
            bestMove = m
            score = newScore
    
    return bestMove

def move(grid, dir):
    if dir == "left":
        return left(grid)
    elif dir == "right":
        return right(grid)
    elif dir == "up":
        return up(grid)
    elif dir == "down":
        return down(grid)

def reverse(mat):
    new=[]
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new

def transpose(mat):
    new=[]
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new

def cover_up(mat):
    new=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    done=False
    for i in range(4):
        count=0
        for j in range(4):
            if mat[i][j]!=0:
                new[i][count]=mat[i][j]
                if j!=count:
                    done=True
                count+=1
    return (new,done)

def merge(mat):
    done=False
    for i in range(4):
         for j in range(3):
             if mat[i][j]==mat[i][j+1] and mat[i][j]!=0:
                 mat[i][j]*=2
                 mat[i][j+1]=0
                 done=True
    return (mat,done)

def up(game):
        # return matrix after shifting up
        game=transpose(game)
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        done=done or temp[1]
        game=cover_up(game)[0]
        game=transpose(game)
        return (game,done)

def down(game):
        game=reverse(transpose(game))
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        done=done or temp[1]
        game=cover_up(game)[0]
        game=transpose(reverse(game))
        return (game,done)

def left(game):
        # return matrix after shifting left
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        done=done or temp[1]
        game=cover_up(game)[0]
        return (game,done)

def right(game):
        # return matrix after shifting right
        game=reverse(game)
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        done=done or temp[1]
        game=cover_up(game)[0]
        game=reverse(game)
        return (game,done)
