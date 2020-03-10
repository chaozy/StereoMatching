from RandomMatch import drawRandom
from PIL import Image
import numpy as np
import time

def matchCost(left, right):
    z = ((left) + (right)) / 2
    result = ((z - left) * (z - right)) / 16
    return abs(result)

def disparity(left, right):
    return abs(left - right)

def rgbToIntensity(rgb):
    return sum(rgb) / len(rgb)

def costMatrix(left, right):
    costOfOcclusion = 1.8
    size = len(left)
    arr = [[0 for i in range(size + 1)] for i in range(size + 1)]
    steps = []
    test = [None for _ in range(size + 1)]
    for i in range(1, size + 1):
        arr[i][0] = i * costOfOcclusion
        arr[0][i] = i * costOfOcclusion

    for i in range(1, size):
        currentSteps = []
        for j in range(1, size):
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
        if last_decision == 1: # matched case
            result[i] = disparity(i, j) + 128
            i -= 1
            j -= 1
        elif last_decision == 3 : # left[i] is occuluded
            # result[i] = 0
            i -= 1
        else:                     # right[j] is occuluded
            j -= 1
    #print(result)
    return result

def go():
    # bigSize = 512
    # smallSize = 256
    # drawRandom(bigSize, smallSize, 128, 124, 132)
    imgA = Image.open("/Users/chaozy/Desktop/CS/Algorithm/Coursework2/Stereo Pairs/Pair 2/view1.png")
    #imgA = Image.open("imgLeft.png")
    imgA = np.asarray(imgA)
    imgA = np.array([[rgbToIntensity(rgb) for rgb in rows] for rows in imgA])
    imgB = Image.open("/Users/chaozy/Desktop/CS/Algorithm/Coursework2/Stereo Pairs/Pair 2/view2.png")
    #imgB = Image.open("imgRight.png")
    imgB = np.asarray(imgB)
    imgB = np.array([[rgbToIntensity(rgb) for rgb in rows] for rows in imgB])

    bigSize = len(imgA)
    smallSize = len(imgA[0])
    disparityMatrix = np.array([[0 for i in range(smallSize)] for i in range(bigSize)])
    #disparityMatrix = np.array([[0 for i in range(bigSize)] for i in range(bigSize)])

    for i in range(bigSize):
            print(i)
            disparityMatrix[i] = backward(costMatrix(imgA[i], imgB[i]))

    img = Image.new('L', (smallSize, bigSize))
    img.putdata(np.reshape(disparityMatrix, smallSize * bigSize))

    #img.save("result1.png")
    img.show()

t1 = time.time()
go()
t2 = time.time()
print("time taken: ", t2 - t1)


