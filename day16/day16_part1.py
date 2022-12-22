import re
from collections import deque

RUN_TEST = True
TEST_SOLUTION = 1651
TEST_INPUT_FILE = "test_input_day_16.txt"
INPUT_FILE = "input_day_16.txt"

ARGS = []


class Spelunker:
    def __init__(
        self, start_valve: "Valve", valves: dict[str, "Valve"], time_limit: int
    ) -> None:
        self.start_valve = start_valve
        self.valves = valves
        self.time_limit = time_limit
        self.start_valve = start_valve
        self.start_time = time_limit
        self.max_pressure = 0
        # Valid actions: "enter" tunnel (cost 1 min), "open" valve (cost 1 min)

    def is_feasible(self, valve: "Valve") -> bool:
        return valve.flow_rate > 0

    def find_pressure(self, valve: "Valve", time_left) -> int:
        return valve.flow_rate * time_left

    def calculate_pressure(self, path: list[tuple[str, str]], start_time: int) -> int:
        """Calculate the pressure release of a path

        Args:
            path (list[tuple[str, str]]): List of actions and valves
            start_time (int): Time to start calculating pressure

        Returns:
            int: Pressure release
        """
        pressure = 0
        time_left = start_time
        for action, valve in path[1:]:
            if action == "open":
                time_left -= 1
                pressure += self.find_pressure(self.valves[valve], time_left)
            elif action == "enter":
                time_left -= 1
            else:
                print(f"Invalid action, {action}")
                pass
        return pressure

    def get_state(self, path: list[tuple[str, str]]) -> tuple[set[str], set[str]]:
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

    def bfs(self, start_valve: str, target_valve: str) -> list[tuple[str, str]]:
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

    def find_highest_pressure(
        self, path: list[tuple[str, str]], time_left: int
    ) -> list[tuple[str, str]]:
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
        if time_left == 0:
            final_pressure = self.calculate_pressure(path, self.start_time)
            path.append(("return", str(final_pressure)))
            # print(f"Time limit reached for path {path}")
            return path

        # Get state of valves based on path, and find the valid next actions
        visited, opened = self.get_state(path)

        _, current_valve = path[-1]
        next_actions: list[tuple[str, str]] = []
        if not current_valve in opened and self.is_feasible(self.valves[current_valve]):
            next_actions.append(("open", current_valve))
        for valve in self.valves.values():
            if (
                valve.valve != current_valve
                and self.is_feasible(valve)
                and valve.valve not in opened
            ):
                path_to_valve = self.bfs(current_valve, valve.valve)
                print(f"Path to {valve.valve}: {path_to_valve}")
                if path_to_valve:
                    # Find first tuple with an enter action
                    first_enter = next(
                        i for i, x in enumerate(path_to_valve) if x[0] == "enter"
                    )
                    next_actions.append(path_to_valve[first_enter])
                    # break
                    # TODO: Make shortcut, instead of re-calculating

        # If there are no valid actions in current valve room
        if not next_actions:
            # check if there are unopened feasible valves left
            unopened_feasible = False
            for valve in self.valves.values():
                if valve.valve not in opened and self.is_feasible(valve):
                    unopened_feasible = True
                    break
            if not unopened_feasible:
                # No more actions to take, return the current path
                final_pressure = self.calculate_pressure(path, self.start_time)
                path.append(("return", str(final_pressure)))
                # print(f"No more actions to take from path {path}")
                return path
            raise Exception(
                "No more actions to take, but there are unopened feasible valves left"
            )

        # Find the best path of actions to take
        best_pressure = 0
        best_path = []
        # print(f"Path: {path}, time left: {time_left}, next actions: {next_actions}")
        for action, valve_b in next_actions:
            new_path = list(path)
            new_path.append((action, valve_b))
            final_path = self.find_highest_pressure(new_path, time_left - 1)
            final_pressure = int(final_path[-1][1])
            if final_pressure > best_pressure:
                best_pressure = final_pressure
                best_path = final_path
        return best_path if best_path else [("return", "0")]


class Valve:
    def __init__(self, parse_string) -> None:
        self.valve = ""
        self.flow_rate = 0
        self.tunnels: list[str] = []
        self._parse(parse_string)

    def _parse(self, parse_string) -> None:
        pattern = re.compile(
            r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
        )
        valve_details: tuple[str, str, str] = pattern.findall(parse_string)[0]
        self.valve = valve_details[0]
        self.flow_rate = int(valve_details[1])
        self.tunnels = valve_details[2].split(", ")

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
        valve = Valve(line)
        valves[valve.valve] = valve

    time_left = 30
    # Start in valve AA
    current_valve = valves["AA"]
    spelunker = Spelunker(current_valve, valves, time_left)
    path = spelunker.find_highest_pressure([("start", "AA")], time_left)
    print(f"Path: {path}")
    solution = path[-1][1]
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
