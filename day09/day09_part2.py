from day09_part1 import Tail

RUN_TEST = False
TEST_SOLUTION = 36
TEST_INPUT_FILE = "test_input_day_09_larger.txt"
INPUT_FILE = "input_day_09.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # Simulate your complete series of motions on a larger rope with ten knots.
    # How many positions does the tail of the rope visit at least once?
    head = (0, 0)
    tail = Tail(head, tail_limit=9)
    for line in lines:
        direction, distance = line[0], int(line[1:])
        if direction == "R":
            for _ in range(distance):
                head = (head[0] + 1, head[1])
                tail.update_position(head)
        elif direction == "L":
            for _ in range(distance):
                head = (head[0] - 1, head[1])
                tail.update_position(head)
        elif direction == "U":
            for _ in range(distance):
                head = (head[0], head[1] + 1)
                tail.update_position(head)
        elif direction == "D":
            for _ in range(distance):
                head = (head[0], head[1] - 1)
                tail.update_position(head)

    # Print the path map based on tail visited (just for fun)
    min_x = min(tail.visited, key=lambda pos: pos[0])[0]
    max_x = max(tail.visited, key=lambda pos: pos[0])[0]
    min_y = min(tail.visited, key=lambda pos: pos[1])[1]
    max_y = max(tail.visited, key=lambda pos: pos[1])[1]
    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            if (x, y) == head:
                print("H", end="")
            elif (x, y) == tail.position:
                print("1", end="")
            else:
                temp_tail = tail
                printed = False
                while temp_tail.next_tail:
                    temp_tail = temp_tail.next_tail
                    if (x, y) == temp_tail.position:
                        print(temp_tail.tail_length(), end="")
                        printed = True
                        break
                while temp_tail.next_tail:
                    temp_tail = temp_tail.next_tail
                if (x, y) in temp_tail.visited:
                    print("#", end="")
                    printed = True
                if not printed:
                    print(".", end="")
        print()

    final_tail = tail
    while final_tail.next_tail:
        final_tail = final_tail.next_tail

    solution = len(final_tail.visited)
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
