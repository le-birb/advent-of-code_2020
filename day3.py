
from math import prod as mult

from itertools import zip_longest

infile = open('day3-input', 'r')

trees = [[c == '#' for c in line.strip()] for line in infile]

infile.close()

height = len(trees)
width = len(trees[0])

def count_trees(right, down):
    tree_count = 0

    for i in range(0, height//down):
        tree_count += trees[down*i][(right*i) % width]
    
    return tree_count


# part 1
right= 3
down = 1

print(count_trees(right, down))


# part 2
rights = [1, 3, 5, 7, 1]
downs  = [1, 1, 1, 1, 2]

slopes = zip_longest(rights, downs)

print(mult(count_trees(*slope) for slope in slopes))