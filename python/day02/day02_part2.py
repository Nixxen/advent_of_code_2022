RUN_TEST = False
TEST_SOLUTION = 12
TEST_INPUT_FILE = "test_input_day_02.txt"
INPUT_FILE = "input_day_02.txt"

ARGS = []


def main_part2(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # The Elf finishes helping with the tent and sneaks back over to you.
    # "Anyway, the second column says how the round needs to end: X means you
    # need to lose, Y means you need to end the round in a draw, and Z means
    # you need to win. Good luck!"

    # Following the Elf's instructions for the second column, what would your
    # total score be if everything goes exactly according to your strategy
    # guide?
    equivalences = {
        "A": "Rock",
        "B": "Paper",
        "C": "Scissor",
        "X": "Lose",
        "Y": "Draw",
        "Z": "Win",
    }
    scores = {
        "Rock": 1,
        "Paper": 2,
        "Scissor": 3,
    }
    score = 0
    for line in lines:
        them, me = line.split(" ")
        if equivalences[me] == "Draw":
            score += 3 + scores[equivalences[them]]
        elif equivalences[me] == "Lose":
            mod_score = (scores[equivalences[them]] - 1) % 3
            score += 0 + (3 if mod_score == 0 else mod_score)
        elif equivalences[me] == "Win":
            mod_score = (scores[equivalences[them]] + 1) % 3
            score += 6 + (3 if mod_score == 0 else mod_score)

    solution = score
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part2(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part2(INPUT_FILE, *ARGS)
        print(solution)
