from pt1 import parse_line, get_score, Card


def test_parse_line():
    line = "Card   1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
    expected = Card(
        number=1, winning=[41, 48, 83, 86, 17], actual=[83, 86, 6, 31, 17, 9, 48, 53]
    )
    actual = parse_line(line)
    assert actual == expected


def test_get_score():
    input = Card(
        number=1, winning=[41, 48, 83, 86, 17], actual=[83, 86, 6, 31, 17, 9, 48, 53]
    )
    expected = 8
    actual = get_score(input)
    assert actual == expected

    input = Card(
        number=3, winning=[1, 21, 53, 59, 44], actual=[69, 82, 63, 72, 16, 21, 14, 1]
    )
    expected = 2
    actual = get_score(input)
    assert actual == expected

    input = Card(
        number=4, winning=[41, 92, 73, 84, 69], actual=[59, 84, 76, 51, 58, 5, 54, 83]
    )
    expected = 1
    actual = get_score(input)
    assert actual == expected

    input = Card(
        number=5, winning=[87, 83, 26, 28, 32], actual=[88, 30, 70, 12, 93, 22, 82, 36]
    )
    expected = 0
    actual = get_score(input)
    assert actual == expected
