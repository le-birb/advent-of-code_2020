
groups = []
curr_group = []

with open('day6-input', 'r') as f:
    for line in f:
        line = line.strip()

        if line == "":
            # blank lines separate groups
            if curr_group:
                groups.append(curr_group)
                curr_group = []

        else:
            # store answers as a set because we're only interested in unique answers
            # and python will handle that for us with a set
            curr_group.append(set(line))

# catch a trailing group not followed by a newline at the end of the input
if curr_group:
    groups.append(curr_group)


# part 1: sum of the number of answers in each group
# we have a set of  from each person, so the union of each persons' answers will be the set of unique answers in a group

unique_answers = [set.union(*group) for group in groups]

print(sum(len(answers) for answers in unique_answers))


# part 2:
# now we want answers common to everybody, which is an intersection of sets this time

common_answers = [set.intersection(*group) for group in groups]

print(sum(len(yeses) for yeses in common_answers))