"""
only 12 red cubes, 13 green cubes, and 14 blue cubes
What is the sum of the IDs of those games?
"""
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
import re

input_file = Path(__file__).parent / "input.txt"


class Color(StrEnum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


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
