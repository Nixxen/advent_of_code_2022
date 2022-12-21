import sys

RUN_TEST = False
TEST_SOLUTION = 26
TEST_INPUT_FILE = "test_input_day_15.txt"
INPUT_FILE = "input_day_15.txt"

ARGS = []


class BeaconZone:
    def __init__(self, raw_input: list[str]) -> None:
        self.input = raw_input
        self.symbols = {"air": ".", "beacon": "B", "sensor": "S", "signal": "#"}
        self.sensors: dict[tuple[int, int], tuple[int, int]] = {}
        self.max_x = 0
        self.min_x = sys.maxsize
        self.max_y = 0
        self.min_y = sys.maxsize
        self.parse_input()

    def parse_input(self):
        """Parse input and map sensors and beacons to the grid"""
        # Example input: Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        for line in self.input:
            sensor__x = int(line.split(":")[0].split("=")[1].split(",")[0])
            sensor__y = int(line.split(":")[0].split("=")[2])
            sensor_coord = (sensor__x, sensor__y)
            beacon__x = int(line.split(":")[1].split("=")[1].split(",")[0])
            beacon__y = int(line.split(":")[1].split("=")[2])
            beacon_coord = (beacon__x, beacon__y)
            self.sensors[sensor_coord] = beacon_coord
            self.max_x = max(self.max_x, sensor__x, beacon__x)
            self.min_x = min(self.min_x, sensor__x, beacon__x)
            self.max_y = max(self.max_y, sensor__y, beacon__y)
            self.min_y = min(self.min_y, sensor__y, beacon__y)

    def distance(self, a: tuple[int, int], b: tuple[int, int]) -> int:
        """Calculate Manhattan distance between two points"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def merge_ranges_in_row(self, y: int) -> tuple[list[list[int]], set]:
        potential_sensors = []
        blocking_beacons = set()
        x_ranges: list[tuple[int, int]] = []
        for sensor, beacon in self.sensors.items():
            dist = self.distance(sensor, beacon)
            if sensor[1] - dist <= y <= sensor[1] + dist:
                potential_sensors.append(sensor)
                y_offset = abs(y - sensor[1])
                x_offset = dist - y_offset
                x_ranges.append((sensor[0] - x_offset, sensor[0] + x_offset))
            if beacon[1] == y:
                blocking_beacons.add(beacon)
        for beacon in blocking_beacons:
            x_ranges.append((beacon[1], beacon[1]))
        # Merge overlapping ranges
        x_ranges.sort()
        merged_ranges: list[list[int]] = [list(x_ranges[0])]
        for x_range in x_ranges[1:]:
            if x_range[0] <= merged_ranges[-1][1] + 1:
                merged_ranges[-1][1] = max(merged_ranges[-1][1], x_range[1])
            else:
                merged_ranges.append(list(x_range))
        return merged_ranges, blocking_beacons

    def filled_in_row(self, y: int) -> int:
        """Return the number of signal covered locations in a row"""
        merged_ranges, blocking_beacons = self.merge_ranges_in_row(y)
        # Count the number of locations that are not covered by a sensor
        total = 0
        for segment in merged_ranges:
            total += segment[1] - segment[0] + 1
        return total - len(blocking_beacons)

    def __str__(self) -> str:
        """Print the grid"""
        grid_str = ""
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                if (x, y) in self.sensors:
                    grid_str += self.symbols["sensor"]
                elif (x, y) in self.sensors.values():
                    grid_str += self.symbols["beacon"]
                else:
                    grid_str += self.symbols["air"]
            grid_str += "\n"
        return grid_str


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # Each sensor knows its own position and can determine the position of a
    # beacon precisely; however, sensors can only lock on to the one beacon
    # closest to the sensor as measured by the Manhattan distance.

    # If a sensor detects a beacon, you know there are no other beacons that
    # close or closer to that sensor. There could still be beacons that just
    # happen to not be the closest beacon to any sensor.

    # Consult the report from the sensors you just deployed. In the row where
    # y=2000000, how many positions cannot contain a beacon?

    print("Building Beacon Zone")
    beacon_zone = BeaconZone(lines)
    print("Beacon Zone built. Checking signal values")
    # print(beacon_zone)
    row = 10 if RUN_TEST else 2000000
    solution = beacon_zone.filled_in_row(row)
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
