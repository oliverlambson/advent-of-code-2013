from pt1 import (
    parse_line,
    is_sample_set_possible,
    Game,
    Sample,
    SampleSet,
    is_sample_possible,
    Color,
    SampleLimits,
)


def test_parse_line():
    input = "Game 15: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
    expected_output = Game(
        number=15,
        sample_sets=[
            SampleSet(
                [
                    Sample(color=Color("red"), number=6),
                    Sample(color=Color("blue"), number=1),
                    Sample(color=Color("green"), number=3),
                ]
            ),
            SampleSet(
                [
                    Sample(color=Color("blue"), number=2),
                    Sample(color=Color("red"), number=1),
                    Sample(color=Color("green"), number=2),
                ]
            ),
        ],
    )
    output = parse_line(input)
    assert output == expected_output


def test_is_sample_possible():
    sample_limits: SampleLimits = {
        Color.RED: 12,
        Color.GREEN: 13,
        Color.BLUE: 14,
    }
    sample_pass = Sample(color=Color("blue"), number=2)
    assert is_sample_possible(sample_pass, sample_limits) is True

    sample_fail = Sample(color=Color("green"), number=14)
    assert is_sample_possible(sample_fail, sample_limits) is False


def test_is_sample_set_possible():
    sample_limits: SampleLimits = {
        Color.RED: 12,
        Color.GREEN: 13,
        Color.BLUE: 14,
    }
    sample_set_pass = SampleSet(
        [
            Sample(color=Color("blue"), number=2),
            Sample(color=Color("red"), number=1),
            Sample(color=Color("green"), number=2),
        ]
    )
    sample_set_fail = SampleSet(
        [
            Sample(color=Color("blue"), number=2),
            Sample(color=Color("red"), number=13),
            Sample(color=Color("green"), number=2),
        ]
    )

    is_sample_set_possible(sample_set_pass, sample_limits) is True
    is_sample_set_possible(sample_set_fail, sample_limits) is False
