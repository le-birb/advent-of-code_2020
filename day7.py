
import re

# hold all bag rules as a dictionary of the form
# color: [requirements]
bag_map = {}

def trim_bag(bag_color: str) -> str:
    "Removes a trailing 'bag' or 'bags', along with any whitespace left over."
    return re.sub("\s*bags?\s*\.?$", "", bag_color)


with open('day7-input', 'r') as f:
    for line in f:
        line = line.strip()
        bag, req_string = line.split(" contain ")
        bag = trim_bag(bag)

        if req_string == "no other bags.":
            bag_map.update({bag: []})

        else:
            req_strings = req_string.split(", ")
            requirements = []
            for req_string in req_strings:
                count, color = req_string.split(' ', 1)
                requirements += [trim_bag(color)] * int(count)
            
            bag_map.update({bag: requirements})


def containing_bags(bag_color):
    for bag in bag_map:
        if bag_color in bag_map[bag]:
            yield bag


already_counted_bags = []

def no_repeats(bag):
    return not bag in already_counted_bags

# part 1: how many bags can hold a shiny gold bag?

def count_containers(my_bag):
    already_counted_bags.append(my_bag)
    # filter out repeats because if e.g. a red bag holds both a blue and a green bag, each of which can hold our shiny gold bag,
    # we only want to count the red bag (and any that might hold it) once 
    containers = [bag for bag in filter(no_repeats, containing_bags(my_bag))]
    return len(containers) + sum(count_containers(bag) for bag in containers)

our_bag = "shiny gold"

print(count_containers(our_bag))

# part 2: how many bags does our bag need to hold?

def count_contained(my_bag):
    return len(bag_map[my_bag]) + sum(count_contained(bag) for bag in bag_map[my_bag])

print(count_contained(our_bag))