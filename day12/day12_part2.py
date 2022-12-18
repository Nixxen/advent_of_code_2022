from day12_part1 import HillClimber

RUN_TEST = False
TEST_SOLUTION = 29
TEST_INPUT_FILE = "test_input_day_12.txt"
INPUT_FILE = "input_day_12.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # What is the fewest steps required to move starting from any square with
    # elevation a to the location that should get the best signal?

    def update_lines(x, y, char, lines) -> list[str]:
        """Update the lines with the given character at the given location"""
        lines[x] = lines[x][:y] + char + lines[x][y + 1 :]
        return lines

    def get_location(target: str, lines: list[str]) -> tuple[int, int]:
        """Return the location of the given character in the map"""
        for x, line in enumerate(lines):
            for y, char in enumerate(line):
                if char == target:
                    return x, y
        raise ValueError(f"Could not find {target} in map")

    start_x, start_y = get_location("S", lines=lines)
    lines = update_lines(start_x, start_y, "a", lines)

    start_location_queue = []
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if char == "a":
                start_location_queue.append((x, y))

    shortest_path = []
    best_hillclimber = None
    for x, y in start_location_queue:
        temp_lines = [line[:] for line in lines]
        temp_hillclimber = HillClimber(temp_lines, x, y)
        path = temp_hillclimber.find_shortest_path()
        if (path and len(path) < len(shortest_path)) or (path and not shortest_path):
            shortest_path = path
            best_hillclimber = temp_hillclimber

    best_hillclimber.print_map(True)

    solution = len(shortest_path) - 1
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
