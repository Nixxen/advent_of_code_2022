from collections import defaultdict

RUN_TEST = False
TEST_SOLUTION = 95437
TEST_INPUT_FILE = "test_input_day_07.txt"
INPUT_FILE = "input_day_07.txt"

ARGS = []


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # The total size of a directory is the sum of the sizes of the files it
    # contains, directly or indirectly.

    # Find all of the directories with a total size of at most 100000. What is
    # the sum of the total sizes of those directories?

    # Example unparsed log:
    # $ cd /
    # $ ls
    # dir a
    # 14848514 b.txt
    # 8504156 c.dat
    # dir d
    # $ cd a
    # $ ls
    # dir e
    # 29116 f
    # 2557 g
    # 62596 h.lst
    # $ cd e
    # $ ls
    # 584 i
    # $ cd ..
    # $ cd ..
    # $ cd d
    # $ ls
    # 4060174 j
    # 8033020 d.log
    # 5626152 d.ext
    # 7214296 k

    class Folder:
        def __init__(self, name: str, parent: "Folder", size: int, is_file=False):
            self._name = name
            self._parent = parent
            self._size = size
            self._is_file = is_file
            self._children: list["Folder"] = []

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, name):
            self._name = name

        @property
        def parent(self):
            return self._parent

        @parent.setter
        def parent(self, parent):
            self._parent = parent

        @property
        def size(self):
            return self._size

        def add_size(self, size):
            self._size += int(size)

        @property
        def children(self):
            return self._children

        def add_child(self, child):
            self.children.append(child)

        @property
        def is_file(self):
            return self._is_file

        def __repr__(self):
            return f"{self.name} {self.parent} {self.size}"

    current_folder: "Folder" = None
    for line in lines:
        # Parse the line.
        line = line.split()
        match line[0]:
            case "$":
                # The line is a command.
                match line[1]:
                    case "cd":
                        # Change the current directory.
                        if not current_folder:
                            # print("creating root folder")
                            current_folder = Folder(line[2], None, 0)
                        else:
                            match line[2]:
                                case "..":
                                    current_folder = current_folder.parent
                                case "/":
                                    while current_folder.parent:
                                        current_folder = current_folder.parent
                                case _:
                                    for folder in current_folder.children:
                                        if folder.name == line[2]:
                                            current_folder = folder
                                            break
                                    else:
                                        new_folder = Folder(line[2], current_folder, 0)
                                        current_folder.add_child(new_folder)
                                        current_folder = new_folder
                    case "ls":
                        # Do nothing. The next line will be a file or directory.
                        pass
            case "dir":
                # The line is a directory.
                # print(f"creating child folder {line[1]}")
                name = line[1]
                size = 0
                new_folder = Folder(name, current_folder, size)
                current_folder.add_child(new_folder)
            case _:  # A number.
                # The line is a file.
                # print(f"creating child file {line[1]}")
                name = line[1]
                size = int(line[0])
                new_folder = Folder(name, current_folder, size, is_file=True)
                current_folder.add_child(new_folder)
                current_folder.add_size(size)
                # recursively add the size to all parent folders
                parent = current_folder.parent
                while parent:
                    parent.add_size(size)
                    parent = parent.parent

    while current_folder.parent:
        current_folder = current_folder.parent

    # Traverse the folder structure and find all of the directories with a
    # total size of at most 100000.
    directories: list["Folder"] = []
    stack: list["Folder"] = [current_folder]
    while stack:
        folder = stack.pop()
        if not folder.is_file and folder.size <= 100000:
            directories.append(folder)
        stack.extend(folder.children)

    # What is the sum of the total sizes of those directories?

    solution = sum(map(lambda directory: directory.size, directories))
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(f"Solution: {solution}")
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
