"""
Day XX - Part 1

1:
####

2:
.#.
###
.#.

3:
..#
..#
###

4:
#
#
#
#

5:
##
##

The rocks fall in the order shown above. There are five types of rocks,
where `#` is rock and `.` is empty space

The rocks don't spin, but they do get pushed around by jets of hot gas
coming out of the walls themselves. The rocks don't spin, but they do get
pushed around by jets of hot gas coming out of the walls themselves.

The chamber is exactly 7 units wide. Each rock appears so that its left
edge is two units away from the left wall and its bottom edge is three
units above the highest rock in the room (or the floor, if there isn't
one).

Each push left or right is followed by falling down one unit. If a rock
is pushed into a wall, it does not move into the wall.

How many units tall will the tower of rocks be after 2022 rocks have stopped
falling?
"""
from collections import defaultdict
from dataclasses import dataclass

RUN_TEST = False
TEST_SOLUTION = 3068
TEST_INPUT_FILE = "test_input_day_17.txt"
INPUT_FILE = "input_day_17.txt"

ARGS = []


@dataclass(frozen=True)
class Coordinate(tuple):
    """A 2D coordinate in the grid."""

    coord: tuple[int, int]

    @property
    def x(self) -> int:
        """Returns the x coordinate."""
        return self.coord[0]

    @property
    def y(self) -> int:
        """Returns the y coordinate."""
        return self.coord[1]

    @classmethod
    def create(cls, x: int, y: int) -> "Coordinate":
        """Creates a coordinate from x and y values."""
        return cls((x, y))

    def __add__(self, other: object) -> "Coordinate":
        """Adds a coordinate to another coordinate."""
        if not isinstance(other, Coordinate):
            raise TypeError("Can only add a coordinate to a coordinate")
        return Coordinate.create(self.x + other.x, self.y + other.y)


class Rock:
    """A falling rock."""

    def __init__(
        self,
        grid: defaultdict["Coordinate", str],
        coord: "Coordinate",
        type: list[str],
        walls: tuple[set, set],
    ):
        self.grid = grid
        self.coord = coord  # Lower left coordinate of the rock
        self.active = True
        self.type = type
        self.walls_x, self.walls_y = walls[0], walls[1]

    def _get_lower_coordinates(self) -> list["Coordinate"]:
        """Returns the coordinates of the lower rock parts"""
        lower_coordinates = []
        for y in range(len(self.type) - 1, -1, -1):
            for x in range(len(self.type[y])):
                if self.type[y][x] == "#":
                    if y == len(self.type) - 1:
                        lower_coordinates.append(
                            Coordinate.create(
                                self.coord.x + x, self.coord.y - y + len(self.type) - 1
                            )
                        )
                    elif self.type[y - 1][x] == ".":
                        lower_coordinates.append(
                            Coordinate.create(
                                self.coord.x + x, self.coord.y - y + len(self.type) - 1
                            )
                        )
                if len(lower_coordinates) == len(self.type[0]):
                    break
            if len(lower_coordinates) == len(self.type[0]):
                break
        return lower_coordinates

    def _get_left_coordinates(self) -> list["Coordinate"]:
        """Returns the coordinates of the left rock parts"""
        left_coordinates = []
        for y, row in enumerate(self.type):
            for x, item in enumerate(row):
                if item == "#":
                    if x == 0:
                        left_coordinates.append(
                            Coordinate.create(
                                self.coord.x + x, self.coord.y - y + len(self.type) - 1
                            )
                        )
                    elif self.type[y][x - 1] == ".":
                        left_coordinates.append(
                            Coordinate.create(
                                self.coord.x + x, self.coord.y - y + len(self.type) - 1
                            )
                        )
                    else:
                        break
                if len(left_coordinates) == len(self.type):
                    break
            if len(left_coordinates) == len(self.type):
                break
        return left_coordinates

    def _get_right_coordinates(self) -> list["Coordinate"]:
        """Returns the coordinates of the right rock parts"""
        right_coordinates = []
        for y, row in enumerate(self.type):
            for x in range(len(row) - 1, -1, -1):
                if self.type[y][x] == "#":
                    if x == len(row) - 1:
                        right_coordinates.append(
                            Coordinate.create(
                                self.coord.x + x,
                                self.coord.y - y + len(self.type) - 1,
                            )
                        )
                    elif self.type[y][x + 1] == ".":
                        right_coordinates.append(
                            Coordinate.create(
                                self.coord.x + x, self.coord.y - y + len(self.type) - 1
                            )
                        )
                    else:
                        break
                if len(right_coordinates) == len(self.type):
                    break
            if len(right_coordinates) == len(self.type):
                break
        return right_coordinates

    def move(self) -> None:
        """Moves the rock down one unit."""
        if not self.active:
            return

        lower_coordinate_bounds = self._get_lower_coordinates()

        for coord in lower_coordinate_bounds:
            new_coord = Coordinate.create(coord.x, coord.y - 1)
            if self.grid[new_coord] == "#" or self._is_wall(new_coord):
                self.active = False
                return

        self.coord = Coordinate.create(self.coord.x, self.coord.y - 1)

    def push_left(self) -> None:
        """Pushes the rock left."""
        if not self.active:
            return

        left_coord_bounds = self._get_left_coordinates()

        for coord in left_coord_bounds:
            new_coord = Coordinate.create(coord.x - 1, coord.y)
            if self.grid[new_coord] == "#" or self._is_wall(new_coord):
                return

        self.coord = Coordinate.create(self.coord.x - 1, self.coord.y)

    def push_right(self):
        """Pushes the rock right."""
        if not self.active:
            return

        right_coord_bounds = self._get_right_coordinates()

        for coord in right_coord_bounds:
            new_coord = Coordinate.create(coord.x + 1, coord.y)
            if self.grid[new_coord] == "#" or self._is_wall(new_coord):
                return

        self.coord = Coordinate.create(self.coord.x + 1, self.coord.y)

    def get_coordinates(self) -> list["Coordinate"]:
        """Returns the rocky coordinates of the rock."""
        coordinates = []
        for y, row in enumerate(self.type):
            for x, item in enumerate(row):
                if item == "#":
                    coordinates.append(
                        Coordinate.create(
                            self.coord.x + x, self.coord.y - y + len(self.type) - 1
                        )
                    )
        return coordinates

    def _is_wall(self, coord: "Coordinate") -> bool:
        """Checks if a coordinate is a wall."""
        return coord.x in self.walls_x or coord.y in self.walls_y

    def __repr__(self):
        return f"Rock({self.coord})"


