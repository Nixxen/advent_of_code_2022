from collections import defaultdict

RUN_TEST = False
TEST_SOLUTION = 45000
TEST_INPUT_FILE = "test_input_day_01.txt"
INPUT_FILE = "input_day_01.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # Find the top three Elves carrying the most Calories. How many Calories
    # are those Elves carrying in total?

    elves_calories = defaultdict(int)
    elf = 0
    calories = 0
    for line in lines:
        if line == "":
            elf+=1
            calories = 0
            continue
        calories += int(line)
        elves_calories[elf] = calories


    solution = sum(sorted(elves_calories.values(), reverse=True)[:3])
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
