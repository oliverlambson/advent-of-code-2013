from pt2 import (
    flatten_sample_sets,
    Color,
    Sample,
    SampleSet,
    SamplesByColor,
    Game,
    get_power_of_game,
)


def test_flatten_sample_sets():
    sample_sets = [
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
    ]
    output_expected = SamplesByColor(
        {
            Color.RED: [6, 1],
            Color.BLUE: [1, 2],
            Color.GREEN: [3, 2],
        }
    )
    output = flatten_sample_sets(sample_sets)
    assert output == output_expected


def test_get_power_of_game():
    game = Game(
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
    expected_output = 36
    output = get_power_of_game(game)
    assert output == expected_output
