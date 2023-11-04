RUN_TEST = False
TEST_SOLUTION = 4
TEST_INPUT_FILE = "test_input_day_04.txt"
INPUT_FILE = "input_day_04.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # In how many assignment pairs do the ranges overlap?

    def convert_to_tuple(section: str) -> tuple:
        start, end = section.split("-")
        return int(start), int(end)

    containments = 0
    for line in lines:
        elf_1, elf_2 = line.split(",")
        e1 = convert_to_tuple(elf_1)
        e2 = convert_to_tuple(elf_2)

        if (
            (e1[0] <= e2[0] <= e1[1])
            or (e2[0] <= e1[0] <= e2[1])
            or (e1[0] <= e2[1] <= e1[1])
            or (e2[0] <= e1[1] <= e2[1])
        ):
            containments += 1

    solution = containments
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
