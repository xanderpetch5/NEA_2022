def get_hash(arr):
    result = []
    for value in arr:
        temp = int(value * 5)
        if temp == 5: temp = 4
        result.append(temp)
    result2 = 0
    result.reverse()
    for count, value in enumerate(result):
        result2 += value * (5 ** count)
    return result2


def find_neighbours(value):
    neighbours = []
    for i in range(0, 11):
        low_neighbour = value + 5 ** i
        high_neighbour = value - 5 ** i
        neighbours.append(low_neighbour)
        neighbours.append(high_neighbour)
    return neighbours


def reverse(n):
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        remainder = n % 5
        digits.append(str(remainder))
        n //= 5
    digits.reverse()
    return digits


def find_distance(arr1, arr2):
    difference_arr = []
    for i in range(0, len(arr1)):
        difference_arr.append(abs(abs(arr1[i]) - abs(arr2[i])))
    return difference_arr
