import sys
from collections import defaultdict

RUN_TEST = False
TEST_SOLUTION = 26
TEST_INPUT_FILE = "test_input_day_15.txt"
INPUT_FILE = "input_day_15.txt"

ARGS = []


class BeaconZone:
    def __init__(self, raw_input: list[str]) -> None:
        self.input = raw_input
        self.symbols = {"air": ".", "beacon": "B", "sensor": "S", "signal": "#"}
        self.grid: defaultdict[tuple, str] = defaultdict(lambda: self.symbols["air"])
        self.sensors: defaultdict[tuple, tuple] = defaultdict(lambda: (None, None))
        self.beacons: set[tuple[int, int]] = set()
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
            self.grid[sensor_coord] = self.symbols["sensor"]
            self.grid[beacon_coord] = self.symbols["beacon"]
            self.sensors[sensor_coord] = beacon_coord
            self.beacons.add(beacon_coord)
            self.max_x = max(self.max_x, sensor__x, beacon__x)
            self.min_x = min(self.min_x, sensor__x, beacon__x)
            self.max_y = max(self.max_y, sensor__y, beacon__y)
            self.min_y = min(self.min_y, sensor__y, beacon__y)

    def fill_signal(self):
        """Fill the signal into the grid using manhattan distance"""
        for sensor_coord, beacon_coord in self.sensors.items():
            print(f"Sensor: {sensor_coord}, Beacon: {beacon_coord}")
            sensor_x, sensor_y = sensor_coord
            beacon_x, beacon_y = beacon_coord
            distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
            # Yank efficiency fix?
            # First quadrant
            for x in range(sensor_x, sensor_x + distance + 1):
                for y in range(sensor_y, sensor_y - distance - 1, -1):
                    if abs(sensor_x - x) + abs(sensor_y - y) > distance:
                        break
                    if self.grid[(x, y)] != self.symbols["air"]:
                        break
                    self.grid[(x, y)] = self.symbols["signal"]

    def filled_in_row(self, y: int) -> int:
        """Check if a row is filled in"""
        return sum(
            1
            for x in range(self.min_x, self.max_x + 1)
            if self.grid[(x, y)] == self.symbols["signal"]
        )

    def __str__(self) -> str:
        """Print the grid"""
        grid_str = ""
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                grid_str += self.grid[(x, y)]
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
    print("Beacon Zone built. Filling signal locations")
    # print(beacon_zone)
    beacon_zone.fill_signal()
    print("Signal locations filled, checking solution")
    print(beacon_zone)
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
