
from itertools import combinations, accumulate, islice

data = []

with open('day9-input', 'r') as f:
    for line in f:
        data.append(int(line))

preamble = 25

# part 1: find the first number which cannot be formed as a sum of the previous preamble numbers
invalid_num = 0

for i in range(preamble, len(data)):
    prev_slice = data[i-preamble:i]

    for pair in combinations(prev_slice, 2):
        if sum(pair) == data[i]:
            break
    else:
        invalid_num = data[i]
        break

print(invalid_num)


# part 2: now that we have the invalid number, find a contiguous set of numbers that add up to it

weakness = None

for i in range(len(data)):
    for j in range(i+1, len(data)):
        data_slice = data[i:j+1]
        s = sum(data_slice)

        if s == invalid_num:
            weakness = min(data_slice) + max(data_slice)
            break

        elif s > invalid_num:
            break

    if weakness:
        break

print(weakness)