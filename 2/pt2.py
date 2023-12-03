"""
The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
"""
import logging
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
import re


class Color(StrEnum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


SampleLimits = dict[Color, int]

SamplesByColor = dict[Color, list[int]]


@dataclass
class Sample:
    color: Color
    number: int


@dataclass
class SampleSet:
    samples: list[Sample]


@dataclass
class Game:
    number: int
    sample_sets: list[SampleSet]


def parse_sample(sample_text: str) -> Sample:
    """
    Parse a sample from a sample text
    in: "6 red"
    out: Sample(color="red", number=6)
    """
    match = re.match(r"(\d+) (\w+)", sample_text)
    if not match:
        raise ValueError(f"Could not parse sample from sample text: {sample_text}")
    number_text = match.group(1)
    assert isinstance(number_text, str)
    number = int(number_text)

    color_str = match.group(2)
    assert isinstance(color_str, str)
    color = Color(color_str)
    return Sample(color, number)


def parse_line(line: str) -> Game:
    """
    Parse a line of the input file

    in: "Game 15: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
    out: Game(number=15, samples=[Sample(color='red', number=6), ...])
    """
    match = re.match(r"^Game (\d+): (.*)$", line)
    if not match:
        raise ValueError(f"Could not parse game number from line: {line}")
    game_number = int(match.group(1))

    sample_texts: list[str] = match.group(2).split(";")
    if not sample_texts:
        raise ValueError(f"Could not parse samples from line: {line}")

    sample_sets = []
    for sample_text in sample_texts:
        sample_strings = [s.strip() for s in sample_text.split(",")]
        samples = [parse_sample(sample_string) for sample_string in sample_strings]
        sample_sets.append(SampleSet(samples))

    return Game(game_number, sample_sets)


def flatten_sample_sets(sample_sets: list[SampleSet]) -> SamplesByColor:
    samples_by_color: SamplesByColor = {color: [] for color in Color}
    for sample_set in sample_sets:
        for sample in sample_set.samples:
            samples_by_color[sample.color].append(sample.number)
    return samples_by_color


def get_power_of_game(game: Game) -> int:
    samples_by_color = flatten_sample_sets(game.sample_sets)
    min_samples_by_color: SampleLimits = {}
    power = 1
    for color, samples in samples_by_color.items():
        min_samples_by_color[color] = max(samples)
        power *= min_samples_by_color[color]
    return power


def get_power_of_games(games: list[Game]) -> int:
    power = sum(map(get_power_of_game, games))
    return power


def main():
    # config
    input_file_name = "input.txt"
    TEST = False
    if TEST:
        input_file_name = "example_input_2.txt"
        logging.basicConfig(level=logging.DEBUG)
    input_file = Path(__file__).parent / input_file_name

    # read games
    games: list[Game] = []
    with input_file.open() as f:
        for line in f:
            game = parse_line(line)
            games.append(game)

    # evaluate games
    power = get_power_of_games(games)
    print(power)


if __name__ == "__main__":
    main()
