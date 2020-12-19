
import re
from typing import Iterator

def remove_whitespace(string: str) -> str:
    return re.sub(r"\s", "", string)

def skip_parentheses(s: Iterator[str]):
    offset = 0
    for c in s:
        if c == ")":
            offset += skip_parentheses(s)
        elif c == "(":
            return offset + 1
        offset += 1
    return offset


def eval_string(string: str, advanced = False):
    # no whitespace has meaning, and it's easier to parse if we remove it
    string = remove_whitespace(string)
    operator = ""
    curr_pos = -1
    op_pos = curr_pos
    # go through the string backwards for left-to-right evaluation
    # so 1 + 2 * 3 will find
    # 1 + 2 op* 3 = (1 + 2) * 3
    str_iter = iter(reversed(string))
    for c in str_iter:
        if c == "*" or c == "+":
            if advanced:
                # in advanced mode, addition always goes first
                # so if the operator is addition, keep going (don't break) to see if a multiplication happens
                # we want to find multiplications first since that will make additions be evaluated first
                # 1 + 2 * 3 + 4 -> (1 + 2) * (3 + 4) if you split from the multiplication first vs.
                # 1 + 2 * 3 + 4 -> (((1 + 2) * 3) + 4) if you treat them equally

                # if it's a plus and operator is empty that means it's the first plus, so we keep it
                # otherwise, we've already seen a plus so skip
                if operator == "" and c == "+":
                    operator = c
                    op_pos = curr_pos
                elif c == "*":
                    operator = c
                    op_pos = curr_pos
                    break
            else:
                operator = c
                # store the position here so we know where to find the right one later
                op_pos = curr_pos
                break
        elif c == ")":
            # if we hit parentheses, just skip right by them
            # we don't care what's in them yet, we'll hit that later
            curr_pos -= skip_parentheses(str_iter)
        curr_pos -= 1

    if operator == "+":
        # use the stored position here to split the string at the operator we want to evaulate here
        # str.split() only goes from the beginning, so it won't work for e.g. 4 * (2 + 3) + 4, where it would make
        # 4 * (2, 3) + 4, making 2 invalid expressions from a split we don't want right now
        l, r = string[:op_pos], string[op_pos+1:]
        return eval_string(l, advanced) + eval_string(r, advanced)
    elif operator == "*":
        # same as above
        l, r = string[:op_pos], string[op_pos+1:]
        return eval_string(l, advanced) * eval_string(r, advanced)

    elif operator == "":
        # this is the no operator found case
        # so we either have a number or a parentheses expression

        # number
        if re.fullmatch(r"\d+", string):
            return int(string)

        # stuff in parentheses
        elif re.fullmatch(r"\(.*\)", string):
            # pass in the string minus the parentheses
            return eval_string(string[1:-1], advanced)
    else:
        return None

# tests = """1 + (2 * 3) + (4 * (5 + 6))
# 2 * 3 + (4 * 5)
# 5 + (8 * 3 + 9 + 3 * 4 * 3)
# 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
# ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

# for test in tests.split("\n"):
#     print(eval_string(test, advanced = True))


with open('day18-input', "r") as f:
    equations = [line for line in f]

# part 1: evaluate all of the basic problems and print the sum of the results
print(sum(eval_string(eqn) for eqn in equations))


# part 2: now do the advanced
print(sum(eval_string(eqn, advanced = True) for eqn in equations))