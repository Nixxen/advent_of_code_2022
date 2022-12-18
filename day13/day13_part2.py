import functools
import json

from day13_part1 import is_correct_order

RUN_TEST = False
TEST_SOLUTION = 140
TEST_INPUT_FILE = "test_input_day_13.txt"
INPUT_FILE = "input_day_13.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # Divider packets:
    # [[2]]
    # [[6]]

    # To find the decoder key for this distress signal, you need to determine
    # the indices of the two divider packets and multiply them together. (The
    # first packet is at index 1, the second packet is at index 2, and so on.)

    # Organize all of the packets into the correct order. What is the decoder
    # key for the distress signal?

    # Prepare lists
    dividers = [[[2]], [[6]]]
    signals = []
    for i in range(0, len(lines), 3):
        left_raw = lines[i]
        right_raw = lines[i + 1]
        left = json.loads(left_raw)
        right = json.loads(right_raw)
        signals += [left, right]
    signals += dividers
    # print(f"Unsorted: {signals}")

    corrected = sorted(
        [*signals], key=functools.cmp_to_key(is_correct_order), reverse=True
    )
    # for element in corrected:
    #     print(element)
    # print()

    for i, element in enumerate(corrected):
        if element == dividers[0]:
            index_1 = i + 1
        elif element == dividers[1]:
            index_2 = i + 1

    solution = index_1 * index_2
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
