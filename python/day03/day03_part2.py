from collections import defaultdict

RUN_TEST = False
TEST_SOLUTION = 70
TEST_INPUT_FILE = "test_input_day_03.txt"
INPUT_FILE = "input_day_03.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # The only way to tell which item type is the right one is by finding the
    # one item type that is common between all three Elves in each group.

    # One group of elves are represented by the three lines containing their
    # backpacks.

    # Find the item type that corresponds to the badges of each three-Elf
    # group. What is the sum of the priorities of those item types?

    def convert(char: str, count: int) -> int:
        if char.islower():
            return (ord(char) - ord("a") + 1) * count
        return (ord(char) - ord("A") + 1 + 26) * count

    badges = defaultdict(int)
    for index in range(0, len(lines), 3):
        for char in lines[index]:
            if char in lines[index + 1] and char in lines[index + 2]:
                badges[char] += 1
                break

    solution = sum(map(convert, badges.keys(), badges.values()))
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
