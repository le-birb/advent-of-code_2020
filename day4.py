
import re

passports = []

with open('day4-input', 'r') as f:
    curr_passport = {}
    for line in f:
        if line.strip() == "":
            # a passport has ended
            passports.append(curr_passport)
            curr_passport = {}
        else:
            entries = line.strip().split(' ')
            for entry in entries:
                key, value = entry.split(":")
                curr_passport.update({key: value})

# if the file ends without a blank line, add the alst passport that would be missed
if curr_passport:
    passports.append(curr_passport)


# part 1
required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

valid_passports = 0

for passport in passports:
    # just check if the required fields exist in the passport
    if all(field in passport for field in required_fields):
        valid_passports += 1

print(valid_passports)


# part 2
valid_passports = 0

for passport in passports:
    # now we need to do some validation
    # my strategy here is to do a bunch of checks to eliminate bad data
    # so anything that makes it through must still be valid

    if not all(field in passport for field in required_fields):
        # not all required fields are present: invalid
        continue

    if not 1920 <= int(passport['byr']) <= 2002:
        # birth year out of range
        continue

    if not 2010 <= int(passport['iyr']) <= 2020:
        # issue year out of range
        continue

    if not 2020 <= int(passport['eyr']) <= 2030:
        # expiration year out of range
        continue
    
    # handle all of the years
    # try:
    #     if not 1920 <= int(passport['byr']) <= 2002:
    #         # birth year out of range
    #         continue

    #     if not 2010 <= int(passport['iyr']) <= 2020:
    #         # issue year out of range
    #         continue

    #     if not 2020 <= int(passport['eyr']) <= 2030:
    #         # expiration year out of range
    #         continue

    # except ValueError:
    #     # entry was not a number, therefore invalid
    #     continue

    # now take a look at height
    height = passport['hgt']

    # split for cm and in heights
    if height.endswith("in"):
        height_num = height[:-2]
        if not (height_num.isdigit() and 59 <= int(height_num) <= 76):
            # height is not a number or isn't in range
            continue

    elif height.endswith("cm"):
        height_num = height[:-2]
        if not (height_num.isdigit() and 150 <= int(height_num) <= 193):
            # height is not a number or isn't in range
            continue

    else:
        # does not end in in or cm; invalid
        continue

    # hair color: must be a 6-digit hex code #xxxxxx
    if not re.match(r'#[0-9a-f]{6}$', passport['hcl']):
        continue

    # eye color: only certain values are acceptable
    if not passport['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        continue

    # passport id must be a 9-digit number
    if not re.match(r'\d{9}$', passport['pid']):
        continue

    # if it made it this far, teh passport has all required fields and all are valid
    valid_passports += 1


print(valid_passports)