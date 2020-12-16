
from itertools import islice

input = [9, 6, 0, 10, 18, 2, 1]

test_input = [0, 3, 6]

# an iterator that spits out consecutive numbers from the game as long as you want it to
def memory_game(starting_list):
    said_numbers = {}
    current_turn = 0

    last_num = None

    for number in starting_list:
        if last_num is not None:
            said_numbers.update({last_num: current_turn})
            yield last_num
        current_turn += 1
        last_num = number

    while True:
        if last_num in said_numbers:
            next_num = current_turn - said_numbers[last_num]
        else:
            next_num = 0
        
        said_numbers.update({last_num: current_turn})
        yield last_num
        current_turn += 1
        last_num = next_num


# testing out my iterator
# for num in islice(memory_game(test_input), 10):
#     print(num)

# part 1: get the 2020th number starting with input
num = next(islice(memory_game(input), 2019, None))
print(num)


# part 2: get the 30,000,000th number, takes a bit (~15 secs on my machine)
num = next(islice(memory_game(input), 30000000-1, None))
print(num)