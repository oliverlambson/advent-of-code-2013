from pt2 import get_surrounding_numbers


def test_get_surrounding_numbers():
    n = False
    number_mask = [
        [1, 1, 1, n, n, 2, 2, 2, n, n],
        [n, n, n, n, n, n, n, n, n, n],
        [n, n, 3, 3, n, n, 4, 4, 4, n],
        [n, n, n, n, n, n, n, n, n, n],
        [5, 5, 5, n, n, n, n, n, n, n],
        [n, n, n, n, n, n, n, 6, 6, n],
        [n, n, 7, 7, 7, n, n, n, n, n],
        [n, n, n, n, n, n, 8, 8, 8, n],
        [n, n, n, n, n, n, n, n, n, n],
        [n, 9, 9, 9, n, 10, 10, 10, n, n],
    ]
    symbol_indices = [(3, 1), (3, 4), (5, 8)]
    expected_output = [{1, 3}, {5}, {8, 10}]
    output = get_surrounding_numbers(number_mask, symbol_indices)
    assert output == expected_output
