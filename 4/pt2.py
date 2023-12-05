from typing import Callable, overload
from functools import lru_cache
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Card:
    number: int
    winning: tuple[int, ...]  # use tuples instead of lists for hashability
    actual: tuple[int, ...]


@dataclass(frozen=True)
class ScoredCard:
    card: Card
    linked_card_numbers: tuple[int, ...]


def parse_line(line: str) -> Card:
    expression = r"^Card\s+(\d+):\s(.*)\s\|\s(.*)$"
    match = re.fullmatch(expression, line)
    if match is None:
        raise ValueError(f"Invalid line: {line}")
    card_number_str, winning_str, actual_str = match.groups()

    card_number = int(card_number_str)
    winning_str = winning_str.strip()
    actual_str = actual_str.strip()

    winning_numbers = tuple(int(x) for x in re.findall(r"\b\d+\b", winning_str))
    actual_numbers = tuple(int(x) for x in re.findall(r"\b\d+\b", actual_str))

    return Card(card_number, winning_numbers, actual_numbers)


def get_number_winning_numbers(card: Card) -> int:
    winning_numbers = set(card.winning)
    actual_numbers = set(card.actual)
    scoring_numbers = winning_numbers & actual_numbers
    score = len(scoring_numbers)
    return score


@lru_cache
def get_card_score(card_number: int, scored_cards: tuple[ScoredCard, ...]) -> int:
    if len(scored_cards) == 0:
        raise ValueError("No scored cards")
    first_card_number = scored_cards[0].card.number
    card_index = card_number - first_card_number

    scored_card = scored_cards[card_index]
    linked_card_numbers = scored_card.linked_card_numbers
    if len(linked_card_numbers) == 0:
        # score is itself
        return 1
    # score is itself plus linked cards plus their scores
    score = len(linked_card_numbers)
    for linked_card_number in linked_card_numbers:
        tmp = get_card_score(linked_card_number, scored_cards)
        score += tmp
    return score


def main():
    input_file_name = "input.txt"
    TEST = False
    if TEST:
        input_file_name = "example_input.txt"
    input_file = Path(__file__).parent / input_file_name
    scored_cards: list[ScoredCard] = []
    with input_file.open() as f:
        for line in f:
            line = line.strip()
            card = parse_line(line)
            n_winning_nos = get_number_winning_numbers(card)
            linked_card_numbers = tuple(
                range(card.number + 1, card.number + n_winning_nos + 1)
            )
            scored_card = ScoredCard(card, linked_card_numbers)
            scored_cards.append(scored_card)

    # since we always know that earlier cards are scored before later cards,
    # we can reverse the list and score from the end avoiding all recursion BS
    scored_cards_rev = reversed(scored_cards)
    lut = {}  # lookup table for later card scores
    score = 0
    for scored_card in scored_cards_rev:
        card_score = 1
        card_score += sum(lut[x] for x in scored_card.linked_card_numbers)
        lut[scored_card.card.number] = card_score
        score += card_score
    print(f"Total score: {score}")


if __name__ == "__main__":
    main()
