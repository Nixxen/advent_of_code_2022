from utils import lcm

RUN_TEST = False
TEST_SOLUTION = 10605
TEST_INPUT_FILE = "test_input_day_11.txt"
INPUT_FILE = "input_day_11.txt"

ARGS = []


class Monkey:
    def __init__(self, monkey_list: list["Monkey"], relief: int = 3):
        self.operator = ""
        self.op_value = 0
        self.test = 0
        self.if_true = 0  # Monkey ID of true check
        self.if_false = 0
        self.items: list[int] = []
        self._relief = relief
        self._worry_level = 0
        self._inspection_count = 0
        self._monkeys = monkey_list
        self._least_common_multiple = 0

    def parse_operation(self, operation: str) -> tuple[str, int]:
        # Operation: new = old operator value
        _, relevant = operation.split(" old ")
        operator, value = relevant.split(" ")
        if value == "old":
            operator = "**"
            value = "2"
        return operator, int(value)

    def parse_test(self, test: str) -> int:
        # Test: operator_string by value
        _, value = test.split(" by ")
        return int(value)

    def set_lcm(self, value: int) -> None:
        self._least_common_multiple = value

    def find_lcm(self) -> None:
        lcm_it = 1
        for monkey in self._monkeys:
            lcm_it = lcm(lcm_it, monkey.test)
        for monkey in self._monkeys:
            monkey.set_lcm(lcm_it)

    def inspect(self) -> None:
        # Inspect
        self._inspection_count += 1
        self._worry_level = self.items.pop(0)
        if self.operator == "+":
            self._worry_level += self.op_value
        elif self.operator == "*":
            self._worry_level *= self.op_value
        elif self.operator == "**":
            self._worry_level **= self.op_value
        # Bored
        if self._relief != 1:
            self._worry_level //= self._relief
        else:
            self._worry_level %= self._least_common_multiple
        # Test, is divisible by
        if self._worry_level % self.test == 0:
            # Throw to true
            self._monkeys[self.if_true].items.append(self._worry_level)
        else:
            # Throw to false
            self._monkeys[self.if_false].items.append(self._worry_level)

    def can_inspect(self) -> bool:
        return len(self.items) > 0

    @property
    def inspection_count(self) -> int:
        return self._inspection_count

    def __str__(self) -> str:
        return f"Monkey {self._monkeys.index(self)} - Operator: {self.operator} - Op value: {self.op_value} - Test: {self.test} - If true: {self.if_true} - If false: {self.if_false} - Inspection count: {self._inspection_count} - Worry level: {self._worry_level} - LCM: {self._least_common_multiple} Items: {self.items}"


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))
    # Each monkey has several attributes:
    # - `Starting items` lists your worry level for each item the monkey is
    #   currently holding in the order they will be inspected.
    # - `Operation` shows how your worry level changes as that monkey inspects
    #   an item. (An operation like `new = old * 5` means that your worry level
    #   after the monkey inspected the item is five times whatever your worry
    #   level was before inspection.)
    # - `Test` shows how the monkey uses your worry level to decide where to
    #   throw an item next.
    #   - `If true` shows what happens with an item if the Test was true.
    #   - `If false` shows what happens with an item if the Test was false.

    # After each monkey inspects an item but before it tests your worry level,
    # your relief that the monkey's inspection didn't damage the item causes
    # your worry level to be divided by three and rounded down to the nearest
    # integer.

    # The monkeys take turns inspecting and throwing items. On a single
    # monkey's turn, it inspects and throws all of the items it is holding one
    # at a time and in the order listed. Monkey 0 goes first, then monkey 1,
    # and so on until each monkey has had one turn. The process of each monkey
    # taking a single turn is called a round.

    # When a monkey throws an item to another monkey, the item goes on the end
    # of the recipient monkey's list. A monkey that starts a round with no
    # items could end up inspecting and throwing many items by the time its
    # turn comes around. If a monkey is holding no items at the start of its
    # turn, its turn ends.

    # Figure out which monkeys to chase by counting how many items they inspect
    # over 20 rounds. What is the level of monkey business after 20 rounds of
    # stuff-slinging simian shenanigans? The level of monkey business is found
    # by multiplying the number of inspected items the two most active monkeys
    # have inspected.

    monkeys: list[Monkey] = []
    monkey = 0
    for line in lines:
        if line.startswith("Monkey"):
            monkey = int(line.split(" ")[1].strip(":"))
            monkeys.append(Monkey(monkeys))
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

    for monkey in monkeys:
        print(monkey)
        print()

    for _ in range(1, 21):
        for monkey in monkeys:
            while monkey.can_inspect():
                monkey.inspect()

    inspections = [monkey.inspection_count for monkey in monkeys]
    inspections.sort()
    monkey_business = inspections[-1] * inspections[-2]

    solution = monkey_business
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
