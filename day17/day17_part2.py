"""
Day 17 - Part 2

The elephants are not impressed by your simulation. They demand to know how
tall the tower will be after 1000000000000 rocks have stopped!

How tall will the tower be after 1000000000000 rocks have stopped?
"""

from day17_part1 import PyroclasticFlow

RUN_TEST = True
TEST_SOLUTION = 1514285714288
TEST_INPUT_FILE = "test_input_day_17.txt"
INPUT_FILE = "input_day_17.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file, encoding="utf8") as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    pyro = PyroclasticFlow(lines[0])
    pyro.simulate(1000000000000)
    # pyro.simulate(100000)

    return pyro.max_y


if __name__ == "__main__":
    if RUN_TEST:
        SOLUTION = main_part2(TEST_INPUT_FILE, *ARGS)
        print(SOLUTION)
        assert TEST_SOLUTION == SOLUTION
    else:
        SOLUTION = main_part2(INPUT_FILE, *ARGS)
        print(SOLUTION)
