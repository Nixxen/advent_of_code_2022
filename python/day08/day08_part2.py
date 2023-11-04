from collections import defaultdict

RUN_TEST = False
TEST_SOLUTION = 8
TEST_INPUT_FILE = "test_input_day_08.txt"
INPUT_FILE = "input_day_08.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # A tree's scenic score is found by multiplying together its viewing
    # distance in each of the four directions.

    # Consider each tree on your map. What is the highest scenic score possible
    # for any tree?

    columns = defaultdict(list)
    rows = defaultdict(list)

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            height = int(char)
            columns[j].append(height)
            rows[i].append(height)

    def check_direction(trees: list, height: int) -> int:
        """Returns the number of trees lower than height, until
        (and including) a tree of `height` is encountered

        Args:
            trees (list): List of tree heights
            height (int): Height of the tree to check

        Returns:
            int: Number of trees lower than height
        """
        for i, h in enumerate(trees):
            if h >= height:
                return i + 1
        return len(trees)

    max_scenic_score = 0
    visible_trees_map = []
    best_spot = (0, 0)
    cutoffs = (0, 0, 0, 0)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            height = int(char)
            if i == 0 or j == 0 or i == len(lines) - 1 or j == len(line) - 1:
                visible_trees_map.append((i, j))
                continue
            # Just a fancy map. Not needed, but I like it =)
            if (
                all(height > h for h in columns[j][0:i])
                or all(height > h for h in rows[i][0:j])
                or all(height > h for h in columns[j][i + 1 :])
                or all(height > h for h in rows[i][j + 1 :])
            ):
                visible_trees_map.append((i, j))
            up = check_direction(columns[j][0:i][::-1], height)
            down = check_direction(columns[j][i + 1 :], height)
            left = check_direction(rows[i][0:j][::-1], height)
            right = check_direction(rows[i][j + 1 :], height)
            scenic_score = up * down * left * right
            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score
                best_spot = (i, j)
                cutoffs = (up, down, left, right)
    print(f"Best spot: {best_spot} with a score of {max_scenic_score}")
    print(f"Cutoffs(U, D, L, R): {cutoffs}")

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if (i, j) == best_spot:
                print("X", end="")
            elif i == best_spot[0] and (
                best_spot[1] - cutoffs[2] + 1 <= j <= best_spot[1] + cutoffs[3] - 1
            ):
                print("-", end="")
            elif j == best_spot[1] and (
                best_spot[0] - cutoffs[0] + 1 <= i <= best_spot[0] + cutoffs[1] - 1
            ):
                print("|", end="")
            elif (i, j) in visible_trees_map:
                print(char, end="")
            else:
                print(" ", end="")
        print()

    solution = max_scenic_score
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
