# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 22:08:59 2020

@author: Rodion Lim
"""

import numpy as np

# Input parsing
def parseInput(file):
    with open(file, "r") as f:
        constraint = int(f.readline().split(" ")[0])
        slices = [int(x) for x in f.readline().split(" ")]
        slicesIdx = np.flip(np.array(list(enumerate(slices))))
    return constraint, slicesIdx

# Conditional cumulative sum on constraint
def cumSumConstraint(data, constraint):
    seed = 0
    for row in data:
        if row[0] + seed > constraint:
            yield False
        else:
            seed+=row[0]
            yield True

# Gets the closest sum of slices to the constraint
def getSumSlices(data, constraint):
    data = data[list(cumSumConstraint(data, constraint))]
    return (sum(data[:,0]), data)

# Inner permutation
def permutateSingleSlice(data):
    for x in [x for x in range(len(data))]:
        if x==0:
            yield data
        else:
            yield np.delete(data, list(range(1+x)), 0)

# Returns output in the format required by problem set
def formatOutput(data, workingsFlag=False):
    pizzaIdx = list(data[:,1])
    pizzaSlices = list(data[:,0])
    return [sum(pizzaSlices), pizzaSlices] if workingsFlag else [len(pizzaIdx), pizzaIdx[::-1]]

# Persists output to disk
def exportOutput(outputName, parsedData):
    with open(outputName, "w") as f:
        f.writelines(str(parsedData[0]) + "\n")
        f.writelines(" ".join([str(x) for x in parsedData[1]]) + "\n")
        
def getMaxSlices(slicesIdx, constraint, maxPerm=0):
    maxSumSlices = 0 # initial seed
    firstIter = True
    # We first drop the biggest values (Outer permutation)
    for dropRows in [x for x,y in enumerate(constraint <= np.flip(np.flip(slicesIdx[:,0]).cumsum())) if y==True]:
        if firstIter:
            data = slicesIdx
            firstIter = False
        else:
            data = np.delete(slicesIdx, dropRows, 0)
        # Then we drop the inner values (Inner permutation)
        for i, data in enumerate(permutateSingleSlice(data)):
            if i>maxPerm:
                continue
            else:
                sumSlices, data = getSumSlices(data, constraint)
                if sumSlices==constraint: # Exit early if possible
                    return data
                elif sumSlices>maxSumSlices:
                    maxSumSlices = sumSlices
                    cacheData = data # Get the slices combination closest to constraint
    return cacheData

# Wrapper to call the main algorithm
def pizzaProb(file, maxPerm=0, workingsFlag=False):
    constraint, slicesIdx = parseInput(file)
    return formatOutput(getMaxSlices(slicesIdx, constraint, maxPerm), workingsFlag)

# Files definition
filesList = [x + ".in" for x in ["a_example", "b_small", "c_medium", "d_quite_big", "e_also_big"]]

if __name__ == "__main__":
    inputName = filesList
    outputName = [x.replace(".in", ".out") for x in filesList]
    output = [pizzaProb(x, maxPerm=1, workingsFlag=False) for x in filesList] # Set working flag to true to display workings
    try:
        [exportOutput(x[0], x[1]) for x in list(zip(outputName, output))]
        print("Create Submission files successfully")
    except:
        print("Export failed")
