from day15_part1 import BeaconZone

RUN_TEST = False
TEST_SOLUTION = 56000011
TEST_INPUT_FILE = "test_input_day_15.txt"
INPUT_FILE = "input_day_15.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # The distress beacon must have x and y coordinates each no lower than 0
    # and no larger than 4000000.

    # To isolate the distress beacon's signal, you need to determine its tuning
    # frequency, which can be found by multiplying its x coordinate by 4000000
    # and then adding its y coordinate.

    # Find the only possible position for the distress beacon. What is its
    # tuning frequency?

    print("Building Beacon Zone")
    beacon_zone = BeaconZone(lines)
    print("Beacon Zone built. Checking signal values")
    position = (0, 0)
    searching = True
    row = -1
    while searching:
        row += 1
        if row == 4000000:
            break
        if row % 100000 == 0:
            print(f"Checking row {row}. Complete: {row / 4000000:.2%}")
        merged_ranges, _ = beacon_zone.merge_ranges_in_row(row)
        if len(merged_ranges) == 1:
            continue
        print(
            f"Row {row} has {len(merged_ranges)} merged ranges, values are {merged_ranges}"
        )
        for i, element in enumerate(merged_ranges[1:], 1):
            if element[0] - merged_ranges[i - 1][1] == 2:
                print(f"Found a gap in {merged_ranges}")
                position = (element[0] - 1, row)
                searching = False
                break

    print(f"Position found: {position}")
    solution = position[0] * 4000000 + position[1]
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
