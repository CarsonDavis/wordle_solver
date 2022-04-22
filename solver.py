from nltk.corpus import words
import random


class Position:
    def __init__(self):
        self.possible_letters = {letter for letter in "abcdefghijklmnopqrstuvwxyz"}

    def remove_letter(self, letter):
        self.possible_letters.discard(letter)

    def __repr__(self):
        return "".join(self.possible_letters)


class Game:
    def __init__(self, word_length=5, word_list_source='official'):
        self.positions = [Position() for _ in range(0, word_length)]
        self.possible_words = self.load_word_list(word_list_source, word_length)
        self.required_letters = set()
        self.game_state = []

    def load_word_list(self, source, word_length):
        if source == 'official':
            with open('official_word_list.txt', 'r') as f:
                return [word.strip() for word in f.readlines()]
        else:
            return [word.lower() for word in words.words() if len(word) == word_length]

    def add_turn(self, guess_results):
        for index, (guess_letter, guess_result) in enumerate(guess_results):

            if guess_result == "wrong":
                [position.remove_letter(guess_letter) for position in self.positions]

            elif guess_result == "right":
                self.positions[index].possible_letters = {guess_letter}

            elif guess_result == "position":
                self.positions[index].remove_letter(guess_letter)
                self.required_letters.add(guess_letter)

        self.reduce_possible_words()
        self.game_state.append(guess_results)

    def reduce_possible_words(self):
        self.possible_words = [
            word for word in self.possible_words if self.word_has_required_letters(word)
        ]
        for index, position in enumerate(self.positions):
            self.possible_words = [
                word for word in self.possible_words if word[index] in position.possible_letters
            ]

    def word_has_required_letters(self, word):
        for letter in self.required_letters:
            if letter not in word:
                return False
        return True

    def __repr__(self):
        return self.positions


class Tester:
    def __init__(self, answer):
        self.answer = answer
        self.game = Game()
        self.number_of_guesses = 0

    def make_guess(self):
        return random.choice(tuple(self.game.possible_words))

    def evaluate_guess(self, guess):
        guess_results = []
        for index, guess_letter in enumerate(guess):
            if guess_letter == self.answer[index]:
                guess_results.append((guess_letter, "right"))
            elif guess_letter in self.answer:
                guess_results.append((guess_letter, "position"))
            elif guess_letter not in self.answer:
                guess_results.append((guess_letter, "wrong"))

        return guess_results

    def play_game(self, print_on=False, first_guess=None, second_guess=None):
        guess = self.make_guess()
        self.number_of_guesses += 1
        if first_guess and self.number_of_guesses == 1:
            guess = first_guess
        elif second_guess and self.number_of_guesses == 2:
            guess = second_guess

        if guess == self.answer:
            if print_on:
                print(f'{guess} was correct!')
        else:
            guess_results = self.evaluate_guess(guess)
            self.game.add_turn(guess_results)
            if print_on:
                print(f"{guess} {len(self.game.possible_words)} remaining")
            self.play_game(print_on)

        return self.number_of_guesses
