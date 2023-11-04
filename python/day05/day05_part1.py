import re
from collections import defaultdict

RUN_TEST = False
TEST_SOLUTION = "CMZ"
TEST_INPUT_FILE = "test_input_day_05.txt"
INPUT_FILE = "input_day_05.txt"

ARGS = []


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # The Elves just need to know which crate will end up on top of each stack;

    # After the rearrangement procedure completes, what crate ends up on top of
    # each stack?

    # Example stack:
    #     [D]
    # [N] [C]
    # [Z] [M] [P]
    #  1   2   3
    #
    # move 1 from 2 to 1
    # move 3 from 1 to 3
    # move 2 from 2 to 1
    # move 1 from 1 to 2

    # One stack is represented by 3 characters, separated by a space
    # Each crate it wrapped in [ ]

    def move_crate(
        amount: int, from_stack: int, to_stack: int, stacks: defaultdict[int, list[str]]
    ) -> defaultdict[int, list[str]]:
        """Move amount of crates from from_stack to to_stack, one at a time

        Args:
            amount (int): Amount of crates to move
            from_stack (int): Stack to move from
            to_stack (int): Stack to move to
            stacks (dict): Input stacks dictionary

        Returns:
            dict: Updated stacks dictionary
        """
        for _ in range(amount):
            stacks[to_stack].append(stacks[from_stack].pop())
        return stacks

    stacks: defaultdict[int, list[str]] = defaultdict(list)
    procedures = []

    done_finding_stacks = False
    for line in lines:
        if not done_finding_stacks:
            if re.search(r"\[.*\]", line):
                # Start stack is index 1, then every 4th char
                stack_index = 0
                for i in range(1, len(line), 4):
                    stack_index += 1
                    if line[i] == " ":
                        continue
                    stacks[stack_index].append(line[i])
                # print(f"Stack line: {line}")
                continue
            # No more crates, skip number line
            done_finding_stacks = True
            # print("Done finding stacks, reversing order")
            for stack in stacks.values():
                stack.reverse()
            # print(f"Stacks: {stacks}")
            continue
        if line == "":
            continue
        # print(f"Procedure line: {line}")
        procedures.append(line)

    for procedure in procedures:
        _, amount, _, from_stack, _, to_stack = procedure.split(" ")
        amount = int(amount)
        from_stack = int(from_stack)
        to_stack = int(to_stack)
        stacks = move_crate(amount, from_stack, to_stack, stacks)

    stacks = dict(sorted(stacks.items()))
    top_stacks = ""
    for stack in stacks.values():
        top_stacks += stack.pop()

    solution = top_stacks
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
