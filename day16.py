
from itertools import takewhile
from typing import Dict, Set, Tuple
from math import prod

fields: Dict[str, Tuple[Tuple[int]]] = {}

your_ticket: Tuple[int] = ()

nearby_tickets: Set[Tuple[int]] = set()

with open('day16-input', 'r') as f:
    for line in takewhile(lambda l: not l.startswith("your ticket:"), f):
        line = line.strip()
        if line == "":
            continue

        field, ranges = line.split(": ")
        ranges = ranges.split(" or ")
        ranges = tuple(tuple(int(n) for n in r.split("-")) for r in ranges)

        fields.update({field: ranges})

    your_ticket = tuple(int(n) for n in next(f).strip().split(","))
    
    for line in f:
        line = line.strip()
        if line == "" or line.startswith("nearby tickets:"):
            continue

        nearby_tickets.add(tuple(int(n) for n in line.split(",")))


def in_range(n, low, high) -> bool:
    return low <= n <= high

def in_ranges(n, ranges) -> bool:
    return any(in_range(n, *r) for r in ranges)


# part 1: find invalid entries on nearby tickets

invalid_nums = []
invalid_tickets = set()

for ticket in nearby_tickets:
    for num in ticket:
        if not any(in_ranges(num, range_set) for range_set in fields.values()):
            invalid_nums.append(num)
            invalid_tickets.add(ticket)

print(sum(invalid_nums))


# part 2: with the valid tickets, find which field goes to what column
valid_tickets = nearby_tickets - invalid_tickets

fields_to_search = set(fields.keys())
indices_to_search = set(range(len(fields_to_search)))

field_map: Dict[str, int] = {}

# rearrange the tickest into lists of numbers by index (column), for later
nums_by_index = [set(ticket[i] for ticket in valid_tickets) for i in range(len(your_ticket))]

# this one'll be tricky
# since some indices might match multiple fields at first, we're gonna need to go through multiple times
# and keep pruning away definite matches only until all are matched up
while fields_to_search:
    # have to make a copy here so that removing an index doesn't throw an error
    for i in indices_to_search.copy():
        nums = nums_by_index[i]
        matching_fields = []
        for field in fields_to_search:
            ranges = fields[field]
            if all(in_ranges(num, ranges) for num in nums):
                # this index and field pairing is a possible match, however it might just be coincidence that they line up
                # just store the field for now and keep going
                matching_fields.append(field)

        # only if there was only one matching field for an index do we know for sure that they match
        # if that's the case, record the match and remove both the index and the field from searching
        if len(matching_fields) == 1:
            field = matching_fields[0]
            field_map[field] = i
            fields_to_search.remove(field)
            indices_to_search.remove(i)

indices_of_interest = set(field_map[f] for f in filter(lambda k: k.startswith("departure"), fields.keys()))

print(prod(your_ticket[i] for i in indices_of_interest))