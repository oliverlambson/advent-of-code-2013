import re
from pathlib import Path
import logging

import numpy as np

RawMatrix = list[list[str]]
Mask = list[list[int | bool | None]]


def get_number_mask(raw_matrix: RawMatrix) -> Mask:
    number = 0
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
                mask = False
            number_mask[j].append(mask)
            prev_char = is_char
    return number_mask


def has_symbol_neighbor(
    raw_matrix: RawMatrix, loc: tuple[int, int], not_symbols: list[str]
) -> bool:
    i_min = 0
    i_max = len(raw_matrix[0]) - 1
    j_min = 0
    j_max = len(raw_matrix) - 1

    i_loc = loc[0]
    j_loc = loc[1]

    i_vals = [i_loc + v for v in range(-1, 2, 1) if (i_min <= i_loc + v <= i_max)]
    j_vals = [j_loc + v for v in range(-1, 2, 1) if (j_min <= j_loc + v <= j_max)]

    for j in j_vals:
        for i in i_vals:
            if i == i_loc and j == j_loc:
                continue
            val = raw_matrix[j][i]
            if val not in not_symbols:
                return True

    return False


def get_symbol_neighbor_mask(raw_matrix: RawMatrix, not_symbols: list[str]) -> Mask:
    symbol_neighbor_mask = []
    for j, line in enumerate(raw_matrix):
        symbol_neighbor_mask.append([])
        for i, _ in enumerate(line):
            mask = has_symbol_neighbor(raw_matrix, (i, j), not_symbols)
            symbol_neighbor_mask[j].append(mask)
    return symbol_neighbor_mask


def apply_mask(target: Mask, mask: Mask) -> Mask:
    result_mask = []
    for j, (target_line, mask_line) in enumerate(zip(target, mask)):
        result_mask.append([])
        for i, (target_element, mask_element) in enumerate(zip(target_line, mask_line)):
            result_mask[j].append(mask_element and target_element)
    return result_mask


def get_valid_number_indices(mask: Mask) -> set[int]:
    valid_number_indices = set()
    for line in mask:
        for element in line:
            if element:
                valid_number_indices.add(element)
    return valid_number_indices


def get_numbers(raw_matrix: RawMatrix) -> list[int]:
    numbers = []
    for line in raw_matrix:
        text = "".join(line)
        ns = re.findall(r"(\d+)", text)
        for n in ns:
            numbers.append(int(n))

    return numbers


def get_valid_numbers(numbers: list[int], valid_number_indices: set[int]) -> list[int]:
    valid_numbers = [n for i, n in enumerate(numbers) if i + 1 in valid_number_indices]
    return valid_numbers


def main():
    # config
    input_file_name = "input.txt"
    TEST = False
    if TEST:
        input_file_name = "example_input.txt"
        logging.basicConfig(level=logging.DEBUG)
    input_file = Path(__file__).parent / input_file_name

    with input_file.open() as f:
        raw_matrix: RawMatrix = []
        for line in f:
            raw_matrix.append(list(line.strip()))

    # evaluate
    not_symbols = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
    number_mask = get_number_mask(raw_matrix)
    symbol_neighbor_mask = get_symbol_neighbor_mask(raw_matrix, not_symbols=not_symbols)
    valid_numbers_mask = apply_mask(number_mask, symbol_neighbor_mask)
    valid_number_indices = get_valid_number_indices(valid_numbers_mask)
    numbers = get_numbers(raw_matrix)
    valid_numbers = get_valid_numbers(numbers, valid_number_indices)
    s = sum(valid_numbers)
    print(s)


if __name__ == "__main__":
    main()
