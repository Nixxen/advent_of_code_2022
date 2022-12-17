RUN_TEST = False
TEST_SOLUTION = 13
TEST_INPUT_FILE = "test_input_day_09.txt"
INPUT_FILE = "input_day_09.txt"

ARGS = []


class Tail:
    def __init__(self, position, parent=None):
        self._position = position
        self._parent = parent
        self._visited: set[tuple] = set()
        self._visited.add(position)

    @property
    def position(self):
        return self._position

    @property
    def visited(self):
        return self._visited

    def __repr__(self):
        return f"Tail({self.position}, {self.visited})"

    def distance(self, target_position):
        return max(
            abs(self.position[0] - target_position[0]),
            abs(self.position[1] - target_position[1]),
        )

    def has_same_cardinals(self, target_position):
        return (
            self.position[0] == target_position[0]
            or self.position[1] == target_position[1]
        )

    def move_cardinally(self, target_position):
        if self.position[0] < target_position[0]:
            self._position = (self.position[0] + 1, self.position[1])
        elif self.position[0] > target_position[0]:
            self._position = (self.position[0] - 1, self.position[1])
        elif self.position[1] < target_position[1]:
            self._position = (self.position[0], self.position[1] + 1)
        elif self.position[1] > target_position[1]:
            self._position = (self.position[0], self.position[1] - 1)

    def move_diagonally(self, target_position):
        if (
            self.position[0] < target_position[0]
            and self.position[1] < target_position[1]
        ):
            self._position = (self.position[0] + 1, self.position[1] + 1)
        elif (
            self.position[0] > target_position[0]
            and self.position[1] > target_position[1]
        ):
            self._position = (self.position[0] - 1, self.position[1] - 1)
        elif (
            self.position[0] < target_position[0]
            and self.position[1] > target_position[1]
        ):
            self._position = (self.position[0] + 1, self.position[1] - 1)
        elif (
            self.position[0] > target_position[0]
            and self.position[1] < target_position[1]
        ):
            self._position = (self.position[0] - 1, self.position[1] + 1)

    def update_position(self, target_position: tuple[int, int]):
        if self.distance(target_position) > 1:
            if not self.has_same_cardinals(target_position):
                self.move_diagonally(target_position)
            else:
                self.move_cardinally(target_position)
            self._visited.add(self.position)


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))
    # The head follows the puzzle input. The tail needs to follow the head,
    # with a max distance of 1 in any direction (cardinal or ordinal
    # directions).

    # Simulate your complete hypothetical series of motions. How many positions
    # does the tail of the rope visit at least once?

    # Assume the head starts at (0, 0), tail stars at head position
    head = (0, 0)
    tail = Tail(head)
    for line in lines:
        direction, distance = line[0], int(line[1:])
        if direction == "R":
            head = (head[0] + distance, head[1])
        elif direction == "L":
            head = (head[0] - distance, head[1])
        elif direction == "U":
            head = (head[0], head[1] + distance)
        elif direction == "D":
            head = (head[0], head[1] - distance)
        for _ in range(distance):
            tail.update_position(head)

    # Print the path map based on tail visited
    min_x = min(tail.visited, key=lambda pos: pos[0])[0]
    max_x = max(tail.visited, key=lambda pos: pos[0])[0]
    min_y = min(tail.visited, key=lambda pos: pos[1])[1]
    max_y = max(tail.visited, key=lambda pos: pos[1])[1]
    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            if (x, y) == head:
                print("H", end="")
            elif (x, y) == tail.position:
                print("T", end="")
            elif (x, y) in tail.visited:
                print("#", end="")
            else:
                print(".", end="")
        print()

    solution = len(tail.visited)
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
