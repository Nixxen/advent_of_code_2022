from colors import colors

RUN_TEST = False
TEST_SOLUTION = 31
TEST_INPUT_FILE = "test_input_day_12.txt"
INPUT_FILE = "input_day_12.txt"

ARGS = []


INFINITY = float("inf")


class HillClimber:
    def __init__(self, lines, start_x=None, start_y=None):
        self.lines = lines
        self.height = len(lines)
        self.width = len(lines[0])
        if start_x is None or start_y is None:
            self.start_x, self.start_y = self.get_location("S")
            self.lines = self.update_lines(self.start_x, self.start_y, "a", self.lines)
        else:
            self.start_x, self.start_y = start_x, start_y
        self.goal_x, self.goal_y = self.get_location("E")
        self.update_lines(self.goal_x, self.goal_y, "z")
        # Distance from start to each location
        self.distance: list[list[int]] = [
            [INFINITY for _ in range(self.width)] for _ in range(self.height)
        ]
        self.distance[self.start_x][self.start_y] = 0
        # Parent/previous step for that coordinate
        self.previous: list[list[tuple[int, int]]] = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]
        self.next_queue = [(self.start_x, self.start_y)]
        self.path_found = False

    def get_location(self, target: str):
        """Return the location of the given character in the map"""
        for x, line in enumerate(self.lines):
            for y, char in enumerate(line):
                if char == target:
                    return x, y
        raise ValueError(f"Could not find {target} in map")

    def update_lines(self, x, y, char):
        """Update the lines with the given character at the given location"""
        self.lines[x] = self.lines[x][:y] + char + self.lines[x][y + 1 :]

    def get_elevation(self, x, y):
        return ord(self.lines[x][y]) - ord("a")

    def get_valid_neighbors(self, x, y):
        """Unvisited neighbors with a max elevation delta of 1, sorted
        in decreasing elevation gain"""
        neighbors = []
        if (
            x > 0
            and self.distance[x - 1][y] == INFINITY
            and self.get_increase(x, y, x - 1, y) <= 1
        ):
            neighbors.append((x - 1, y))
        if (
            x < self.height - 1
            and self.distance[x + 1][y] == INFINITY
            and self.get_increase(x, y, x + 1, y) <= 1
        ):
            neighbors.append((x + 1, y))
        if (
            y > 0
            and self.distance[x][y - 1] == INFINITY
            and self.get_increase(x, y, x, y - 1) <= 1
        ):
            neighbors.append((x, y - 1))
        if (
            y < self.width - 1
            and self.distance[x][y + 1] == INFINITY
            and self.get_increase(x, y, x, y + 1) <= 1
        ):
            neighbors.append((x, y + 1))
        neighbors.sort(
            key=lambda neighbor: self.get_increase(x, y, *neighbor), reverse=True
        )
        return neighbors

    def get_increase(self, start_x, start_y, target_x, target_y) -> int:
        """Return the elevation increase between the two locations"""
        return self.get_elevation(target_x, target_y) - self.get_elevation(
            start_x, start_y
        )

    def find_shortest_path(self) -> list:
        """Find the shortest path from start to the goal, using Dijkstra's
        Shortest Path"""
        while self.next_queue:
            x, y = self.next_queue.pop(0)
            for neighbor in self.get_valid_neighbors(x, y):
                self.distance[neighbor[0]][neighbor[1]] = self.distance[x][y] + 1
                self.previous[neighbor[0]][neighbor[1]] = (x, y)
                self.next_queue.append(neighbor)
                if neighbor == (self.goal_x, self.goal_y):
                    self.path_found = True
                    return self.get_path(self.goal_x, self.goal_y)
        return []

    def get_path(self, x, y):
        """Return the path from start to the given location"""
        path = [(x, y)]
        while path[-1] != (self.start_x, self.start_y):
            path.append(self.previous[path[-1][0]][path[-1][1]])
        return path[::-1]

    def print_map(self, show_marks=False):
        if show_marks:
            self.update_lines(self.start_x, self.start_y, "S")
            self.update_lines(self.goal_x, self.goal_y, "E")
            if self.path_found:
                path = self.get_path(self.goal_x, self.goal_y)
                for x, line in enumerate(self.lines):
                    for y, char in enumerate(line):
                        if (x, y) in path:
                            print(colors.BLUE + char + colors.ENDC, end="")
                        else:
                            print(char, end="")
                    print()
            else:
                print("\n".join(self.lines))
            self.update_lines(self.start_x, self.start_y, "a")
            self.update_lines(self.goal_x, self.goal_y, "z")
        else:
            print("\n".join(self.lines))


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # The heightmap shows the local area from above broken into a grid; the
    # elevation of each square of the grid is given by a single lowercase
    # letter, where a is the lowest elevation, b is the next-lowest, and so on
    # up to the highest elevation, z.

    # Your current position (S) has elevation a, and the location that should
    # get the best signal (E) has elevation z. During each step, you can move
    # exactly one square up, down, left, or right. The elevation of the
    # destination square can be at most one higher than the elevation of your
    # current square

    # What is the fewest steps required to move from your current position to
    # the location that should get the best signal?

    hillclimber = HillClimber(lines)
    # hillclimber.print_map()
    # print()
    hillclimber.print_map(True)

    path = hillclimber.find_shortest_path()
    # print(path)
    hillclimber.print_map(True)

    solution = len(path) - 1
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
