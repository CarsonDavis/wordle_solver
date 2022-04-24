from statistics import mean
from typing import List, Tuple

from solver import Game, Tester

word_list = Game().possible_words

guesses_log: List[Tuple[str, int]] = []
for index, word in enumerate(word_list):
    tester = Tester(word)
    number_guesses = tester.play_game(print_on=False, first_guess='resin', second_guess='loath')
    guesses_log.append((word, number_guesses))
    if index % 50 == 0:
        print(index, mean([guess[1] for guess in guesses_log]))

# print(guesses_log)
print('final score', mean([guess[1] for guess in guesses_log]))
