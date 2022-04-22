from solver import Tester, Game
from nltk.corpus import words
from statistics import mean

word_list = Game().possible_words

guesses_log = []
for index, word in enumerate(word_list):
    if index // 50:
        print(index, mean([guess[1] for guess in guesses_log]))
    tester = Tester(word)
    number_guesses = tester.play_game(print_on=False)
    guesses_log.append((word, number_guesses))

# print(guesses_log)
print('final score', mean([guess[1] for guess in guesses_log]))
