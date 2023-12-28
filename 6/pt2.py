from math import sqrt, ceil, prod
from dataclasses import dataclass
from pathlib import Path
import logging


@dataclass
class Race:
    time: int  # ms
    record: int  # mm


@dataclass
class RaceResult:
    race: Race
    accel_times: range

    @property
    def no_winning(self) -> int:
        return len(self.accel_times)


def extract_num(input_file_line: str) -> int:
    line = input_file_line.replace(" ", "")
    words = line.split(":")
    return int(words[1])


def find_winning(time: int, record: int) -> range:
    """
    Race(time=7, record=9)
    - 7ms
    - 9mm
    - accel = 1mm/ms/ms

    dist = accel * accel_time * (time - accel_time)
    [mm] = [ms]  * [mm/ms/ms] * [ms]

    --> solve for accel_time where dist >= record
    9 <= accel_time * (7 - accel_time)
    accel_time = (1.7, 5.3) --> [2,6) = range(2, 6, 1)

    200 <= accel_time * (30 - accel_time)
    accel_time = (10.0, 20.0) --> [11,20) = range(11, 20, 1)

    record <= accel_time * (time - accel_time)
    record <= time * accel_time  - accel_time^2
    0 <  - accel_time^2 + time * accel_time - record
    0 >  accel_time^2 - time * accel_time + record
    a = 1, b = -time, c = record
    0 > (accel_time - x1)(accel_time - x2)
    x1 = (-b + sqrt(b^2 - 4ac)) / 2a = (time + sqrt(time^2 - 4*record))/2
    x2 = (-b - sqrt(b^2 - 4ac)) / 2a = (time - sqrt(time^2 - 4*record))/2
    """
    accel_time_max = (time + sqrt(time**2 - 4 * record)) / 2
    accel_time_min = (time - sqrt(time**2 - 4 * record)) / 2

    if int(accel_time_min) == accel_time_min:
        accel_time_min = int(accel_time_min + 1)
    else:
        accel_time_min = ceil(accel_time_min)

    accel_time_max = ceil(accel_time_max)

    return range(accel_time_min, accel_time_max, 1)


def main():
    input_file_name = "input.txt"
    TEST = False
    if TEST:
        input_file_name = "example_input.txt"
        logging.basicConfig(level=logging.DEBUG)
    input_file = Path(__file__).parent / input_file_name
    input_file_contents = input_file.read_text()
    input_file_lines = input_file_contents.split("\n")
    time = extract_num(input_file_lines[0])
    distance = extract_num(input_file_lines[1])
    race = Race(time, distance)
    race_result = RaceResult(race, find_winning(race.time, race.record))
    no_winning = race_result.no_winning
    result = no_winning
    print(f"{result=}")


if __name__ == "__main__":
    main()