class PyroclasticFlow:
    """Main class for the Pyroclastic Flow puzzle.
    Call simulate to solve"""

    def __init__(self, air_flow: str):
        self.air_flow = air_flow
        self.walls_x = set([0, 8])
        self.walls_y = set([0])
        self.max_y = 0
        self.rocks: dict[int, list[str]] = {}
        self.rocks[0] = ["####"]
        self.rocks[1] = [".#.", "###", ".#."]
        self.rocks[2] = ["..#", "..#", "###"]
        self.rocks[3] = ["#", "#", "#", "#"]
        self.rocks[4] = ["##", "##"]
        self.grid: defaultdict["Coordinate", str] = defaultdict(lambda: ".")

    def spawn_coordinate(self) -> "Coordinate":
        """Returns the spawn coordinate for the next rock in the grid"""
        return Coordinate.create(3, self.max_y + 4)  # +1 for offset

    def simulate(self, rocks: int):
        """Simulates the pyroclastic flow."""
        rock_counter = 0
        rock_is_active = False
        rock = Rock(
            self.grid,
            self.spawn_coordinate(),
            self.rocks[rock_counter],
            (self.walls_x, self.walls_y),
        )
        tick = 0
        simulating = True
        while simulating:
            if not rock_is_active:
                rock = Rock(
                    self.grid,
                    self.spawn_coordinate(),
                    self.rocks[rock_counter % len(self.rocks)],
                    (self.walls_x, self.walls_y),
                )
                # print("Spawning new rock")
                # for row in rock.type:
                #     print(row)
                rock_counter += 1
                rock_is_active = True

            if self.air_flow[tick % len(self.air_flow)] == "<":
                rock.push_left()
                # print("Pushing left")
            elif self.air_flow[tick % len(self.air_flow)] == ">":
                rock.push_right()
                # print("Pushing right")
            rock.move()

            if not rock.active:
                # print("Rock is no longer active!")
                rock_is_active = False
                self.max_y = max(self.max_y, rock.coord.y + len(rock.type) - 1)
                for coord in rock.get_coordinates():
                    self.grid[coord] = "#"
                if rock_counter >= rocks:
                    simulating = False
                    break
            tick += 1

    def print_grid(self):
        """Prints the grid."""
        for y in range(self.max_y + 2, -1, -1):
            for x in range(max(self.walls_x) + 1):
                if y in self.walls_y or x in self.walls_x:
                    print("+", end="")
                else:
                    print(self.grid[Coordinate.create(x, y)], end="")
            print()


def main_part1(
    input_file,
):
    with open(input_file, encoding="utf8") as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    pyro = PyroclasticFlow(lines[0])
    pyro.simulate(2022)
    # pyro.print_grid()

    return pyro.max_y


if __name__ == "__main__":
    if RUN_TEST:
        SOLUTION = main_part1(TEST_INPUT_FILE, *ARGS)
        print(SOLUTION)
        assert TEST_SOLUTION == SOLUTION
    else:
        SOLUTION = main_part1(INPUT_FILE, *ARGS)
        print(SOLUTION)
