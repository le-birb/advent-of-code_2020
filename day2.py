
f = open('day2-input', 'r')

passwords = [line.strip() for line in f]

f.close()

# part 1
valid_count = 0

for line in passwords:
    rule, password = line.split(": ")
    nums, letter = rule.split(' ')
    low, high = nums.split('-')
    low = int(low)
    high = int(high)

    if low <= password.count(letter) <= high:
        valid_count = valid_count + 1

print(valid_count)


# part 2
def xor(a, b):
    return (a and not b) or (not a and b)

valid_count = 0

for line in passwords:
    rule, password = line.split(": ")
    nums, letter = rule.split(' ')
    low, high = nums.split('-')
    low = int(low)
    high = int(high)

    if xor(password[low-1] == letter, password[high-1] == letter):
        valid_count = valid_count + 1

print(valid_count)