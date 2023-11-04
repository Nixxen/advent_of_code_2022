"""
Day XX - Part 1 

<<insert problem description>>

Reminder for self: To run, use base folder in terminal, 
    `pythonpath/python.exe -m dayXX.dayXX_part1`
"""

from helpers.measure import measure

RUN_TEST = True
TEST_SOLUTION = ...
TEST_INPUT_FILE = "dayXX/test_input_day_XX.txt"
INPUT_FILE = "dayXX/input_day_XX.txt"

ARGS = []


def main_part1(
    input_file,
):
    with open(input_file, encoding="utf8") as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    ...

    return ...


if __name__ == "__main__":
    if RUN_TEST:
        SOLUTION = main_part1(TEST_INPUT_FILE, *ARGS)
        print(SOLUTION)
        assert TEST_SOLUTION == SOLUTION
    else:
        SOLUTION = main_part1(INPUT_FILE, *ARGS)
        print(SOLUTION)
