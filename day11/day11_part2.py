from day11_part1 import Monkey

RUN_TEST = False
TEST_SOLUTION = 2713310158
TEST_INPUT_FILE = "test_input_day_11.txt"
INPUT_FILE = "input_day_11.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # Worry levels are no longer divided by three after each item is inspected;
    # you'll need to find another way to keep your worry levels manageable.
    # Starting again from the initial state in your puzzle input, what is the
    # level of monkey business after 10000 rounds?

    monkeys: list[Monkey] = []
    monkey = 0
    for line in lines:
        if line.startswith("Monkey"):
            monkey = int(line.split(" ")[1].strip(":"))
            monkeys.append(Monkey(monkeys, 1))
        elif line.startswith("  Starting items"):
            _, items = line.split(": ")
            monkeys[monkey].items = list(map(int, items.split(", ")))
        elif line.startswith("  Operation"):
            operator, value = monkeys[monkey].parse_operation(line)
            monkeys[monkey].operator = operator
            monkeys[monkey].op_value = value
        elif line.startswith("  Test"):
            test = monkeys[monkey].parse_test(line)
            monkeys[monkey].test = test
        elif line.startswith("    If true"):
            _, if_true = line.split("monkey ")
            monkeys[monkey].if_true = int(if_true)
        elif line.startswith("    If false"):
            _, if_false = line.split("monkey ")
            monkeys[monkey].if_false = int(if_false)

    monkeys[0].find_lcm()
    for monkey in monkeys:
        print(monkey)

    for _ in range(1, 10001):
        for monkey in monkeys:
            while monkey.can_inspect():
                monkey.inspect()
        if _ % 1000 == 0:
            print(f"Round {_}")

    inspections = [monkey.inspection_count for monkey in monkeys]
    inspections.sort()
    monkey_business = inspections[-1] * inspections[-2]

    solution = monkey_business
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
