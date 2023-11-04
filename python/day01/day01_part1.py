from collections import defaultdict

RUN_TEST = False
TEST_SOLUTION = 24000
TEST_INPUT_FILE = "test_input_day_01.txt"
INPUT_FILE = "input_day_01.txt"

ARGS = []


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))
    # One important consideration is food - in particular, the number of
    # Calories each Elf is carrying (your puzzle input).

    # The Elves take turns writing down the number of Calories contained by the
    # various meals, snacks, rations, etc. that they've brought with them, one
    # item per line. Each Elf separates their own inventory from the previous
    # Elf's inventory (if any) by a blank line.

    # In case the Elves get hungry and need extra snacks, they need to know
    # which Elf to ask: they'd like to know how many Calories are being carried
    # by the Elf carrying the most Calories.

    # Find the Elf carrying the most Calories. How many total Calories is that
    # Elf carrying?

    elves_calories = defaultdict(int)
    elf = 0
    calories = 0
    for line in lines:
        if line == "":
            elf += 1
            calories = 0
            continue
        calories += int(line)
        elves_calories[elf] = calories

    solution = max(elves_calories.values())
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
