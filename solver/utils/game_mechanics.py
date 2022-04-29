import random
from typing import List, Literal, Set, Tuple

from nltk.corpus import words


# define some custom types
ResultChoices = Literal['position', 'correct', 'wrong']
GuessResults = List[Tuple[str, ResultChoices]]
GameState = List[GuessResults]


class Position:
    def __init__(self):
        """Position is initialized with the entire alphabet"""
        self.possible_letters = {letter for letter in "abcdefghijklmnopqrstuvwxyz"}

    def remove_letter(self, letter: str):
        """Removes a specific letter from the list of possibilities for the position"""
        self.possible_letters.discard(letter)

    def __repr__(self) -> str:
        """Returns a string of each possible letter"""
        return "".join(self.possible_letters)


class Game:
    def __init__(self, word_length: int = 5, word_list_source: str = 'official') -> None:
        self.positions = [Position() for _ in range(0, word_length)]
        self.original_word_list = self.generate_initial_word_list(word_list_source, word_length)
        self.possible_words = self.original_word_list.copy()
        self.required_letters: Set[str] = set()
        self.game_state: GameState = []

    def load_word_list_file(self, file_name: str) -> List[str]:
        """Opens a word list file saved to disk and returns the words as a list of strings"""
        with open(file_name, 'r') as f:
            word_list = [word for word in f.readlines()]
        return word_list

    def generate_initial_word_list(self, source: str, word_length: int) -> List[str]:
        """Loads a word list from file or from library, cleans it of spaces, filters for word
        length, and returns the list of strings"""

        if source == 'official':
            word_list = self.load_word_list_file('solver/utils/word_lists/official_word_list.txt')
        elif source == 'knuth':
            word_list = self.load_word_list_file('solver/utils/word_lists/knuth_words.txt')
        elif source == 'nltk':
            word_list = words.words()
        else:
            raise ValueError(
                f"Invalid word list source: {source}. Accepted choices are 'official', 'knuth', and 'nltk'."
            )

        clean_word_list = []
        for word in word_list:
            word = word.strip().lower()
            if len(word) == word_length:
                clean_word_list.append(word)

        return clean_word_list

    def update_position_data(self, guess_results: GuessResults) -> None:
        """Takes the results from a guess and updates the self.required_letters and
        self.position.possible_letters."""

        for index, (guess_letter, guess_result) in enumerate(guess_results):

            if guess_result == "wrong":
                [position.remove_letter(guess_letter) for position in self.positions]

            elif guess_result == "right":
                self.positions[index].possible_letters = {guess_letter}
                # these could technically also be added to self.required_letters, but that would
                # be redundant and increase runtime, since remove_words_with_wrong letters will
                # catch all information obtained from this elif block

            elif guess_result == "position":
                self.positions[index].remove_letter(guess_letter)
                self.required_letters.add(guess_letter)

            else:
                raise ValueError(f"guess result must be one of {GuessResults}")

        self.game_state.append(guess_results)

    def update_possible_words(self):
        """Uses self.required_letters and self.position.possible_letters to parse down
        the list of self.possible_words"""

        self.remove_words_with_wrong_letters()
        self.remove_words_without_required_letters()

        return self.possible_words

    def word_has_required_letters(self, word: str) -> bool:
        """Evaluates whether a word contains every required letter."""

        for letter in self.required_letters:
            if letter not in word:
                return False
        return True

    def remove_words_without_required_letters(self) -> None:
        """Removes any words which lack a letter that was known to be in the word
        but who's position was unknown.
        """

        self.possible_words = [
            word for word in self.possible_words if self.word_has_required_letters(word)
        ]

    def remove_words_with_wrong_letters(self) -> None:
        """Removes any words which have a letter in a position that is not listed
        in that position's possible letters.
        """

        for index, position in enumerate(self.positions):
            self.possible_words = [
                word for word in self.possible_words if word[index] in position.possible_letters
            ]

    def __repr__(self) -> str:
        return '\n'.join([position.__str__() for position in self.positions])


class Tester:
    def __init__(self, answer: str) -> None:
        self.answer = answer
        self.game = Game()
        self.number_of_guesses = 0

    def make_guess(self) -> str:
        """Randomly choose a word from the possible words"""

        return random.choice(tuple(self.game.possible_words))

    def evaluate_guess(self, guess: str) -> GuessResults:
        """Take a guess and compare it with the answer to generate GuessResults"""

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
        """Play the game, making guesses and decreasing the possible word space until
        the correct answer is found, then return number of guesses it took"""

        self.number_of_guesses += 1
        if self.number_of_guesses == 1 and first_guess:
            guess = first_guess
        elif self.number_of_guesses == 2 and second_guess:
            guess = second_guess
        else:
            guess = self.make_guess()

        if guess == self.answer:
            if print_on:
                print(f'{guess} was correct!')
        else:
            guess_results = self.evaluate_guess(guess)
            self.game.update_position_data(guess_results)
            self.game.update_possible_words()
            if print_on:
                print(f"{guess} {len(self.game.possible_words)} remaining")
            self.play_game(print_on, first_guess, second_guess)

        return self.number_of_guesses
