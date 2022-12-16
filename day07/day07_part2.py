from day07_part1 import Folder

RUN_TEST = False
TEST_SOLUTION = 24933642
TEST_INPUT_FILE = "test_input_day_07.txt"
INPUT_FILE = "input_day_07.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # The total disk space available to the filesystem is 70000000. To run the
    # update, you need unused space of at least 30000000. You need to find a
    # directory you can delete that will free up enough space to run the
    # update.

    # Find the smallest directory that, if deleted, would free up enough space
    # on the filesystem to run the update. What is the total size of that
    # directory?

    current_folder: "Folder" | None = None
    for line in lines:
        # Parse the line.
        current_folder = Folder.parse_line(current_folder, line)

    while current_folder.parent:
        current_folder = current_folder.parent

    # Traverse the folder structure and find all of the directories
    directories: list["Folder"] = []
    stack: list["Folder"] = [current_folder]
    while stack:
        folder = stack.pop()
        if not folder.is_file:
            directories.append(folder)
        stack.extend(folder.children)

    # Sort the directories by size.
    directories.sort(key=lambda directory: directory.size)

    # Find the smallest directory that, if deleted, would free up enough space
    # on the filesystem to run the update.
    used_space = directories[-1].size
    available = 70000000 - used_space
    required = 30000000
    for directory in directories:
        if directory.size >= required - available:
            solution = directory.size
            break

    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
