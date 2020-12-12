
from itertools import tee, takewhile, count
from math import prod

adapters = [0]

with open('day10-input', 'r') as f:
    for line in f:
        adapters.append(int(line))

adapters.sort()

# add in the laptop
adapters.append(adapters[-1] + 3)

# convenience function to get consecutive pairs grouped together
def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

# part 1: get the differences between consecutive links

differences = []

for link in pairwise(adapters):
    differences.append(link[1] - link[0])

print(differences.count(1) * differences.count(3))


# part 2: how many possible arrangements are there?

# a lookup table to store 
chains_from_idx = {}

def count_valid_chains(adapter_list, start_idx):
    # avoid computing a number we already know
    if start_idx in chains_from_idx:
        return chains_from_idx[start_idx]

    jolts = adapter_list[start_idx]
    next_links = list(takewhile(
        lambda x: x < len(adapter_list) and adapter_list[x] - jolts <= 3,
        count(start_idx + 1)))
    if next_links:
        possibilities = sum(count_valid_chains(adapter_list, link_idx) for link_idx in next_links)
    else:
        possibilities = 1
    # store this now known result to use later
    chains_from_idx[start_idx] = possibilities
    return possibilities

print(count_valid_chains(adapters, 0))