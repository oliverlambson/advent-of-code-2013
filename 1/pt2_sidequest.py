"""
I accidentally thought that I needed to parse as humans read: e.g. "height" wouldn't count as "eight".
"""
import json
from pathlib import Path
import re

# filepath = "test_input_2.txt"
filepath = "input.txt"

words_file = Path("words_dictionary.json")

with open(words_file) as file:
    words_dictionary = json.load(file)
    all_words = list(words_dictionary.keys())

number_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
number_words = list(number_map.keys())

words = [w for w in all_words if w not in number_words]
words = all_words


def parse_line(
    line: str,
    position: int = 0,
    parsed: list | None = None,
    line_masked: str | None = None,
) -> tuple[str, list]:
    if line_masked is None:
        line_masked = line
    if parsed is None:
        parsed = []

    if len(line) == 0:
        raise Exception("len(line) == 0")

    if position >= len(line):
        if parsed is None:
            raise Exception("parsed is None")
        return line_masked, parsed

    partial = line[position:]
    token = re.match(f"^({'|'.join(words)})", partial)
    if token is not None:
        match = token.group(0)
        match_len = len(match)

        if match not in number_words:
            partial_masked = "-" * match_len + partial.lstrip(match)
            line_masked = line_masked[:position] + partial_masked

        parsed.append(line[position : position + match_len])
        position += match_len
    else:
        parsed.append(line[position])
        position += 1

    return parse_line(line, position, parsed, line_masked)


def convert_number_word_to_number(number_word: str) -> str:
    return str(number_map.get(number_word, number_word))


def main():
    sum = 0
    data = []
    for line in open(filepath):
        numbers = re.findall(f"(\\d|{'|'.join(number_words)})", line)
        if len(numbers) == 0:
            raise Exception(f"Expected 2 numbers, got {len(numbers)}")

        first = numbers[0]
        last = numbers[-1]
        number = int(
            convert_number_word_to_number(first) + convert_number_word_to_number(last)
        )
        data.append((line.strip(), numbers, first, last, number))
        # print(line.strip(), end="")
        # print(f": {first} + {last} = {number}")
        sum += number

        numbers = None
        first = None
        last = None
        number = None

    print(sum)
    # sorted(data, key=lambda x: len(x[1]))


if __name__ == "__main__":
    main()
