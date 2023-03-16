from tools import tag_remover

CONFIG = {
    'captions_dir': r'.\data\remove_tags',
    'caption_file_ext': 'txt',
    # match the whole tag
    'tags_to_remove': ['girl'],
    # match part of tag
    # e.g. 'eyes' --will match and delete--> 'blue_eyes', 'blue eyes', 'green eyes'...
    'part_of_tags_to_remove': ['eye'],
    # if not set, backup files will be put into same directory as caption files.
    # call the recover() function to replace modified captions with backup files.
    'backup_dir': r'',
}


def assert_test_file_contents():
    with open(r'.\data\remove_tags\a.txt', 'r') as f:
        assert f.read().splitlines() == ['girl, smile, blue_eyes, girl , girl, looks at viewer, girl']

    with open(r'.\data\remove_tags\b.txt', 'r') as f:
        assert f.read().splitlines() == ['red eyes, smile, green eyes, angry, green eyes max, yellow eyes']


def test_tag_remover():
    assert_test_file_contents()
    tag_remover.remove_tags(CONFIG)

    with open(r'.\data\remove_tags\a.txt', 'r') as f:
        assert f.read().splitlines() == ['smile, looks at viewer,']

    with open(r'.\data\remove_tags\b.txt', 'r') as f:
        assert f.read().splitlines() == ['smile, angry,']

    tag_remover.recover(CONFIG)
    assert_test_file_contents()
