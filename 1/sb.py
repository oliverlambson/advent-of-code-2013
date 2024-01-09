from dataclasses import dataclass
import json
from pathlib import Path

words_file = Path("words_dictionary.json")

with open(words_file) as file:
    words_dictionary = json.load(file)
    ALL_WORDS = list(words_dictionary.keys())


@dataclass
class Word:
    word: str

    def __post_init__(self):
        self.word = self.word.lower()
        self.letters = sorted(set(self.word))

    def __str__(self) -> str:
        return self.word




def valid_word(letters: str, word: Word):
    if len(word.word) < 4:
        return False
    return all(letter in letters for letter in word.letters) and letters[-1] in word.letters

def main():
    letters = input("Enter letters (last == centre): ")
    TEST = False
    all_words = ALL_WORDS
    if TEST:
        all_words = ["a", "apple", "ant", "any", "allan"]
    words = [Word(word) for word in all_words]

    valid_words = list(filter(lambda word: valid_word(letters, word), words))
    print(", ".join([ word.word for word in valid_words ]))



if __name__ == "__main__":
    main()
