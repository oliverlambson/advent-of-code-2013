import re
from pathlib import Path
import logging


RawMatrix = list[list[str]]
Mask = list[list[int | bool | None]]


def get_number_mask(raw_matrix: RawMatrix, number_chars: list[str]) -> Mask:
    number = 0
    prev_char = False
    number_mask = []
    for j, line in enumerate(raw_matrix):
        number_mask.append([])
        for char in line:
            is_char = char in number_chars
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
    raw_matrix: RawMatrix, loc: tuple[int, int], symbols: list[str]
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


def get_numbers(raw_matrix: RawMatrix) -> list[int]:
    numbers = []
    for line in raw_matrix:
        text = "".join(line)
        ns = re.findall(r"(\d+)", text)
        for n in ns:
            numbers.append(int(n))

    return numbers


def get_symbol_indices(
    raw_matrix: RawMatrix, symbols: list[str]
) -> list[tuple[int, int]]:
    symbol_indices = []
    for j, line in enumerate(raw_matrix):
        for i, element in enumerate(line):
            if element in symbols:
                symbol_indices.append((i, j))
    return symbol_indices


def get_surrounding_number_indices(
    number_mask: Mask,
    symbol_indices: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    i_min = 0
    i_max = len(number_mask[0]) - 1
    j_min = 0
    j_max = len(number_mask) - 1
    surrounding_numbers = []
    for i_loc, j_loc in symbol_indices:
        i_vals = [i_loc + v for v in range(-1, 2, 1) if (i_min <= i_loc + v <= i_max)]
        j_vals = [j_loc + v for v in range(-1, 2, 1) if (j_min <= j_loc + v <= j_max)]

        surrounding_number_set = set()
        for j in j_vals:
            for i in i_vals:
                if i == i_loc and j == j_loc:
                    continue
                val = number_mask[j][i]
                if isinstance(val, int) and val is not True and val is not False:
                    surrounding_number_set.add(val)
        surrounding_numbers.append(tuple(surrounding_number_set))
    invalid_surrounding_numbers = list(
        filter(lambda x: len(x) > 2, surrounding_numbers)
    )
    if len(invalid_surrounding_numbers) != 0:
        raise Exception(">2 numbers found connected to symbol")
    surrounding_numbers = list(filter(lambda x: len(x) == 2, surrounding_numbers))
    return surrounding_numbers


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
    symbols = ["*"]
    number_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    numbers = get_numbers(raw_matrix)
    number_mask = get_number_mask(raw_matrix, number_chars=number_chars)
    symbol_indices = get_symbol_indices(raw_matrix, symbols=symbols)
    surrounding_number_indices = get_surrounding_number_indices(
        number_mask, symbol_indices
    )
    surrounding_numbers = [
        [numbers[i - 1], numbers[j - 1]] for i, j in surrounding_number_indices
    ]
    gear_ratios = [x * y for x, y in surrounding_numbers]
    s = sum(gear_ratios)
    print(s)


if __name__ == "__main__":
    main()
