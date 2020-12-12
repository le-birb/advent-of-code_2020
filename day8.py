
from enum import Enum

# define a bunch of classes
# the basic purpose of these is to consolidate the repeat call checking to just the base class instruction

class instruction(Enum):
    nop = "nop"
    accumulate = "acc"
    jump = "jmp"

    def __repr__(self):
        return self.value


instruction_list = []

with open('day8-input', 'r') as f:
    for line in f:
        line = line.strip()
        inst, arg = line.split(" ")

        instruction_list.append( (instruction(inst), int(arg)) )


accumulator = 0
instruction_pointer = 0

past_pointer_vals = set()

# part 1: run code, get accumulator value just before first loop

while True:
    if instruction_pointer in past_pointer_vals:
        print(accumulator)
        break
    else:
        past_pointer_vals.add(instruction_pointer)

    inst, arg = instruction_list[instruction_pointer]
    if inst == instruction.nop:
        pass
    elif inst == instruction.accumulate:
        accumulator += arg
    elif inst == instruction.jump:
        instruction_pointer += arg
        # skip the pointer increment
        continue

    instruction_pointer += 1


# part 2: now we need to do some funky instruction replacements

# first, a function to test each replacement
def exec(instruction_list) -> int:
    instruction_pointer = 0
    accumulator = 0

    past_pointer_vals = set()

    while True:
        if instruction_pointer in past_pointer_vals:
            return None
        elif instruction_pointer >= len(instruction_list):
            return accumulator
        else:
            past_pointer_vals.add(instruction_pointer)

        inst, arg = instruction_list[instruction_pointer]
        if inst == instruction.nop:
            pass
        elif inst == instruction.accumulate:
            accumulator += arg
        elif inst == instruction.jump:
            instruction_pointer += arg
            # skip the pointer increment
            continue

        instruction_pointer += 1

# now a function to switch a nop to a jump or vice versa:
def switch_op(op: instruction) -> instruction:
    if op == instruction.nop:
        return instruction.jump
    else:
        return instruction.nop

# and a generator for instruction lists with one instruction switched each
def instruction_switches(instruction_list):
    for i in range(len(instruction_list)):
        inst, val = instruction_list[i]
        if inst == instruction.jump or inst == instruction.nop:
            yield instruction_list[:i] + [(switch_op(inst), val)] + instruction_list[i+1:]

for program in instruction_switches(instruction_list):
    result = exec(program)
    if result is not None:
        print(result)
        break