from pprint import pprint
from pathlib import Path
import logging

RawMatrix = list[list[str]]
Mask = list[list[int | None]]


def get_number_mask(raw_matrix: RawMatrix) -> Mask:
    number = -1
    prev_char = False
    number_mask = []
    for j, line in enumerate(raw_matrix):
        number_mask.append([])
        for char in line:
            is_char = char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            if is_char:
                if not prev_char:
                    number += 1
                mask = number
            else:
                mask = None
            number_mask[j].append(mask)
            prev_char = is_char
    return number_mask


def has_symbol_neighbor(
    raw_matrix: RawMatrix, loc: tuple[int, int], symbols: list[str]
) -> bool:
    i_min = 0
    i_max = len(raw_matrix[0])
    j_min = 0
    j_max = len(raw_matrix)

    i_loc = loc[0]
    j_loc = loc[1]

    i_vals = [
        i_loc + v for v in range(-1, 2, 1) if (i_min <= i_loc + v <= i_max) and (v != 0)
    ]
    j_vals = [
        j_loc + v for v in range(-1, 2, 1) if (j_min <= j_loc + v <= j_max) and (v != 0)
    ]

    for j in j_vals:
        for i in i_vals:
            val = raw_matrix[j][i]
            if val in symbols:
                return True

    return False


def get_symbol_neighbor_mask(raw_matrix: RawMatrix, symbols: list[str]) -> Mask:
    symbol_neighbor_mask = []
    for j, line in enumerate(raw_matrix):
        symbol_neighbor_mask.append([])
        for i, _ in enumerate(line):
            mask = has_symbol_neighbor(raw_matrix, (i, j), symbols)
            symbol_neighbor_mask[j].append(mask)
    return symbol_neighbor_mask


def main():
    # config
    input_file_name = "input.txt"
    TEST = True
    if TEST:
        input_file_name = "example_input.txt"
        logging.basicConfig(level=logging.DEBUG)
    input_file = Path(__file__).parent / input_file_name

    with input_file.open() as f:
        raw_matrix: RawMatrix = []
        for line in f:
            raw_matrix.append(list(line.strip()))

    # evaluate games


if __name__ == "__main__":
    main()
