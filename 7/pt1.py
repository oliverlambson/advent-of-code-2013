from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
import logging
from pathlib import Path


CARD_RANK = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


@dataclass(frozen=True)
class Card:
    value: str

    def __post_init__(self) -> None:
        if self.value not in CARD_RANK:
            raise ValueError("Invalid card value")

    @property
    def rank(self) -> int:
        return rank_card(self)

    def __eq__(self, other) -> bool:
        return self.rank == other.rank

    def __lt__(self, other) -> bool:
        return self.rank < other.rank

    def __hash__(self) -> int:
        return hash(self.value)


def rank_card(card: Card) -> int:
    return -CARD_RANK.index(card.value)


@dataclass(frozen=True)
class Hand:
    value: list[Card]

    def __post_init__(self):
        if len(self.value) != 5:
            raise ValueError("A hand must have 5 cards")

    @property
    def grouped(self) -> list[tuple[Card, int]]:
        return Counter(self.value).most_common()

    @property
    def rank(self) -> int:
        return rank_hand(self)

    def __eq__(self, other) -> bool:
        return self.rank == other.rank and self.value == other.value

    def __lt__(self, other) -> bool:
        if self.rank == other.rank:
            for self_card, other_card in zip(self.value, other.value, strict=True):  # type: ignore
                if self_card == other_card:
                    continue
                return self_card < other_card
            return False

        return self.rank < other.rank

    def __hash__(self) -> int:
        return hash(self.value)


class HandRank(IntEnum):
    FIVE_OF_A_KIND = 0
    FOUR_OF_A_KIND = -1
    FULL_HOUSE = -2
    THREE_OF_A_KIND = -3
    TWO_PAIR = -4
    ONE_PAIR = -5
    HIGH_CARD = -6


def rank_hand(hand: Hand) -> HandRank:
    counts = hand.grouped
    first_count = counts[0][1]
    match first_count:
        case 5:
            return HandRank.FIVE_OF_A_KIND
        case 4:
            return HandRank.FOUR_OF_A_KIND
        case 3:
            second_count = counts[1][1]
            if second_count == 2:
                return HandRank.FULL_HOUSE
            else:
                return HandRank.THREE_OF_A_KIND
        case 2:
            second_count = counts[1][1]
            if second_count == 2:
                return HandRank.TWO_PAIR
            else:
                return HandRank.ONE_PAIR
        case 1:
            return HandRank.HIGH_CARD
        case _:
            raise ValueError("Invalid hand")


def text_to_hand(text: str) -> Hand:
    if len(text) != 5:
        raise ValueError("A hand must have 5 cards")
    return Hand([Card(c) for c in text])


@dataclass(frozen=True)
class Play:
    hand: Hand
    bid: int


def line_to_play(line: str) -> Play:
    hand_text, bid_text = line.split(" ")
    return Play(text_to_hand(hand_text), int(bid_text))


def score_game(game: list[Play]) -> int:
    sorted_game = sorted(game, key=lambda play: play.hand)
    scores = [(i + 1) * play.bid for i, play in enumerate(sorted_game)]
    return sum(scores)


def main():
    input_file_name = "input.txt"
    TEST = False
    if TEST:
        input_file_name = "example_input.txt"
        logging.basicConfig(level=logging.DEBUG)
    input_file = Path(__file__).parent / input_file_name
    input_file_contents = input_file.read_text().strip()
    input_file_lines = input_file_contents.split("\n")
    game = [line_to_play(line) for line in input_file_lines]
    score = score_game(game)
    print(f"{score=}")


if __name__ == "__main__":
    main()
