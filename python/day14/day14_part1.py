from collections import defaultdict

RUN_TEST = False
TEST_SOLUTION = 24
TEST_INPUT_FILE = "test_input_day_14.txt"
INPUT_FILE = "input_day_14.txt"

ARGS = []


class RegolithSimulator:
    def __init__(
        self, input_file: list[str], start_coord: tuple[int, int], part: int = 1
    ):
        self.input_file = input_file
        self.start_coord = start_coord
        self.symbols = {"rock": "#", "air": ".", "sand": "o", "sand_spawner": "+"}
        self.grid: defaultdict[tuple, str] = defaultdict(lambda: self.symbols["air"])
        self.max_x = 0
        self.min_x = float("inf")
        self.max_y = 0
        self.min_y = 0
        self.simulating = True
        self.parse_input()
        self.find_grid_bounds()
        if part == 2:
            # +1 instead of +2 since bound is already +1
            self.floor = self.max_y + 1
            self.max_y += 2
        else:
            self.floor = 0

    def swap(self, coord_a, coord_b):
        self.grid[coord_a], self.grid[coord_b] = self.grid[coord_b], self.grid[coord_a]

    def parse_input(self):
        """Parse input and map rocks to the grid"""
        for line in self.input_file:
            fillers = line.split(" -> ")
            from_coord = to_coord = empty = (None,)
            for filler in fillers:
                x, y = map(int, filler.split(","))
                if from_coord == empty:
                    from_coord = (x, y)
                    continue
                if to_coord == empty:
                    to_coord = (x, y)
                else:
                    from_coord = to_coord
                    to_coord = (x, y)
                if from_coord[0] == to_coord[0]:  # Iterate Y
                    if from_coord[1] < to_coord[1]:
                        for y in range(from_coord[1], to_coord[1] + 1):
                            self.grid[(from_coord[0], y)] = self.symbols["rock"]
                    else:
                        for y in range(to_coord[1], from_coord[1] + 1):
                            self.grid[(from_coord[0], y)] = self.symbols["rock"]
                else:  # Iterate X
                    if from_coord[0] < to_coord[0]:
                        for x in range(from_coord[0], to_coord[0] + 1):
                            self.grid[(x, from_coord[1])] = self.symbols["rock"]
                    else:
                        for x in range(to_coord[0], from_coord[0] + 1):
                            self.grid[(x, from_coord[1])] = self.symbols["rock"]

    def find_grid_bounds(self):
        """Find grid bounds"""
        for (x, y) in self.grid.keys():
            if x > self.max_x:
                self.max_x = x
            if x < self.min_x:
                self.min_x = x
            if y > self.max_y:
                self.max_y = y

    def is_in_bounds(self, coord: tuple[int, int]):
        """Check if coordinate is in bounds"""
        x, y = coord
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    def print_grid(self):
        """Print grid as a 2d structure"""
        symbol_backup = self.grid[self.start_coord]
        self.grid[self.start_coord] = self.symbols["sand_spawner"]
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                print(self.grid[(x, y)], end="")
            print()
        print()
        self.grid[self.start_coord] = symbol_backup

    def simulate(self):
        """Simulate sand falling until it falls off the grid"""
        while self.simulating:
            self.grid[self.start_coord] = self.symbols["sand"]
            active_location = self.start_coord
            while True:
                x, y = active_location
                if self.grid[(x, y + 1)] == self.symbols["air"]:
                    self.swap((x, y + 1), (x, y))
                    active_location = (x, y + 1)
                elif self.grid[(x - 1, y + 1)] == self.symbols["air"]:
                    self.swap((x - 1, y + 1), (x, y))
                    active_location = (x - 1, y + 1)
                elif self.grid[(x + 1, y + 1)] == self.symbols["air"]:
                    self.swap((x + 1, y + 1), (x, y))
                    active_location = (x + 1, y + 1)
                else:
                    # Done with this particular grain of sand
                    if active_location == self.start_coord:
                        self.simulating = False
                    break
                # Sand moved, check out of bounds or floor
                if self.floor and active_location[1] == self.floor:
                    # Hit the floor, done with this grain of sand
                    break
                if not self.floor and not self.is_in_bounds(active_location):
                    self.simulating = False
                    self.grid[active_location] = self.symbols["air"]
                    break

    def count_sand(self):
        """Count sand in grid"""
        return sum(1 for v in self.grid.values() if v == self.symbols["sand"])


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # Your scan traces the path of each solid rock structure and reports the
    # x,y coordinates that form the shape of the path, where x represents
    # distance to the right and y represents distance down.

    # The sand is pouring into the cave from point 500,0 (x,y).

    # Sand is produced one unit at a time, and the next unit of sand is not
    # produced until the previous unit of sand comes to rest. A unit of sand is
    # large enough to fill one tile of air in your scan.

    # A unit of sand always falls down one step if possible. If the tile
    # immediately below is blocked (by rock or sand), the unit of sand attempts
    # to instead move diagonally one step down and to the left. If that tile is
    # blocked, the unit of sand attempts to instead move diagonally one step
    # down and to the right. Sand keeps moving as long as it is able to do so,
    # at each step trying to move down, then down-left, then down-right. If all
    # three possible destinations are blocked, the unit of sand comes to rest
    # and no longer moves, at which point the next unit of sand is created back
    # at the source.

    # Using your scan, simulate the falling sand. How many units of sand come
    # to rest before sand starts flowing into the abyss below?

    start = (500, 0)
    regolith_sim = RegolithSimulator(lines, start)
    regolith_sim.print_grid()
    regolith_sim.simulate()
    regolith_sim.print_grid()

    solution = regolith_sim.count_sand()
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
