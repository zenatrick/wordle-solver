from math import log
from itertools import product
import pickle

CORRECT_LETTER_CORRECT_POSITION = 0
CORRECT_LETTER_WRONG_POSITION = 1
WRONG_LETTER = 2

all_patterns = list(product((CORRECT_LETTER_CORRECT_POSITION,
                             CORRECT_LETTER_WRONG_POSITION, WRONG_LETTER), repeat=5))


def entropy(p):
    if p == 0:
        return 'Inf'
    return -log(p, 2)


def filter_possible_answers(guess, pattern, words):
    guess_pattern = tuple(zip(guess, pattern))

    def is_possible_answer(word):
        # For each letter and its pattern status, check if any condition is broken
        for pos, (letter, status) in enumerate(guess_pattern):
            if status == CORRECT_LETTER_CORRECT_POSITION and letter != word[pos]:
                return False
            if status == CORRECT_LETTER_WRONG_POSITION:
                wrong_letter_count_before_current = sum(map(lambda x: 1, filter(
                    lambda letter_status: letter_status[0] == letter and letter_status[1] == WRONG_LETTER, guess_pattern[:pos])))

                if letter == word[pos] or wrong_letter_count_before_current > 0:
                    return False
            if status == WRONG_LETTER and letter == word[pos]:
                return False

            correct_letter_count = sum(map(lambda x: 1, filter(
                lambda letter_status: letter_status[0] == letter and letter_status[1] != WRONG_LETTER, guess_pattern)))
            wrong_letter_count = sum(map(lambda x: 1, filter(
                lambda letter_status: letter_status[0] == letter and letter_status[1] == WRONG_LETTER, guess_pattern)))

            if wrong_letter_count > 0 and word.count(letter) != correct_letter_count:
                return False
            if word.count(letter) < correct_letter_count:
                return False

        return True
    return list(filter(is_possible_answer, words))


def calc_prob_entropy_possible_answers(guess, pattern, current_possible_answers):
    filtered_possible_answers = filter_possible_answers(
        guess, pattern, current_possible_answers)
    p = len(filtered_possible_answers) / len(current_possible_answers)
    return p, entropy(p), filtered_possible_answers


def calc_expected_entropy_pattern_to_possible_answers(guess, current_possible_answers):
    pattern_to_possible_answers = {}
    expected_entropy = 0
    for pattern in all_patterns:
        p, entropy, possible_answers = calc_prob_entropy_possible_answers(
            guess, pattern, current_possible_answers)
        if p == 0:
            continue
        pattern_to_possible_answers[pattern] = (entropy, possible_answers)
        expected_entropy += p * entropy

    return expected_entropy, pattern_to_possible_answers


def calc_entropy(current_possible_answers):
    guess_to_expected_entropy_and_pattern_to_possible_answers = {}
    for guess in current_possible_answers:
        # print(f'Calculating entropy for {guess}')
        guess_to_expected_entropy_and_pattern_to_possible_answers[guess] = calc_expected_entropy_pattern_to_possible_answers(
            guess, current_possible_answers)
    return guess_to_expected_entropy_and_pattern_to_possible_answers


def generate_first_mapping():
    with open('data/words/possible_answers.txt', 'r') as f:
        possible_answers = f.read().splitlines()

    first_guess_mappings = calc_entropy(possible_answers)

    with open('data/mappings/first_guess_mappings.txt', 'wb+') as f:
        pickle.dump(first_guess_mappings, f)
