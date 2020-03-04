# a and b are the lengths of the str1 and str2 respectively
def editDistance(str1, str2, a, b):
    if a == 0:
        return b
    elif b == 0:
        return a

    elif str1[a - 1] == str2[b - 1]:
        return editDistance(str1, str2, a - 1, b - 1)

    else:
        return 1 + min(editDistance(str1, str2, a - 1, b), editDistance(str1, str2, a, b - 1), editDistance(str1, str2, a - 1, b - 1))

def editDistanceDP(str1, str2):
    m, n = len(str1), len(str2)
    arr = [[0 for i in range(m + 1)] for i in range(n + 1)]

    for row in range(n + 1):
        for col in range(m + 1):
            if row == 0:
                arr[row][col] = col
            elif col == 0:
                arr[row][col] = row

            elif str1[col - 1] == str2[row - 1]:
                arr[row][col] = arr[row - 1][col - 1]

            else:
                arr[row][col] = min(arr[row-1][col], arr[row][col-1], arr[row-1][col-1]) + 1

    return arr[n][m]
#
# str1 = [0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0]
# str2 = [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1]
#
# print(editDistanceDP(str1, str2))
# print(editDistanceDP([1,2, 3], [1,5 ,4]))