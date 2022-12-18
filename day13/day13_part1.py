import json
from itertools import zip_longest

RUN_TEST = False
TEST_SOLUTION = 13
TEST_INPUT_FILE = "test_input_day_13.txt"
INPUT_FILE = "input_day_13.txt"

ARGS = []


def verify_signal(input: list[str]) -> tuple[list[int], list[int]]:
    """Base call to recursively compare left and right packet of input

    Args:
        input (list[str]): list of packets

    Returns:
        tuple(list[int], list[int]): Two lists of indices. The first has
        packets in the right order, the second has packets in the wrong order
    """
    correct_order = []
    wrong_order = []
    for i in range(0, len(input), 3):
        left_raw = input[i]
        right_raw = input[i + 1]
        left = json.loads(left_raw)
        right = json.loads(right_raw)
        print(f"\nPair {i // 3 + 1}: L{left_raw} vs R{right_raw}")
        result = is_correct_order(left, right)
        if result == 1:
            correct_order.append((i // 3) + 1)
            print("Correct order")
        elif result == -1:
            wrong_order.append((i // 3) + 1)
            print("Wrong order")
        else:
            print("Undecided")
    return (correct_order, wrong_order)


def is_correct_order(left: list | None, right: list | None) -> int:
    """Recursive function to compare left and right packet of input

    Args:
        left (list): left packet
        right (list): right packet

    Returns:
        int: 1 if in correct order, 0 if undecided, -1 if in wrong order
    """
    # print(f"left: {left}, right: {right}")
    if left is None:
        return 1
    if right is None:
        return -1
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        if left > right:
            return -1
        return 0
    if isinstance(left, list) and isinstance(right, list):
        for left_item, right_item in zip_longest(left, right, fillvalue=None):
            result = is_correct_order(left_item, right_item)
            if result != 0:
                return result
        return 0
    if isinstance(left, int) and isinstance(right, list):
        return is_correct_order([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return is_correct_order(left, [right])
    raise Exception("Invalid input")


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # Packet data consists of lists and integers. Each list starts with [, ends
    # with ], and contains zero or more comma-separated values (either integers
    # or other lists). Each packet is always a list and appears on its own
    # line.

    # When comparing two values, the first value is called left and the second
    # value is called right. Then:
    # - If both values are integers, the lower integer should come first. If
    #   the left integer is lower than the right integer, the inputs are in the
    #   right order. If the left integer is higher than the right integer, the
    #   inputs are not in the right order. Otherwise, the inputs are the same
    #   integer; continue checking the next part of the input.
    # - If both values are lists, compare the first value of each list, then
    #   the second value, and so on. If the left list runs out of items first,
    #   the inputs are in the right order. If the right list runs out of items
    #   first, the inputs are not in the right order. If the lists are the same
    #   length and no comparison makes a decision about the order, continue
    #   checking the next part of the input.
    # - If exactly one value is an integer, convert the integer to a list which
    #   contains that integer as its only value, then retry the comparison. For
    #   example, if comparing [0,0,0] and 2, convert the right value to [2] (a
    #   list containing 2); the result is then found by instead comparing
    #   [0,0,0] and [2].

    # Determine which pairs of packets are already in the right order. What is
    # the sum of the indices of those pairs?

    correct, wrong = verify_signal(lines)

    print(f"Correct: {correct}, Wrong: {wrong}")
    solution = sum(correct)
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
