from PIL import Image
import numpy as np

def RandMatGenerator(size):
    arr = np.random.randint(0, 2, (size, size))
    for i in range (size):
        for j in range(size):
            if arr[i][j] == 1:
                arr[i][j] = 255
    return arr

def drawRandom(bigSize, smallSize, startRow, colA, colB):
    matA = RandMatGenerator(bigSize)
    matB = np.copy(matA)
    matC = RandMatGenerator(smallSize)

    matA[startRow: startRow + smallSize, colA : colA + smallSize] = matC
    matB[startRow: startRow + smallSize, colB : colB + smallSize] = matC

    imgLeft = Image.new('L', (bigSize, bigSize))
    imgLeft.putdata(np.reshape(matA, bigSize * bigSize))
    imgRight = Image.new('L', (bigSize, bigSize))
    imgRight.putdata(np.reshape(matB, bigSize * bigSize))
    imgLeft.save("imgLeft.png")
    imgRight.save("imgRight.png")

    return (matA, matB)