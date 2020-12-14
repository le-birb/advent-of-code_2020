
from itertools import count
from typing import List, Tuple

time = 1013728
# there's a .split(",") at the end of this one
input = "23,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,733,x,x,x,x,x,x,x,x,x,x,x,x,13,17,x,x,x,x,19,x,x,x,x,x,x,x,x,x,29,x,449,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,37".split(",")

# part 1: we don't care about x, just which bus is the best for us
table = {int(x): int(x) for x in filter(lambda c: c != "x", input)}

while any(t < time for t in table.values()):
    for bus_id in filter(lambda id: table[id] < time, table):
        table[bus_id] += bus_id

best_bus = 23

for bus_id in table:
    if table[bus_id] < table[best_bus]:
        best_bus = bus_id

print(best_bus * (table[best_bus] - time))

# part 2: now we care about the xes
bus_eqns = []
for i in range(len(input)):
    if input[i] == "x":
        continue
    else:
        bus_id = int(input[i])
        bus_eqns.append( (-i % bus_id, bus_id) )

# the bus list now is essentialy a list of conditions on the time t,
# where t = -i mod input[i]
# for every i that has a bus

# we can solve this system with the chinese remainder theorem
# essentially, go through the list and reduce a pair of equations
# t = a1 mod n1
# t = a2 mod n2
# to something like
# t = b mod n1*n2
# until you only have one left

def solve_mod_eqns(equations: List[Tuple[int]]):
    if len(equations) == 2:
        a, m = equations[0] # t = a mod m
        b, n = equations[1] # t = b mod n

        # these 2 equations define a linear system of equations over the integers:
        # t = jm + a
        # t = kn + b
        # which can be manipulated to get
        # t = a + mj
        # j = (nk + b - a)/m
        # so we just look for the first value j that is an integer that pops out for an integer k
        # (count() just spits out consecutive integers until you stop asking for them)
        j = next(filter(float.is_integer, map(lambda k: (n*k + b - a)/m, count())))
        t = a + m*j
        return (int(t), m*n)
    else:
        return solve_mod_eqns( [equations[0], solve_mod_eqns(equations[1:])] )

t, N = solve_mod_eqns(bus_eqns)

print(t)