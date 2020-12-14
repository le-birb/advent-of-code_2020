
import re
from itertools import product

class mem:
    def __init__(self, string: str):
        # grab from mem[address] = value
        address = int(re.search(r"(?<=\[)\d+(?=\])", string).group())
        value = int(string.split(" = ")[1])

        self.address = address
        self.value = value
    
    def __repr__(self):
        return "mem[%d] = %d".format(self.address, self.value)


class mask:
    def __init__(self, string: str):
        self.string = string.split(" = ")[1]
        self.rev_string = "".join([c for c in reversed(self.string)])
    
    def __repr__(self):
        return self.string


program = []

with open('day14-input', 'r') as f:
    for op in f:
        op = op.strip()
        if op.startswith("mem["):
            program.append(mem(op))

        elif op.startswith("mask"):
            program.append(mask(op))

        else:
            continue


# part 1: fairly straightforward masking of values before assignment
# the mask is split into 2: one to handle the 1s and the other to handle the 0s
one_mask = 0
zero_mask = 2**36-1

memory = [0]*2**16

for op in program:
    if isinstance(op, mem):
        memory[op.address] = op.value & zero_mask | one_mask

    elif isinstance(op, mask):
        one_mask = 0
        zero_mask = 2**36-1

        for i in range(len(op.rev_string)):
            m = op.rev_string[i]
            if m == "0":
                zero_mask ^= 2**i
            elif m == "1":
                one_mask ^= 2**i
            else:
                continue
        
print(sum(memory))

# part 2: weird address masking stuff
bit_vals = (0, 1)

def float_bits(bit_string: list):
    floating_bits = []
    for i in range(len(bit_string)):
        bit = bit_string[i]
        if bit == "X":
            floating_bits.append(i)
    
    for bit_combo in product(bit_vals, repeat = len(floating_bits)):
        floated_addr = bit_string
        for i in range(len(bit_combo)):
            floated_addr[floating_bits[i]] = bit_combo[i]
        # convert floated_addr back into an int
        floated_addr = int("".join(map(str, floated_addr)), base = 2) 
        yield floated_addr


def apply_mask(mask: mask, address: int) -> list:
    "Returns the list of addresses to assign to when mask is applied to address"
    # ensure address is 36 bits long
    bin_address = "{:0>36b}".format(address)
    masked_address = []

    for i in range(len(mask.string)):
        if mask.string[i] == "X":
            masked_address.append("X")

        elif mask.string[i] == "1" or mask.string[i] == "0":
            masked_address.append(int(bin_address[i]) | int(mask.string[i]))

    return [addr for addr in float_bits(masked_address)]


memory = {}
curr_mask = None

for op in program:
    if isinstance(op, mem):
        addresses = apply_mask(curr_mask, op.address)
        for address in addresses:
            memory[address] = op.value

    elif isinstance(op, mask):
        curr_mask = op

print(sum(memory.values()))