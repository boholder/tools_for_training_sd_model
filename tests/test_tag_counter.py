from tools import tag_counter


def test_tag_counter():
    assert tag_counter.count_tag_frequencies('./data/count_tags') == {
        'girl': 2,
        'blue_eyes': 1,
        'smile': 1,
        'green eyes': 1,
        'angry': 1,
    }
