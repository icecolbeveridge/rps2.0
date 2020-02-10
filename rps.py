# Analysis of RPS2.0

# Game state: R:{1,0,-1}, P:{} , S:{} (as tuple (R,P,S))
# Strategy: gameState: (pr, pp, ps)
# Value of position

import itertools

PZM = [1, 0, -1]
GAMESTATES = [p for p in itertools.product(PZM, repeat = 3)]
NEG = lambda g: tuple([-k for k in g])

currentValues = { g: 0.5 for g in GAMESTATES }
print (currentValues)   
currentStrategies = {g: (1/3., 1/3., 1/3.) for g in GAMESTATES}

value = lambda g, currentValues: 1 if 2 in g else 0 if -2 in g else currentValues[g]

def iterateValues( currentValues, currentStrategies ):
    # evaluate strategy for each state
    newValues = {}
    for g in GAMESTATES:
        if g not in newValues:
            newValues[g] = 0.
            newValues[NEG(g)] = 0.
            r, p, s = g
            score = [r,p,s]
            for myMove in [0,1,2]:
                probMe = currentStrategies[g][myMove]
                for theirMove in [0,1,2]:
                    probTh = currentStrategies[NEG(g)][theirMove]
                    res = (myMove - theirMove) % 3
                    P = probMe * probTh
                    if res == 0:
                        newValues[g] += P * value(tuple(score), currentValues)
                        newValues[NEG(g)] += P * value(NEG(tuple(score)), currentValues)

                    elif res == 1: 
                        score[myMove] += 1
                        newValues[g] += P * value(tuple(score), currentValues)
                        newValues[NEG(g)] += P * value(NEG(tuple(score)), currentValues)
                        score[myMove] -= 1
                    else:
                        score[theirMove] -= 1                                                
                        newValues[g] += P * value(tuple(score), currentValues)
                        newValues[NEG(g)] += P * value(NEG(tuple(score)), currentValues)
                        score[theirMove] += 1
            if g == NEG(g):
                newValues[g] *= 0.5
    return newValues

def iterateStrategies( currentValues, currentStrategies ):
    newStrategies = {}
    for  g in GAMESTATES:
        score = [g[0], g[1], g[2]]
        vals = [0., 0., 0.]
        for me in [0,1,2]:
            # suppose I make this move, what values do I expect?
            for them  in [0,1,2]:
                pt = currentStrategies[NEG(g)][them]
                res = (me - them) % 3
                if res == 0:
                    vals[me] += pt *  value( tuple(score), currentValues)
                elif res == 1:
                    score[me] += 1
                    vals[me] += pt * value( tuple(score),currentValues)
                    score[me] -= 1
                else:
                    score[them] += 1
                    vals[me] += pt * value( tuple(score), currentValues)
                    score[them] -= 1
        s = sum(vals)
        newStrategies[g] = [i/s for i in vals]
    return newStrategies
            
for i in range(1000):
    print ("***" + str(i))
    currentValues = iterateValues( currentValues, currentStrategies )
    currentStrategies = iterateStrategies( currentValues, currentStrategies )
    for j in GAMESTATES:
        print ( j, currentValues[j], currentStrategies[j] )
