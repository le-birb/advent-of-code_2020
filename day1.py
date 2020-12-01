
from itertools import product
from math import prod as multiply
from typing import Iterable, Union

infile = open('day1-input', 'r')

# our report is a list of all of the numbers in the file, with line breaks removed
report = [int(line.strip()) for line in infile]

infile.close()


# part 1
# I iterate through the cartesian product of the report with itself,
# which is to say, I iterate through every possible pairing of a number
# another in the report, and check that they sum to 2020, if so, return
# their (arithmetic) product and exit the loop
for pair in product(report, repeat = 2):
    if sum(pair) == 2020:
        print(multiply(pair))
        break

# part 2
# same as part 1 but with 3 copies of report
for trio in product(report, repeat = 3):
    if sum(trio) == 2020:
        print(multiply(trio))
        break


# for fun, here's a function that'll do the above for any number of elements n
def tuple_sum_to(l: Iterable, n: int, target) -> Union[tuple, None]:
    for t in product(l, repeat = n):
        if sum(t) == target:
            return t

# the solutions using this function would look like:

multiply(tuple_sum_to(report, n = 2, target = 2020))
multiply(tuple_sum_to(report, n = 3, target = 2020))