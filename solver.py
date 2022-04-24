import random
from typing import List, Set, Tuple

from nltk.corpus import words

# define some custom types
GuessResults = List[Tuple[str, str]]
GameState = List[GuessResults]


class Position:
    def __init__(self):
        self.possible_letters = {letter for letter in "abcdefghijklmnopqrstuvwxyz"}

    def remove_letter(self, letter: str):
        self.possible_letters.discard(letter)

    def __repr__(self):
        return "".join(self.possible_letters)


class Game:
    def __init__(self, word_length: int = 5, word_list_source: str = 'official') -> None:
        self.positions = [Position() for _ in range(0, word_length)]
        self.possible_words = self.generate_initial_word_list(word_list_source, word_length)
        self.required_letters: Set[str] = set()
        self.game_state: GameState = []

    def load_word_list_file(self, file_name: str) -> List[str]:
        with open(file_name, 'r') as f:
            word_list = [word.strip().lower() for word in f.readlines()]
        return word_list

    def generate_initial_word_list(self, source: str, word_length: int) -> List[str]:
        if source == 'official':
            word_list = self.load_word_list_file('official_word_list.txt')
        elif source == 'knuth':
            word_list = self.load_word_list_file('knuth_words.txt')
        elif source == 'nltk':
            word_list = [word.lower() for word in words.words() if len(word) == word_length]
        else:
            raise ValueError(f"Invalid word list source: {source}")

        return word_list

    def add_turn(self, guess_results: GuessResults) -> None:
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

    def reduce_possible_words(self) -> None:
        self.possible_words = [
            word for word in self.possible_words if self.word_has_required_letters(word)
        ]
        for index, position in enumerate(self.positions):
            self.possible_words = [
                word for word in self.possible_words if word[index] in position.possible_letters
            ]

    def word_has_required_letters(self, word: str) -> bool:
        for letter in self.required_letters:
            if letter not in word:
                return False
        return True

    def __repr__(self) -> str:
        return '\n'.join([position.__str__() for position in self.positions])


class Tester:
    def __init__(self, answer: str) -> None:
        self.answer = answer
        self.game = Game()
        self.number_of_guesses = 0

    def make_guess(self) -> str:
        return random.choice(tuple(self.game.possible_words))

    def evaluate_guess(self, guess: str) -> GuessResults:
        guess_results = []
        for index, guess_letter in enumerate(guess):
            if guess_letter == self.answer[index]:
                guess_results.append((guess_letter, "right"))
            elif guess_letter in self.answer:
                guess_results.append((guess_letter, "position"))
            elif guess_letter not in self.answer:
                guess_results.append((guess_letter, "wrong"))

        return guess_results

    def play_game(
        self, print_on: bool = False, first_guess: str = None, second_guess: str = None
    ) -> int:
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
            self.play_game(print_on, first_guess, second_guess)

        return self.number_of_guesses
