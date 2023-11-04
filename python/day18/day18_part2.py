"""Day 18 - Part 2

The cooling rate depends on exterior surface area, but your calculation also
included the surface area of air pockets trapped in the lava droplet.

Instead, consider only cube sides that could be reached by the water and steam
as the lava droplet tumbles into the pond. The steam will expand to reach as
much as possible, completely displacing any air on the outside of the lava
droplet but never expanding diagonally.

What is the exterior surface area of your scanned lava droplet?
"""

import sys

from day18.day18_part1 import BoilingBoulders, Coordinate3d

print(
    "In module sys.path[0], __package__, __name__ ==",
    sys.path[0],
    __package__,
    __name__,
)

import os

print("In module os.getcwd() ==", os.getcwd())

from helpers.measure import measure

RUN_TEST = False
TEST_SOLUTION = 58
TEST_INPUT_FILE = "day18/test_input_day_18.txt"
INPUT_FILE = "day18/input_day_18.txt"

ARGS = []


@measure
def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    print("Creating test boiling boulders...")
    coord_set = set()
    coord = Coordinate3d.create(0, 0, 0)
    coord_set.add(coord)
    for neighbor in coord.neighbors:
        coord_set.add(neighbor)
    coord = Coordinate3d.create(12, 4, 5)
    coord_set.add(coord)
    for neighbor in coord.neighbors:
        coord_set.add(neighbor)

    test_boiling_boulders = BoilingBoulders(list(coord_set))
    joined_air = test_boiling_boulders._join_air_bubbles(coord_set)
    print("Joined air:")
    for key, value in joined_air.items():
        print(f"{key}: {value}")
    # TODO: Expecting two dict entries. Not what I am seeing...

    print("Creating coordinates...")
    coordinates = [Coordinate3d.create(*map(int, line.split(","))) for line in lines]

    print("Creating boiling boulders...")

    boiling_boulders = BoilingBoulders(coordinates)
    print(f"Trapped air: {boiling_boulders.trapped_air}")
    print("Calculating surface area...")
    # TODO: Something jank going on.
    return boiling_boulders.calculate_surface_area_with_trapped_air()


if __name__ == "__main__":
    if RUN_TEST:
        SOLUTION = main_part2(TEST_INPUT_FILE, *ARGS)
        print(SOLUTION)
        assert TEST_SOLUTION == SOLUTION
    else:
        SOLUTION = main_part2(INPUT_FILE, *ARGS)
        print(SOLUTION)
