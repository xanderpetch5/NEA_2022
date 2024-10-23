import math


def get_hash(arr):
    result = []
    for value in arr:
        temp = int(value * 5)
        if temp == 5: temp = 4
        result.append(temp)
    print(result)
    result.reverse()
    result2 = 0
    for count, value in enumerate(result):
        result2 += value * (5 ** count)
    return result2



def find_neighbours(value, n):
    neighbours = {value}
    for nth_neighbour in range(n):
        new_neighbours = set()
        for neighbour in neighbours:
            for i in range(10):
                low_neighbour = neighbour + (5 ** i)
                high_neighbour = neighbour - (5 ** i)
                if low_neighbour not in new_neighbours: new_neighbours.add(low_neighbour)
                if high_neighbour not in new_neighbours:new_neighbours.add(high_neighbour)
        neighbours = new_neighbours
    neighbours = sorted(neighbours)
    return neighbours


def reverse(n):
    digits = []
    while n > 0:
        remainder = n % 5
        digits.append(int(remainder))
        n //= 5
    while len(digits) < 10:
        digits.append(0)
    digits.reverse()
    return digits


def find_distance(hash1, hash2):
    arr1 = reverse(hash1)
    arr2 = reverse(hash2)
    distance = 0
    for i in range(10):
        distance += (abs(abs(arr1[i]) - abs(arr2[i]))) ** 2
    distance = math.sqrt(distance)
    similar = (4 * math.sqrt(10) - distance) / (4 * math.sqrt(10))
    return distance, similar



