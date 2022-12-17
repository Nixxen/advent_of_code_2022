RUN_TEST = False
TEST_SOLUTION = 13140
TEST_INPUT_FILE = "test_input_day_10.txt"
INPUT_FILE = "input_day_10.txt"

ARGS = []


class Program:
    def __init__(self, instructions: list[str], register_start=1):
        self._instructions = instructions
        self._instruction_pointer = 0
        self._register = register_start
        self._cycle = 0
        self._delayed_instructions: list[str] = []
        self._previous_register = None

    def run(self) -> None:
        # Start of cycle
        self._cycle += 1
        self._previous_register = self._register
        # print(f"Cycle {self._cycle}: {self._register}")
        if self._delayed_instructions:
            # End of cycle with instruction queue
            # print(f"Delayed Instruction: {self._delayed_instructions[0]}")
            self._execute_instruction(self._delayed_instructions.pop(0))
        else:
            # Middle of cycle with no instruction queue
            if self._instruction_pointer >= len(self._instructions):
                return
            instruction = self._instructions[self._instruction_pointer]
            # print(f"Instruction: {instruction}")
            if instruction.startswith("addx"):
                # self._delayed_instructions.append("noop")
                self._delayed_instructions.append(instruction)
            else:
                self._execute_instruction(instruction)

    def is_running(self) -> bool:
        return (
            self._instruction_pointer < len(self._instructions)
            or self._delayed_instructions
        )

    def _execute_instruction(self, instruction: str) -> None:
        if instruction.startswith("addx"):
            self._register += int(instruction.split(" ")[1])
            self._instruction_pointer += 1
        elif instruction.startswith("noop"):
            self._instruction_pointer += 1
        else:
            raise ValueError(f"Unknown instruction: {instruction}")

    @property
    def register(self):
        return self._register

    @property
    def previous_register(self):
        """Compensate for getting the register at the middle of the cycle"""
        return self._previous_register

    @property
    def cycle(self):
        return self._cycle


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # The CPU has a single register, X, which starts with the value 1. It
    # supports only two instructions:
    # - `addx V` takes two cycles to complete. After two cycles, the X register
    # is increased by the value V. (V can be negative.)
    # - `noop` takes one cycle to complete. It has no other effect.

    # Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and
    # 220th cycles. What is the sum of these six signal strengths?

    program = Program(lines)
    check_points = set([20, 60, 100, 140, 180, 220])
    signal_strength = {}
    while program.is_running():
        program.run()
        # NB! During is not AFTER, and updates to register are executed AFTER
        # the cycle completes. Compensate by taking the previous cycle value.
        if program.cycle in check_points:
            signal_strength[program.cycle] = program.previous_register * program.cycle
            print(
                f"Cycle {program.cycle+1}: {program.previous_register * program.cycle}"
            )

    solution = sum(signal_strength.values())
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
