from collections import defaultdict

RUN_TEST = False
TEST_SOLUTION = 157
TEST_INPUT_FILE = "test_input_day_03.txt"
INPUT_FILE = "input_day_03.txt"

ARGS = []


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # Each rucksack has two large compartments. All items of a given type are
    # meant to go into exactly one of the two compartments.

    # To help prioritize item rearrangement, every item type can be converted
    # to a priority:

    # Lowercase item types a through z have priorities 1 through 26.
    # Uppercase item types A through Z have priorities 27 through 52.
    def convert(char: str, count: int) -> int:
        if char.islower():
            return (ord(char) - ord("a") + 1) * count
        return (ord(char) - ord("A") + 1 + 26) * count

    # Find the item type that appears in both compartments of each rucksack.
    # What is the sum of the priorities of those item types?

    duplicates = defaultdict(int)
    for line in lines:
        left_compartment = line[: len(line) // 2]
        right_compartment = line[len(line) // 2 :]
        for char in left_compartment:
            if char in right_compartment:
                duplicates[char] += 1
                break  # Do not count duplicates

    solution = sum(map(convert, duplicates.keys(), duplicates.values()))
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
