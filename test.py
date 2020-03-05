def matchCost(left, right):
    z = (left + right) / 2
    result = ((z - left) * (z - right)) / 2
    return abs(result)
print(matchCost(0, 255))