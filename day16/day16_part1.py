import re
from collections import deque
from dataclasses import dataclass
from functools import total_ordering

RUN_TEST = False
TEST_SOLUTION = 1651
TEST_INPUT_FILE = "test_input_day_16.txt"
INPUT_FILE = "input_day_16.txt"

ARGS = []


@total_ordering
class Journey:
    """Container class for one individual path and time"""

    def __init__(
        self, path: list[tuple[str, str]], time: int, valves: dict[str, "Valve"]
    ) -> None:
        self.path = path
        self.time_left = time
        self.visited, self.opened = self._get_state(path)
        self.complete = False
        self.pressure = 0
        self.valves = valves

    def _calculate_pressure(self, start_time: int) -> int:
        """Calculate the pressure release of a path

        Args:
            start_time (int): Time to start calculating pressure

        Returns:
            int: Pressure release
        """
        pressure = 0
        time_left = start_time
        for action, valve in self.path[1:]:
            if action == "open":
                time_left -= 1
                pressure += self._find_pressure(self.valves[valve], time_left)
            elif action == "enter":
                time_left -= 1
            else:
                print(f"Invalid action, {action}")
                pass
        return pressure

    def _find_pressure(self, valve: "Valve", time_left) -> int:
        return valve.flow_rate * time_left

    def complete_journey(self, start_time: int) -> None:
        """Finalizes the journey, calculating the total pressure released
        from the given start time"""
        self.complete = True
        self.pressure = self._calculate_pressure(start_time)

    def _get_state(self, path: list[tuple[str, str]]) -> tuple[set[str], set[str]]:
        """Get the state of the valves based on the given path

        Args:
            path (list[tuple[str, str]]): List of actions and valves

        Returns:
            tuple[set[str], set[str]]: Visited and opened valves
        """
        visited = set()
        opened = set()
        for action, valve in path:
            visited.add(valve)
            if action == "open":
                opened.add(valve)
        return visited, opened

    def __str__(self) -> str:
        return f"Journey(Path: {self.path}, Time left: {self.time_left}, Pressure: {self.pressure})"

    def __eq__(self, __o: object) -> bool:
        """Equality based on final pressure. Uncompleted journeys can not be
        compared"""
        if isinstance(__o, Journey):
            return self.pressure == __o.pressure
        return False

    def __lt__(self, __o: object) -> bool:
        """Less than based on final pressure. Uncompleted journeys can not be
        compared"""
        if isinstance(__o, Journey):
            return self.pressure < __o.pressure
        return False


