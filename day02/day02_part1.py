RUN_TEST = False
TEST_SOLUTION = 15
TEST_INPUT_FILE = "test_input_day_02.txt"
INPUT_FILE = "input_day_02.txt"

ARGS = []


def main_part1(
    input_file,
):
    with open(input_file) as file:
        lines = list(map(lambda line: line.rstrip(), file.readlines()))

    # The score for a single round is the score for the shape you selected (1
    # for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome
    # of the round (0 if you lost, 3 if the round was a draw, and 6 if you
    # won).

    # For example, suppose you were given the following strategy guide:

    # A Y
    # B X
    # C Z
    # This strategy guide predicts and recommends the following:

    # In the first round, your opponent will choose Rock (A), and you should
    # choose Paper (Y). This ends in a win for you with a score of 8 (2 because
    # you chose Paper + 6 because you won). In the second round, your opponent
    # will choose Paper (B), and you should choose Rock (X). This ends in a
    # loss for you with a score of 1 (1 + 0). The third round is a draw with
    # both players choosing Scissors, giving you a score of 3 + 3 = 6. In this
    # example, if you were to follow the strategy guide, you would get a total
    # score of 15 (8 + 1 + 6).

    # What would your total score be if everything goes exactly according to
    # your strategy guide?


    equivalences = {
        "A": "Rock",
        "B": "Paper",
        "C": "Scissor",
        "X": "Rock",
        "Y": "Paper",
        "Z": "Scissor",
    }
    scores = {
        "Rock": 1,
        "Paper": 2,
        "Scissor": 3,
    }
    score = 0
    for line in lines:
        them, me = line.split(" ")
        if equivalences[them] == equivalences[me]: # Draw
            score += 3 + scores[equivalences[me]]
        elif (
            (equivalences[them] == "Rock" and equivalences[me] == "Scissor")
            or (equivalences[them] == "Paper" and equivalences[me] == "Rock")
            or (equivalences[them] == "Scissor" and equivalences[me] == "Paper")
        ): # They win
            score += 0 + scores[equivalences[me]]
        else: # I win
            score += 6 + scores[equivalences[me]]


    solution = score
    return solution


if __name__ == "__main__":
    if RUN_TEST:
        solution = main_part1(TEST_INPUT_FILE, *ARGS)
        print(solution)
        assert TEST_SOLUTION == solution
    else:
        solution = main_part1(INPUT_FILE, *ARGS)
        print(solution)
