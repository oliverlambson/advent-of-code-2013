import logging
import re

TEST = False
if TEST:
    logging.basicConfig(level=logging.DEBUG)
    filepath = "test_input_2.txt"

filepath = "input.txt"

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


def convert_number_word_to_number(number_word: str) -> str:
    return str(number_map.get(number_word, number_word))


def parse_line(line: str) -> list[str]:
    # capture group to get all overlapping matches
    numbers = list(re.finditer(f"(?=(\\d|{'|'.join(number_words)}))", line))
    if len(numbers) == 0:
        raise Exception(f"Expected 2 numbers, got {len(numbers)}")
    numbers = [n.group(1) for n in numbers]
    return numbers


def main():
    sum = 0
    data = []
    for line in open(filepath):
        numbers = parse_line(line)
        first = numbers[0]
        last = numbers[-1]
        number = int(
            convert_number_word_to_number(first) + convert_number_word_to_number(last)
        )
        data.append((line.strip(), numbers, first, last, number))
        logging.debug(f"{line.strip()}: {first} + {last} = {number}")
        sum += number

        numbers = None
        first = None
        last = None
        number = None

    print(f"{sum=}")


if __name__ == "__main__":
    main()
