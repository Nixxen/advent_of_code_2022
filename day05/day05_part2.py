import re
from collections import defaultdict

RUN_TEST = False
TEST_SOLUTION = "MCD"
TEST_INPUT_FILE = "test_input_day_05.txt"
INPUT_FILE = "input_day_05.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))
    # One stack is represented by 3 characters, separated by a space
    # Each crate it wrapped in [ ]

    def move_crate_multiple(
        amount: int, from_stack: int, to_stack: int, stacks: defaultdict[int, list[str]]
    ) -> defaultdict[int, list[str]]:
        """Move amount of crates from from_stack to to_stack, all at the same
        time

        Args:
            amount (int): Amount of crates to move
            from_stack (int): Stack to move from
            to_stack (int): Stack to move to
            stacks (dict): Input stacks dictionary

        Returns:
            dict: Updated stacks dictionary
        """
        stacks[to_stack] += stacks[from_stack][-amount:]
        stacks[from_stack] = stacks[from_stack][:-amount]
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
        stacks = move_crate_multiple(amount, from_stack, to_stack, stacks)

    stacks = dict(sorted(stacks.items()))
    top_stacks = ""
    for stack in stacks.values():
        top_stacks += stack.pop()

    solution = top_stacks
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
