from collections import defaultdict

RUN_TEST = False
TEST_SOLUTION = 21
TEST_INPUT_FILE = "test_input_day_08.txt"
INPUT_FILE = "input_day_08.txt"

ARGS = []


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # A tree is visible if all of the other trees between it and an edge of the
    # grid are shorter than it. Only consider trees in the same row or column;
    # that is, only look up, down, left, or right from any given tree.

    # All of the trees around the edge of the grid are visible - since they are
    # already on the edge, there are no trees to block the view.

    # Consider your map; how many trees are visible from outside the grid?

    columns = defaultdict(list)
    rows = defaultdict(list)

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            height = int(char)
            columns[j].append(height)
            rows[i].append(height)

    visible_trees = 0
    visible_trees_map = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            height = int(char)
            if i == 0 or j == 0 or i == len(lines) - 1 or j == len(line) - 1:
                visible_trees += 1
                visible_trees_map.append((i, j))
                continue
            if (
                all(height > h for h in columns[j][0:i])
                or all(height > h for h in rows[i][0:j])
                or all(height > h for h in columns[j][i + 1 :])
                or all(height > h for h in rows[i][j + 1 :])
            ):
                visible_trees += 1
                visible_trees_map.append((i, j))

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if (i, j) in visible_trees_map:
                print(char, end="")
            else:
                print(" ", end="")
        print()

    solution = visible_trees
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
