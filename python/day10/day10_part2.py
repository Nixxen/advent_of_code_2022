from day10_part1 import Program

RUN_TEST = False
TEST_SOLUTION = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""
TEST_INPUT_FILE = "test_input_day_10.txt"
INPUT_FILE = "input_day_10.txt"

ARGS = []


class CRT:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._screen = [["." for _ in range(width)] for _ in range(height)]

    def render(self, cycle: int, register: int, sprite: list[str] = "###") -> None:
        row = (cycle - 1) // self._width
        col = (cycle - 1) % self._width
        if register - len(sprite) // 2 <= col <= register + len(sprite) // 2:
            # Assuming sprite has equal pixel values
            self._screen[row][col] = sprite[0]

    def __str__(self):
        return "\n".join(["".join(row) for row in self._screen])


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # Specifically, the sprite is 3 pixels wide, and the X register sets the
    # horizontal position of the middle of that sprite.

    # You count the pixels on the CRT: 40 wide and 6 high. This CRT screen
    # draws the top row of pixels left-to-right, then the row below that, and
    # so on. The left-most pixel in each row is in position 0, and the
    # right-most pixel in each row is in position 39.

    # the CRT draws a single pixel during each cycle. Representing each pixel
    # of the screen as a `#`. If the sprite is positioned such that one of its
    # three pixels is the pixel currently being drawn, the screen produces a
    # lit pixel (#); otherwise, the screen leaves the pixel dark (.).

    # Render the image given by your program. What eight capital letters appear
    # on your CRT?

    program = Program(lines)
    crt = CRT(40, 6)
    while program.is_running():
        program.run()
        crt.render(program.cycle, program.previous_register)

    solution = str(crt)
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
