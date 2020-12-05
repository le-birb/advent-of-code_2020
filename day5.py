

# this challenege essentially encodes each seat location as a binary number, with the first
# 7 digits giving the row, and the last 3 the column of the seat
seat_map = {'F': '0', 'B': '1', 'L': '0', 'R': '1'}

seat_codes = []

with open('day5-input', 'r') as f:
    for line in f:
        # store code as a string for easy appending
        seat_code = ''
        for character in line.strip():
            seat_code += seat_map[character]

        seat_codes.append(int(seat_code, 2))

# part 1, just getting the maximum number
print(max(seat_codes))

# part 2

last_num = None
second_to_last_num_in_list = False
last_num_in_list = False

for num in range(2**10):
    num_in_list = num in seat_codes

    # searching for a situation like:
    # 459 <- second to last num
    # 461 <- num
    # to return 460 <- last num
    if not last_num_in_list and num_in_list and second_to_last_num_in_list:
        print(last_num)
        break

    last_num = num
    second_to_last_num_in_list = last_num_in_list
    last_num_in_list = num_in_list