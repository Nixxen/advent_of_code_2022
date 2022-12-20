from day14_part1 import RegolithSimulator

RUN_TEST = False
TEST_SOLUTION = 93
TEST_INPUT_FILE = "test_input_day_14.txt"
INPUT_FILE = "input_day_14.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # Using your scan, simulate the falling sand until the source of the sand
    # becomes blocked. How many units of sand come to rest?

    start = (500, 0)
    regolith_sim = RegolithSimulator(lines, start, part=2)
    regolith_sim.print_grid()
    regolith_sim.simulate()
    regolith_sim.print_grid()

    solution = regolith_sim.count_sand()
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
