from random import *
from copy import deepcopy
from time import sleep
from random import randint
from math import log

'''WEIGHT = [
        [ 6,  5,  4,  1],
        [ 5,  4,  1,  0],
        [ 4,  1,  0, -1],
        [ 1, 0, -1, -2]
]'''

WEIGHT = [
        [ 0.135759, 0.121925, 0.102812, 0.099937],
        [ 0.0997992, 0.0888405, 0.076711, 0.0724143],
        [ 0.060654, 0.0562579, 0.037116, 0.0161889],
        [ 0.0125498, 0.00992495, 0.00575871, 0.00335193]
]

MOVES = ["up", "right", "down", "left"]

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

#def heur(mat):
#    return score(mat) - penalty(mat)

def heur(mat):
    weight_1 = 11.992
    weight_2 = 13.959
    weight_3 = 7.05
    weight_4 = 3.967
    weight_5 = -0.282

    state = [elem for sub in mat for elem in sub]
    max_cell = log(max(state), 2)

    free_tiles = 0.0
    adjacent_sum = 1.0
    adjacent_cells = 0.0
    edges_sum = 0.0
    # diff_adjacent_cells = 0.0
    sum_tiles = 0.0
    for i, coord in enumerate(state):
        if coord == 0:
            free_tiles += 1.0
        else:
            sum_tiles += coord
            y = i // 4
            x = i % 4
            if x > 0 and state[(x-1) + y*4] != 0:
                adjacent_sum += abs(log(coord, 2) - log(state[(x-1) + y*4], 2))
                if coord == state[(x-1) + y*4]:
                    adjacent_cells += 1.0
                    
            if x < 3 and state[(x+1) + y*4] != 0:
                adjacent_sum += abs(log(coord, 2) - log(state[(x+1) + y*4], 2))
                if coord == state[(x+1) + y*4]:
                    adjacent_cells += 1.0

            if y > 0 and state[x + (y-1)*4] != 0:
                adjacent_sum += abs(log(coord, 2) - log(state[x + (y-1)*4], 2))
                if coord == state[x + (y-1)*4]:
                    adjacent_cells += 1.0

            if y < 3 and state[x + (y+1)*4] != 0:
                adjacent_sum += abs(log(coord, 2) - log(state[x + (y+1)*4], 2))
                if coord == state[x + (y+1)*4]:
                    adjacent_cells += 1.0

    if state[0] != 0:
        edges_sum += log(state[0], 2)
    if state[3] != 0:
        edges_sum += log(state[3], 2)
    if state[12] != 0:
        edges_sum += log(state[12], 2)
    if state[15] != 0:
        edges_sum += log(state[15], 2)
    return (max_cell * weight_1) + \
            (free_tiles * weight_2) + \
            (adjacent_cells * weight_3) + \
            (edges_sum * weight_4) + \
            (adjacent_sum * weight_5)

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

def add_four(mat):
    a=randint(0,len(mat)-1)
    b=randint(0,len(mat)-1)
    while(mat[a][b]!=0):
        a=randint(0,len(mat)-1)
        b=randint(0,len(mat)-1)
    mat[a][b]=4
    return mat

def add_new(mat):
    a=randint(0,len(mat)-1)
    b=randint(0,len(mat)-1)
    while(mat[a][b]!=0):
        a=randint(0,len(mat)-1)
        b=randint(0,len(mat)-1)
    mat[a][b]= 2 if randint(0,100) <= 90 else 4
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

def get_possible_moves(grid):
    possible = 0
    for m in MOVES:
        newGrid = [row[:] for row in grid]

        if grid != move(newGrid, m)[0]:
            possible += 1
    return possible

def expectimax(grid, depth, agent):
    if depth == 0:
        return heur(grid)
    elif agent is "BOARD":
        score = 0
        empty_tiles = get_empty_tiles(grid)
        #number_of_empty = len(empty_tiles)
        #possible = get_possible_moves(grid)
        for tile in empty_tiles:
            newGrid = [row[:] for row in grid]
            newGrid[tile[0]][tile[1]] = 4
            newScore = expectimax(newGrid, depth - 1, "PLAYER")
            if newScore == -99999:
                score += 0
            else:
                score += (0.1 * newScore)


            newGrid = [row[:] for row in grid]
            newGrid[tile[0]][tile[1]] = 2
            newScore = expectimax(newGrid, depth - 1, "PLAYER")
            if newScore == -99999:
                score += 0
            else:
                score += (0.9 * newScore)

        #if(number_of_empty == 0):
        #    return score
        #else:
        #    return score/number_of_empty
        return score
    elif agent is "PLAYER":
        score = -99999
        for dir in MOVES:
            newGrid = [row[:] for row in grid]
            nextLevel = [row[:] for row in grid]
            nextLevel = move(nextLevel, dir)[0]
            if newGrid == nextLevel:
                continue
            newScore = expectimax(newGrid, depth-1, "BOARD")
            if newScore > score:
                score = newScore
            #score = max([score, expectimax(newGrid, depth-1, "BOARD")])
        return score

def getBestMove(grid, depth):
    score = -999999
    bestMove = "none"

    for m in MOVES:
        newGrid = [row[:] for row in grid]
        newGrid = move(newGrid, m)[0]
        if grid == newGrid:
            continue
        
        newScore = expectimax(newGrid, depth-1, "BOARD")

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
