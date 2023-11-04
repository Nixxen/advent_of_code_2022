RUN_TEST = False
TEST_SOLUTION = [7, 5, 6, 10, 11]
TEST_INPUT_FILE = "test_input_day_06.txt"
INPUT_FILE = "input_day_06.txt"

ARGS = []


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # 4 unique characters defines a marker. The character number at the 4th
    # unique character is the end goal.

    # How many characters need to be processed before the first start-of-packet
    # marker is detected?

    solutions = []
    for line in lines:
        for i in range(4, len(line)):
            if len(set(line[i - 4 : i])) == 4:
                solutions.append(i)
                break

    solution = solutions
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
