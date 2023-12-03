from pt1 import parse_line, Game, Sample, SampleSet


def test_parse_line():
    input = "Game 15: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
    expected_output = Game(
        number=15,
        sample_sets=[
            SampleSet(
                [
                    Sample(color="red", number=6),
                    Sample(color="blue", number=1),
                    Sample(color="green", number=3),
                ]
            ),
            SampleSet(
                [
                    Sample(color="blue", number=2),
                    Sample(color="red", number=1),
                    Sample(color="green", number=2),
                ]
            ),
        ],
    )
    output = parse_line(input)
    assert output == expected_output
