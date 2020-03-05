from RandomMatch import drawRandom
from PIL import Image
import numpy as np
from matplotlib import pyplot as PLT

def matchCost(left, right):
    z = (int(left) + int(right)) / 2
    result = ((z - left) * (z - right)) / 2
    return abs(result)

def disparity(left, right):
    return abs(left - right)

def costMatrix(left, right, size):
    costOfOcclusion = 3.8
    occludedPixel = 0
    arr = [[0 for i in range(size + 1)] for i in range(size + 1)]
    steps = []
    for i in range(1, size):
        arr[i][0] = i * costOfOcclusion
        arr[0][i] = i * costOfOcclusion

    for i in range(1, size):
        currentSteps = []
        for j in range(1, size):
            #print(left[i], " ", right[j], "  " , matchCost(left[i], right[j]))
            arr[i][j] = min(arr[i-1][j-1] + matchCost(left[i], right[j]), arr[i][j-1] + costOfOcclusion, arr[i-1][j] + costOfOcclusion)

            if arr[i][j] == arr[i-1][j-1] + matchCost(left[i], right[j]):

                currentSteps.append([-1, -1])
            elif arr[i][j] == arr[i][j - 1] + costOfOcclusion:
                currentSteps.append([0, -1])
            else:
                currentSteps.append([-1, 0])
        steps.append(currentSteps)
    #print(steps)
    return steps

def backward(decisions):
    i = j = len(decisions) - 1
    result = [[0, 0, 0] for i in range(len(decisions) + 1)]
    while (i >= 0 and j >= 0):
        last_decision = decisions[i][j]
        #print(last_decision)
        if last_decision[0] == -1 and last_decision[1] == -1: # matched case
            if i != j:
                #result[i] = result[j] = disparity(i, j) * 128
                result[i] = result[j] = [255, 255, 255]
            # else:
            #     result[i] = 0
            i -= 1
            j -= 1

        elif last_decision[0] == -1 and last_decision[1] == 0: # left[i] is occuluded
            result[i] = [0, 0, 255]
            i -= 1
        else:                                 # right[j] is occuluded
            result[j] = [0, 0, 255]
            j -= 1
    return result

def go():
    bigSize = 512
    smallSize = 256
    drawRandom(bigSize, smallSize, 128, 124, 132)
    imgA = Image.open("imgLeft.png")
    imgA = np.asarray(imgA)
    imgB = Image.open("imgRight.png")
    imgB = np.asarray(imgB)


    disparityMatrix = np.array([[[0,0,0] for i in range(bigSize)] for i in range(bigSize)])
    for i in range(len(imgA)):
        if np.any(imgA[i] != imgB[i]):
            print(i)
            #print(imgA[i][90:], imgB[i][90:])
            disparityMatrix[i] = backward(costMatrix(imgA[i], imgB[i], bigSize))
        # else:  # for the common area
        #     disparityMatrix[i] = [[0, 0, 0] for i in range(bigSize)]
    print(disparityMatrix.shape)
    # img = Image.new('L', (bigSize, bigSize))
    # img.putdata(np.reshape(disparityMatrix, bigSize * bigSize))
    # disparityMatrix = np.ndarray.flatten(disparityMatrix)
    # for i in disparityMatrix:
    #     print(i)
    #img = Image.fromarray(disparityMatrix, 'L')
    # img = Image.new('RGB', (bigSize, bigSize))
    #     # img.putdata(np.reshape(disparityMatrix, bigSize * bigSize))

    # img.save("result.png")
    # img.show()
    PLT.imshow(disparityMatrix)
    PLT.show()
    print()
go()


