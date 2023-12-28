from pt1 import find_winning


def test_find_winning():
    assert find_winning(7, 9) == range(2, 6, 1)
    assert find_winning(15, 40) == range(4, 12, 1)
    assert find_winning(30, 200) == range(11, 20, 1)
