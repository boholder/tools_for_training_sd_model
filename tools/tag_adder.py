"""
Add tags into captions.
"""
import os
import shutil

BACKUP_FILE_EXT = '.bak'


def add_tags(config: dict[str, [str, list[str]]]):
    captions_dir = config.get('captions_dir')
    backup_dir = config.get('backup_dir')
    backup_dir = backup_dir if backup_dir else captions_dir

    caption_files = [f for f in os.listdir(captions_dir) if f.endswith(config.get('caption_file_ext'))]
    for filename in caption_files:
        file_path = os.path.join(captions_dir, filename)
        # back up the file
        shutil.copy(file_path, os.path.join(backup_dir, filename + BACKUP_FILE_EXT))

        with open(file_path, 'a') as file:
            file.write(','.join(config.get('tags_to_add')))


if __name__ == '__main__':
    CONFIG = {
        'captions_dir': r'',
        'caption_file_ext': 'txt',
        'tags_to_add': [],
        # if not set, backup files will be put into same directory as caption files.
        # call the recover() function to replace modified captions with backup files.
        'backup_dir': r'G:\DIY\2021-2023DIY\himemiyamaho-LoRA\caption_bak',
    }

    add_tags(CONFIG)
