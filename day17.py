
from itertools import chain, product
from copy import deepcopy
from typing import Tuple

input = """\
#.#.##.#
#.####.#
...##...
#####.##
#....###
##..##..
#..####.
#...#.#."""

test_input = """\
.#.
..#
###"""

class coord_space:
    def __init__(self, center_val = None, default_val = False):
        self.pos_coords = []
        self.neg_coords = []
        self.default_val = deepcopy(default_val)
        if center_val is not None:
            self.pos_coords[0:] = [deepcopy(center_val)]
    
    def __repr__(self):
        elems = []
        for i in self.points():
            elems.append("{}: {}".format(i, repr(self[i])))
        return "[" + ", ".join(elems) + "]"
    
    def __str__(self):
        return str(list(reversed(self.neg_coords)) + self.pos_coords)
    
    def __iter__(self):
        return chain(reversed(self.neg_coords), self.pos_coords)

    def __getitem__(self, idx: int):
        if idx >= 0:
            if idx >= len(self.pos_coords):
                return self.default_val
            else:
                return self.pos_coords[idx]
        else:
            if -idx > len(self.neg_coords):
                return self.default_val
            else:
                return self.neg_coords[-idx-1]
    
    def __setitem__(self, idx: int, val):
        if idx >= 0:
            if idx >= len(self.pos_coords):
                ext_slice = slice(len(self.pos_coords), idx+1)
                extension = [deepcopy(self.default_val) for _ in range(ext_slice.stop - ext_slice.start)]
                self.pos_coords[ext_slice] = extension
            self.pos_coords[idx] = val
        else:
            if -idx > len(self.neg_coords):
                ext_slice = slice(len(self.neg_coords), -idx)
                extension = [deepcopy(self.default_val) for _ in range(ext_slice.stop - ext_slice.start)]
                self.neg_coords[ext_slice] = extension
            self.neg_coords[-idx-1] = val

    def get_bounds(self) -> Tuple[int, int]:
        if self.neg_coords:
            return -len(self.neg_coords), len(self.pos_coords)
        else:
            return 0, len(self.pos_coords)

    def points(self, extension = 0):
        return chain(range(-len(self.neg_coords) - extension, 0), range(len(self.pos_coords) + extension))


class conway3d:
    def __init__(self, init_string: str = ""):
        self.grid = coord_space(default_val = coord_space(default_val = coord_space(default_val = False)))
        lines = init_string.split("\n")
        for y in range(len(lines)):
            line = lines[y]
            for x in range(len(line)):
                self[x, y, 0] = line[x] == "#"

    def __str__(self):
        x_range, y_range, z_range = self.get_bounds()
        z_slices = []
        for z in z_range:

            rows = []
            for y in y_range:
                row_str = ""
                for x in x_range:
                    if self[x,y,z]:
                        row_str += "#"
                    else:
                        row_str += "."
                rows.append(row_str)

            z_slices.append("\n".join(["z={}".format(z)] + rows))
        
        return "\n\n".join(z_slices)

    def __repr__(self):
        return repr(self.grid)

    def __iter__(self):
        for y_coord in self.grid:
            for z_coord in y_coord:
                yield from z_coord
    
    def __getitem__(self, i: tuple):
        x, y, z = i
        return self.grid[x][y][z]
    
    def __setitem__(self, i: tuple, val):
        x, y, z = i
        if x not in self.grid.points():
            self.grid[x] = deepcopy(self.grid.default_val)
        if y not in self.grid[x].points():
            self.grid[x][y] = deepcopy(self.grid[x].default_val)
        self.grid[x][y][z] = val

    def get_bounds(self, extension = 0) -> Tuple[range, range, range]:
        x_min, x_max = self.grid.get_bounds()
        y_min = y_max = z_min = z_max = 0
        for x_coord in range(x_min, x_max):
            y_slice = self.grid[x_coord]
            y_low, y_high = y_slice.get_bounds()

            if y_low < y_min:
                y_min = y_low
            if y_high > y_max:
                y_max = y_high

            for y_coord in range(y_low, y_high):
                z_slice = self.grid[x_coord][y_coord]
                z_low, z_high = z_slice.get_bounds()

                if z_low < z_min:
                    z_min = z_low
                if z_high > z_max:
                    z_max = z_high

        return range(x_min - extension, x_max + extension), range(y_min - extension, y_max + extension), range(z_min - extension, z_max + extension)

    def cycle_cube(self, x, y, z):
        x_test = (x-1, x, x+1)
        y_test = (y-1, y, y+1)
        z_test = (z-1, z, z+1)
        test_coords = set(product(x_test, y_test, z_test))
        # remove (x, y, z) to not test the cube itself, only the surroundings
        test_coords.remove( (x, y, z) )
        adjacent_count = sum(self[x, y, z] for x, y, z, in test_coords)
        if self[x, y, z] and not 2 <= adjacent_count <= 3:
            return False
        elif not self[x, y, z] and adjacent_count == 3:
            return True
        else:
            return self[x,y,z]

    def step_simulation(self, count = 1):
        curr_state = self
        for _ in range(count):
            new_state = conway3d()
            x_range, y_range, z_range = curr_state.get_bounds(extension = 1)
            for x in x_range:
                for y in y_range:
                    for z in z_range:
                        new_val = curr_state.cycle_cube(x, y, z)
                        if new_val:
                            new_state[x,y,z] = new_val
            curr_state = new_state
        self.grid = curr_state.grid


