RUN_TEST = False
TEST_SOLUTION = [19, 23, 23, 29, 26]
TEST_INPUT_FILE = "test_input_day_06.txt"
INPUT_FILE = "input_day_06.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # How many characters need to be processed before the first
    # start-of-message marker is detected?

    solutions = []
    marker = 14
    for line in lines:
        for i in range(marker, len(line)):
            if len(set(line[i - marker : i])) == marker:
                solutions.append(i)
                break

    solution = solutions
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
