from functools import reduce
from solver_utils import *
import os.path
import pickle


def main():
    if not os.path.isfile('data/mappings/first_guess_mappings.txt'):
        generate_first_mapping()

    with open('data/mappings/first_guess_mappings.txt', 'rb') as f:
        first_guess_mappings = pickle.load(f)

    result = first_guess_mappings
    while result:
        result = run_one_iteration(result)


def run_one_iteration(guess_mappings):
    sorted_list = sorted(guess_mappings.items(),
                         key=lambda x: x[1][0], reverse=True)
    print('The current top 10 guesses and their corresponding expected entropy are:')
    for guess_entropy in sorted_list[:10]:
        word, (expected_entropy, _) = guess_entropy
        print(word, round(expected_entropy, 3))
    print()

    input_guess = input('Guess: ')
    input_pattern = tuple(map(lambda x: int(x), input('Pattern: ').split()))
    actual_entropy, possible_answers = guess_mappings[input_guess][1][input_pattern]
    print()
    print(f'Actual entropy:\n{actual_entropy}\n')
    print(
        f'Possible answers ({len(possible_answers)}):\n{" ".join(possible_answers)}\n')

    if len(possible_answers) == 1:
        print(f'FINAL ANSWER: {possible_answers[0]}\n')
        return False
    return calc_entropy(possible_answers)


if __name__ == "__main__":
    main()