class Spelunker:
    """Main explorer logic"""

    def __init__(self, valves: dict[str, "Valve"], time_limit: int) -> None:
        self.valves = valves
        self.time_limit = time_limit
        self.start_time = time_limit
        self.max_pressure = 0
        # Valid actions: "enter" tunnel (cost 1 min), "open" valve (cost 1 min)

    def _is_feasible(self, valve: "Valve") -> bool:
        return valve.flow_rate > 0

    def _bfs(self, start_valve: str, target_valve: str) -> list[tuple[str, str]]:
        """BFS to find the shortest path from start_valve to target_valve

        Args:
            start_valve (str): Name of start valve
            target_valve (str): Name of target valve

        Returns:
            list[tuple[str, str]]: List of actions and valves
        """
        queue: deque[list[tuple[str, str]]] = deque()
        queue.append([("start", start_valve)])
        visited = set()
        while queue:
            path = queue.popleft()
            visited.add(path[-1][1])
            if path[-1][1] == target_valve:
                return path
            for valve in self.valves[path[-1][1]].tunnels:
                if valve not in visited:
                    new_path = list(path)
                    new_path.append(("enter", valve))
                    queue.append(new_path)
        return []

    def find_highest_pressure(self, journey: "Journey") -> "Journey":
        """Find the actions to take that releases most pressure. DFS is used
        to find the highest possible pressure release in the shortest amount
        of time.

        Args:
            path (list[tuple[str, str]]): List of previous actions and valves
            time_left (int): Time left to explore

        Returns:
            list[str]: List of action (valve or tunnel) names in priority order
        """
        # Base case
        if journey.time_left == 0:
            journey.complete_journey(self.start_time)
            # print(f"Time limit (pressure={journey.pressure}) reached for path {journey.path}")
            return journey

        _, current_valve = journey.path[-1]
        next_journeys: list["Journey"] = []
        if not current_valve in journey.opened and self._is_feasible(
            self.valves[current_valve]
        ):
            # Open current valve
            new_path = list(journey.path)
            new_path.append(("open", current_valve))
            new_journey = Journey(new_path, journey.time_left - 1, self.valves)
            next_journeys.append(new_journey)
        else:
            for valve in self.valves.values():
                if (
                    valve.valve != current_valve
                    and self._is_feasible(valve)
                    and valve.valve not in journey.opened
                ):
                    path_to_valve = self._bfs(current_valve, valve.valve)
                    # print(f"Path to {valve.valve}: {path_to_valve}")
                    if path_to_valve:
                        # Extend path with path to valve
                        path_to_valve.pop(0)
                        new_path = list(journey.path)
                        new_path.extend(path_to_valve)
                        new_journey = Journey(
                            new_path,
                            journey.time_left - len(path_to_valve),
                            self.valves,
                        )
                        next_journeys.append(new_journey)

        if not next_journeys:
            # check if there are unopened feasible valves left
            unopened_feasible = False
            for valve in self.valves.values():
                if valve.valve not in journey.opened and self._is_feasible(valve):
                    unopened_feasible = True
                    break
            if not unopened_feasible:
                # No more actions to take, return the current path
                journey.complete_journey(self.start_time)
                return journey
            raise Exception(
                "No more actions to take, but there are unopened feasible valves left. Logical error somewhere!"
            )

        # Find the best path of actions to take
        best_journey = None
        for new_journey in next_journeys:
            complete_journey = self.find_highest_pressure(new_journey)
            if not complete_journey.complete:
                raise ValueError(f"Journey not complete, {complete_journey}")
            if not best_journey:
                best_journey = complete_journey
                continue
            if complete_journey > best_journey:
                best_journey = complete_journey
        # Intentionally returning incomplete journey if no best_journey
        return best_journey if best_journey else journey


@dataclass(frozen=True)
class Valve:
    """One individual valve node"""

    valve: str
    flow_rate: int
    tunnels: tuple[str]

    @classmethod
    def parse(cls, parse_string: str) -> "Valve":
        """Parse a string to create a Valve object

        Args:
            parse_string (str): String to parse in the format
                "Valve AA has flow rate=1; tunnels lead to valves BB, CC"

        Returns:
            Valve: Valve object
        """
        pattern = re.compile(
            r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
        )
        valve_details: tuple[str, str, str] = pattern.findall(parse_string)[0]
        valve = valve_details[0]
        flow_rate = int(valve_details[1])
        tunnels = tuple(valve_details[2].split(", "))
        return cls(valve, flow_rate, tunnels)

    def __repr__(self):
        return f"Valve(valve={self.valve}, flow_rate={self.flow_rate}, tunnels={self.tunnels})"


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # You estimate it will take you one minute to open a single valve and one
    # minute to follow any tunnel from one valve to another.

    # Work out the steps to release the most pressure in 30 minutes. What is
    # the most pressure you can release?

    valves: dict[str, Valve] = {}
    for line in lines:
        valve = Valve.parse(line)
        valves[valve.valve] = valve

    time_left = 30
    # Start in valve AA
    spelunker = Spelunker(valves, time_left)
    start_journey = Journey([("start", "AA")], time_left, valves)
    best_journey = spelunker.find_highest_pressure(start_journey)
    print(f"Path: {best_journey.path}")
    if not best_journey.complete:
        raise ValueError(f"Journey not complete, {best_journey}")
    solution = best_journey.pressure
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
