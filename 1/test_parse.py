def test_extract():
    from pt2 import parse_line

    line = "height33twone"
    first_expected = "eight"
    last_expected = "one"
    numbers = parse_line(line)
    first = numbers[0]
    last = numbers[-1]
    assert first == first_expected
    assert last == last_expected
    assert True


def test_parse_line():
    from pt2_sidequest import parse_line

    line = "height2one9"
    line_masked_expected = "------2one9"
    parsed_expected = ["height", "2", "one", "9"]
    line_masked, parsed = parse_line(line)
    assert line_masked == line_masked_expected
    assert parsed == parsed_expected
    assert True


if __name__ == "__main__":
    test_extract()
    # test_parse_line()
