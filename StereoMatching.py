from RandomMatch import drawRandom
from PIL import Image
import numpy as np
from matplotlib import pyplot as PLT
import time

def matchCost(left, right):
    z = (int(left) + int(right)) / 2
    result = ((z - left) * (z - right)) / 16
    return abs(result)

def disparity(left, right):
    return abs(left - right)

def costMatrix(left, right, rowSize):
    costOfOcclusion = 3.8
    colSize = len(left)
    arr = [[0 for i in range(colSize + 1)] for i in range(rowSize + 1)]
    steps = []
    for i in range(1, rowSize):
        arr[i][0] = i * costOfOcclusion
    for i in range(1, colSize):
        arr[0][i] = i * costOfOcclusion

    for i in range(1, rowSize):
        currentSteps = []
        for j in range(1, colSize):
            #print(left[i], " ", right[j], "  " , matchCost(left[i], right[j]))
            costOfMatch = matchCost(left[i], right[j]) + arr[i - 1][j - 1]
            leftOcculsion = arr[i-1][j] + costOfOcclusion
            rightOcculsion = arr[i][j - 1] + costOfOcclusion

            arr[i][j] = min(costOfMatch, rightOcculsion, leftOcculsion)

            if arr[i][j] == costOfMatch:
                currentSteps.append(1)
            elif arr[i][j] == rightOcculsion:
                currentSteps.append(2)
            else:
                currentSteps.append(3)
        steps.append(currentSteps)
    return steps

def backward(decisions):
    i = j = len(decisions) - 1
    result = [0 for i in range(len(decisions) + 1)]
    while (i >= 0 and j >= 0):
        last_decision = decisions[i][j]
        #print(last_decision)
        if last_decision == 1: # matched case
            #if i != j:
            result[i] = result[j] = disparity(i, j) + 128
            i -= 1
            j -= 1

        elif last_decision == 3 : # left[i] is occuluded
            result[i] = 0
            i -= 1
        else:                                 # right[j] is occuluded
            result[j] = 0
            j -= 1
    return result

def go():
    # bigSize = 512
    # smallSize = 256
    # drawRandom(bigSize, smallSize, 128, 124, 132)
    imgA = Image.open("/Users/chaozy/Desktop/CS/Algorithm/Coursework2/Stereo Pairs/Pair 2/disp1.png")
    #imgA = Image.open("imgLeft.png")
    imgA = np.asarray(imgA)
    imgB = Image.open("/Users/chaozy/Desktop/CS/Algorithm/Coursework2/Stereo Pairs/Pair 2/disp2.png")
    #imgB = Image.open("imgRight.png")
    imgB = np.asarray(imgB)

    bigSize = len(imgA)
    smallSize = len(imgA[0])
    disparityMatrix = np.array([[0 for i in range(bigSize)] for i in range(smallSize)])

    for i in range(len(imgA)):
        #if np.any(imgA[i] != imgB[i]):
            print(i)
            #print(imgA[i][90:], imgB[i][90:])
            disparityMatrix[i] = backward(costMatrix(imgA[i], imgB[i], bigSize))

    print(disparityMatrix.shape)
    # img = Image.new('L', (bigSize, bigSize))
    # img.putdata(np.reshape(disparityMatrix, bigSize * bigSize))
    # disparityMatrix = np.ndarray.flatten(disparityMatrix)

    img = Image.new('L', (bigSize, smallSize))
    img.putdata(np.reshape(disparityMatrix, smallSize * bigSize))

    img.save("result2.png")
    img.show()
    # PLT.imshow(disparityMatrix)
    # PLT.show()

t1 = time.time()
go()
t2 = time.time()
print("time taken: ", t2 - t1)


