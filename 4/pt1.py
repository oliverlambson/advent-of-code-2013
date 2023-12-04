import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Card:
    number: int
    winning: list[int]
    actual: list[int]


def parse_line(line: str) -> Card:
    expression = r"^Card\s+(\d+):\s(.*)\s\|\s(.*)$"
    match = re.fullmatch(expression, line)
    if match is None:
        raise ValueError(f"Invalid line: {line}")
    card_number_str, winning_str, actual_str = match.groups()

    card_number = int(card_number_str)
    winning_str = winning_str.strip()
    actual_str = actual_str.strip()

    winning_numbers = [int(x) for x in re.findall(r"\b\d+\b", winning_str)]
    actual_numbers = [int(x) for x in re.findall(r"\b\d+\b", actual_str)]

    return Card(card_number, winning_numbers, actual_numbers)


def get_score(card: Card) -> int:
    winning_numbers = set(card.winning)
    actual_numbers = set(card.actual)
    scoring_numbers = winning_numbers & actual_numbers
    n_scoring_numbers = len(scoring_numbers)
    if n_scoring_numbers == 0:
        return 0
    score = 2 ** (n_scoring_numbers - 1)
    return score


def main():
    input_file_name = "input.txt"
    TEST = False
    if TEST:
        input_file_name = "example_input.txt"
    input_file = Path(__file__).parent / input_file_name
    total_score = 0
    with input_file.open() as f:
        for line in f:
            line = line.strip()
            card = parse_line(line)
            score = get_score(card)
            total_score += score

    print(f"Total score: {total_score}")


if __name__ == "__main__":
    main()