# there's definitely a way to abstract the class above for n dimensions but I don't feel like doing that rn
class conway4d:
    def __init__(self, init_string: str = ""):
        self.grid = coord_space(default_val = coord_space(default_val = coord_space(default_val = coord_space(default_val = False))))
        lines = init_string.split("\n")
        for y in range(len(lines)):
            line = lines[y]
            for x in range(len(line)):
                self[x, y, 0, 0] = line[x] == "#"

    def __str__(self):
        x_range, y_range, z_range, w_range = self.get_bounds()
        z_slices = []
        for w, z in product(w_range, z_range):

            rows = []
            for y in y_range:
                row_str = ""
                for x in x_range:
                    if self[x,y,z,w]:
                        row_str += "#"
                    else:
                        row_str += "."
                rows.append(row_str)

            z_slices.append("\n".join(["z={}, w={}".format(z, w)] + rows))

        return "\n\n".join(z_slices)

    def __repr__(self):
        return repr(self.grid)

    def __iter__(self):
        for y_slice in self.grid:
            for z_slice in y_slice:
                for w_slice in z_slice:
                    yield from w_slice

    def __getitem__(self, i: tuple):
        x, y, z, w = i
        return self.grid[x][y][z][w]

    def __setitem__(self, i: tuple, val):
        x, y, z, w = i
        if x not in self.grid.points():
            self.grid[x] = coord_space(default_val = coord_space(default_val = coord_space()))
        if y not in self.grid[x].points():
            self.grid[x][y] = coord_space(default_val = coord_space())
        if z not in self.grid[x][y].points():
            self.grid[x][y][z] = coord_space()
        self.grid[x][y][z][w] = val

    def get_bounds(self, extension = 0) -> Tuple[range, range, range, range]:
        x_min, x_max = self.grid.get_bounds()
        y_min = y_max = z_min = z_max = w_min = w_max = 0
        for x_coord in range(x_min, x_max):
            y_slice = self.grid[x_coord]
            y_low, y_high = y_slice.get_bounds()

            if y_low < y_min:
                y_min = y_low
            if y_high > y_max:
                y_max = y_high

            for y_coord in range(y_low, y_high):
                z_slice = self.grid[x_coord][y_coord]
                z_low, z_high = z_slice.get_bounds()

                if z_low < z_min:
                    z_min = z_low
                if z_high > z_max:
                    z_max = z_high

                for z_coord in range(z_low, z_high):
                    w_slice = self.grid[x_coord][y_coord][z_coord]
                    w_low, w_high = w_slice.get_bounds()

                    if w_low < w_min:
                        w_min = w_low
                    if w_high > w_max:
                        w_max = w_high

        return range(x_min - extension, x_max + extension), range(y_min - extension, y_max + extension),\
            range(z_min - extension, z_max + extension), range(w_min - extension, w_max + extension)

    def cycle_cube(self, x, y, z, w):
        x_test = (x-1, x, x+1)
        y_test = (y-1, y, y+1)
        z_test = (z-1, z, z+1)
        w_test = (w-1, w, w+1)
        test_coords = set(product(x_test, y_test, z_test, w_test))
        # remove (x, y, z) to not test the cube itself, only the surroundings
        test_coords.remove( (x, y, z, w) )
        adjacent_count = sum(self[x, y, z, w] for x, y, z, w in test_coords)
        if self[x, y, z, w] and not 2 <= adjacent_count <= 3:
            return False
        elif not self[x, y, z, w] and adjacent_count == 3:
            return True
        else:
            return self[x, y, z, w]

    def step_simulation(self, count = 1):
        curr_state = self
        for _ in range(count):
            new_state = conway4d()
            x_range, y_range, z_range, w_range = curr_state.get_bounds(extension = 1)
            for w in w_range:
                for z in z_range:
                    for y in y_range:
                        for x in x_range:
                            new_val = curr_state.cycle_cube(x, y, z, w)
                            if new_val:
                                new_state[x,y,z,w] = new_val
            curr_state = new_state
        self.grid = curr_state.grid


# c = coord_space()
# for i in range(-3, 9):
#     c[i] = i

# test = conway3d(test_input)
# test.step_simulation(6)

# print(sum(test))

# test = conway4d(test_input)
# test.step_simulation(6)

# print(sum(test))


part_1 = conway3d(input)
part_1.step_simulation(6)

print(sum(part_1))


part_2 = conway4d(input)
part_2.step_simulation(6)

print(sum(part_2))