from RandomMatch import drawRandom
from PIL import Image
import numpy as np

def matchCost(left, right):
    z = (left + right) / 2
    return ((z - left) * (z - right)) / 2

def desparity(left, right):
    return abs(left - right)

def costMatrix(left, right, size):
    costOfOcclusion = 3.8
    occludedPixel = 0
    arr = [[0 for i in range(size + 1)] for i in range(size + 1)]
    desparityArray = [0 for i in range(size )]

    for i in range(1, size):
        arr[i][0] = i * costOfOcclusion
        arr[0][i] = i * costOfOcclusion

    for i in range(1, size ):
        for j in range(1, size):
            arr[i][j] = min(arr[i-1][j-1] + matchCost(left[i], right[j]), arr[i][j-1] + costOfOcclusion, arr[i-1][j] + costOfOcclusion)

            if arr[i][j] == arr[i-1][j-1] + matchCost(left[i], right[j]):
                if i != j:
                    desparityArray[i], desparityArray[j] = 255, 255

            elif arr[i][j] == arr[i][j - 1] + costOfOcclusion:
                desparityArray[j] = 122
            else:
                desparityArray[i] = 122

    return desparityArray

def go():
    bigSize = 512
    smallSize = 256
    drawRandom(bigSize, smallSize, 128, 124, 132)
    imgA = Image.open("imgLeft.png")
    imgA = np.asarray(imgA)
    imgB = Image.open("imgRight.png")
    imgB = np.asarray(imgB)

    disparityMatrix = np.array([[0 for i in range(bigSize)] for i in range(bigSize)])
    print(len(disparityMatrix[0]))
    for i in range(len(imgA)):
        if np.any(imgA[i] != imgB[i]):
            print(i)
            disparityMatrix[i] = costMatrix(imgA[i], imgB[i], bigSize )
        else:  # for the common area
            disparityMatrix[i] = [0 for i in range(bigSize)]
    print(disparityMatrix)
    img = Image.new('L', (bigSize, bigSize))
    img.putdata(np.reshape(disparityMatrix, bigSize * bigSize))
    img.save("result.png")
    img.show()
    print()
go()


