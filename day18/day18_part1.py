"""Day 18 - Part 1

Depending on the specific compounds in the lava and speed at which it cools, it
might be forming obsidian! The cooling rate should be based on the surface area
of the lava droplets, so you take a quick scan of a droplet as it flies past
you (your puzzle input).

Because of how quickly the lava is moving, the scan isn't very good; its
resolution is quite low and, as a result, it approximates the shape of the lava
droplet with 1x1x1 cubes on a 3D grid, each given as its x,y,z position.

To approximate the surface area, count the number of sides of each cube that
are not immediately connected to another cube. So, if your scan were only two
adjacent cubes like 1,1,1 and 2,1,1, each cube would have a single side covered
and five sides exposed, a total surface area of 10 sides.

What is the surface area of your scanned lava droplet?
"""

from dataclasses import dataclass
from typing import ClassVar

RUN_TEST = False
TEST_SOLUTION = 64
TEST_INPUT_FILE = "test_input_day_18.txt"
INPUT_FILE = "input_day_18.txt"

ARGS = []


class BoilingBoulders:
    def __init__(self, coordinates: list["Coordinate3d"]) -> None:
        self.coordinates = coordinates
        self.coordinate_exposed_sides = {coord: 0 for coord in coordinates}
        self._calculate_exposed_sides()

    def _calculate_exposed_sides(self) -> None:
        """Calculates the number of exposed sides for each coordinate."""
        for coord in self.coordinates:
            self.coordinate_exposed_sides[
                coord
            ] = self._calculate_exposed_sides_for_coordinate(coord)

    def _calculate_exposed_sides_for_coordinate(self, coord: "Coordinate3d") -> int:
        """Calculates the number of exposed sides for a coordinate."""
        return sum(
            1 for neighbor in coord.neighbors if neighbor not in self.coordinates
        )

    def calculate_surface_area(self) -> int:
        """Calculates the surface area of the lava droplets defined by the
        coordinates."""
        return sum(self.coordinate_exposed_sides.values())


@dataclass(frozen=True)
class Coordinate3d(tuple):
    """A 3D coordinate in the grid."""

    coord: tuple[int, int, int]
    DIRECTIONS: ClassVar[
        tuple[
            tuple[int, int, int],
            tuple[int, int, int],
            tuple[int, int, int],
            tuple[int, int, int],
            tuple[int, int, int],
            tuple[int, int, int],
        ]
    ] = (
        (0, 0, 1),
        (0, 0, -1),
        (0, 1, 0),
        (0, -1, 0),
        (1, 0, 0),
        (-1, 0, 0),
    )

    @property
    def x(self) -> int:
        """Returns the x coordinate."""
        return self.coord[0]

    @property
    def y(self) -> int:
        """Returns the y coordinate."""
        return self.coord[1]

    @property
    def z(self) -> int:
        """Returns the z coordinate."""
        return self.coord[2]

    @property
    def neighbors(self) -> list["Coordinate3d"]:
        """Returns the neighbors of the coordinate."""
        return [
            self + Coordinate3d.create(*direction)
            for direction in Coordinate3d.DIRECTIONS
        ]

    @classmethod
    def create(cls, x: int, y: int, z: int) -> "Coordinate3d":
        """Creates a coordinate from x, y, and z values."""
        return Coordinate3d((x, y, z))

    def __add__(self, other: object) -> "Coordinate3d":
        """Adds a coordinate to another coordinate."""
        if not isinstance(other, Coordinate3d):
            raise TypeError("Can only add a 3d coordinate to a 3d coordinate")
        return Coordinate3d.create(self.x + other.x, self.y + other.y, self.z + other.z)


def main_part1(
    input_file,
):
    with open(input_file, encoding="utf8") as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    coordinates = [Coordinate3d.create(*map(int, line.split(","))) for line in lines]

    boiling_boulders = BoilingBoulders(coordinates)
    return boiling_boulders.calculate_surface_area()


if __name__ == "__main__":
    if RUN_TEST:
        SOLUTION = main_part1(TEST_INPUT_FILE, *ARGS)
        print(SOLUTION)
        assert TEST_SOLUTION == SOLUTION
    else:
        SOLUTION = main_part1(INPUT_FILE, *ARGS)
        print(SOLUTION)
