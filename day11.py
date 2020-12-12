
from itertools import count, product, takewhile, filterfalse

class seat_grid(list):

    tolerance = 4

    def __init__(self, score_method = "default"):
        super().__init__()
        self.score_method = score_method

    def copy(self):
        new_grid = seat_grid()
        new_grid[:] = self[:]
        return new_grid

    def in_bounds(self, row, col):
        return 0 <= row < len(self) and 0 <= col < len(self[row])

    def is_occupied(self, row, col):
        if not self.in_bounds(row, col):
            # the given position is outside the grid, and cannot be sat upon
            return False
        
        return self[row][col] == "#"

    def get_score(self, row, col):
        if self.score_method == "part 2":
            return self.get_score_2(row, col)
        else:
            return self.get_score_1(row, col)

    # function for part 1
    def get_score_1(self, row, col):
        # check the area round the seat but not the seat itself
        checks = [seat for seat in product([row-1, row, row+1], [col-1, col, col+1])]
        checks.remove( (row, col) )
        return sum(self.is_occupied(*seat) for seat in checks)
    
    # function for part 2
    def get_score_2(self, row, col):
        # check the area round the seat but not the seat itself
        diags = [direction for direction in product([-1, 0, 1], repeat = 2)]
        diags.remove( (0, 0) )
        return sum(self.check_diagonal(row, col, direction) for direction in diags)

    def is_floor(self, row, col):
        return self.in_bounds(row, col) and self[row][col] == "."

    def check_diagonal(self, row, col, direction):
        rows = count(row+direction[0], direction[0])
        cols = count(col+direction[1], direction[1])
        # pull only non-floor seats that are in-bounds
        checks = filterfalse(lambda seat: self.is_floor(*seat), takewhile(lambda p: self.in_bounds(*p), zip(rows, cols)))
        # check only the first such place, or if none exists, return false
        return next(map(lambda seat: self.is_occupied(*seat), checks), False)

    def iterate_spot(self, row, col):
        spot = self[row][col]
        if spot == ".":
            return "."
        
        score = self.get_score(row, col)
        if spot == "L" and score == 0:
            return "#"
        elif spot == "#" and score >= seat_grid.tolerance:
            return "L"
        else:
            return spot

    def iterate(self):
        new_grid = seat_grid(self.score_method)
        for row in range(len(self)):
            new_grid.append([])
            for col in range(len(self[row])):
                new_grid[row].append(self.iterate_spot(row, col))
        
        return new_grid

    def simulate(self):
        counter = 0
        while counter < 10000:
            new_grid = self.iterate()
            if new_grid == self:
                break
            else:
                self[:] = new_grid[:]
            
            counter += 1

    def count_occupied(self):
        return sum(row.count("#") for row in self)


grid = seat_grid()
with open('day11-input', 'r') as f:
    for line in f:
        grid.append(list(line.strip()))



# part 1: simple rules
grid_1 = grid.copy()
grid_1.simulate()
print(grid_1.count_occupied())


# part 2: more tolerant people, but they can see farther
seat_grid.tolerance = 5

grid_2 = grid.copy()

grid_2.score_method = "part 2"

grid_2.simulate()
print(grid_2.count_occupied())