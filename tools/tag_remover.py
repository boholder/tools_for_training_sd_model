"""
Batch remove given tags in captions.
If you want the model to learn some tags that image-tag-estimation-systems have tagged, it is a good idea to remove them from the captions.

FYI: What effect image captions have during training:
https://github.com/rinongal/textual_inversion/issues/131
"""
import os
import re
import shutil

BACKUP_FILE_EXT = '.bak'


def remove_tags(config: dict[str, [str, list[str]]]):
    captions_dir = config.get('captions_dir')
    backup_dir = config.get('backup_dir')
    backup_dir = backup_dir if backup_dir else captions_dir

    tags_to_remove: list[str] = config.get('tags_to_remove')
    if len(tags_to_remove) == 0:
        tags_to_remove.append("PLACE_HOLDER")
    tags_to_remove_ = tags_to_remove[0] if len(tags_to_remove) == 1 else f"({'|'.join(config.get('tags_to_remove'))})"
    tags_to_remove_pattern = f"(?<=,)\\s*{tags_to_remove_}\\s*,?"
    # can't use (?<=^|,) or (?<=[,^])
    tags_to_remove_pattern_head = f"^\\s*{tags_to_remove_}\\s*,?"

    part_of_tags_to_remove: list[str] = config.get('part_of_tags_to_remove')
    if len(part_of_tags_to_remove) == 0:
        part_of_tags_to_remove.append("PLACE_HOLDER")
    part_of_tags_to_remove_ = part_of_tags_to_remove[0] if len(
        part_of_tags_to_remove) == 1 else f"({'|'.join(config.get('part_of_tags_to_remove'))})"
    part_of_tags_to_remove_pattern = f"(?<=,)[\\s\\w]*{part_of_tags_to_remove_}[\\s\\w]*,?"
    part_of_tags_to_remove_pattern_head = f"^[\\s\\w]*{part_of_tags_to_remove_}[\\s\\w]*,?"

    caption_files = [f for f in os.listdir(captions_dir) if f.endswith(config.get('caption_file_ext'))]
    for filename in caption_files:
        file_path = os.path.join(captions_dir, filename)
        # back up the file
        shutil.copy(file_path, os.path.join(backup_dir, filename + BACKUP_FILE_EXT))

        content = []
        with open(file_path, 'r') as file:
            for line in file.read().splitlines():
                temp = re.sub(tags_to_remove_pattern, '', line)
                temp = re.sub(tags_to_remove_pattern_head, '', temp)
                temp = re.sub(part_of_tags_to_remove_pattern, '', temp)
                temp = re.sub(part_of_tags_to_remove_pattern_head, '', temp)
                content.append(temp.strip())

        with open(file_path, 'w') as file:
            file.writelines(content)


def recover(config: dict[str, str]):
    """Replacing modified captions with backup files."""
    captions_dir = config.get('captions_dir')
    backup_dir = config.get('backup_dir')
    backup_dir = backup_dir if backup_dir else captions_dir

    caption_files = [f for f in os.listdir(captions_dir) if f.endswith(config.get('caption_file_ext'))]
    for modified_file_name in caption_files:
        file_path = os.path.join(captions_dir, modified_file_name)
        backup_file_path = os.path.join(backup_dir, modified_file_name + BACKUP_FILE_EXT)

        try:
            os.remove(file_path)
        except OSError:
            pass

        shutil.move(backup_file_path, file_path)


if __name__ == '__main__':
    CONFIG = {
        'captions_dir': r'',
        'caption_file_ext': 'txt',
        # match the whole tag
        'tags_to_remove': [],
        # match part of tag
        # e.g. 'eyes' --will match and delete--> 'blue_eyes', 'red eyes', 'green eyes'...
        'part_of_tags_to_remove': [],
        # if not set, backup files will be put into same directory as caption files.
        # call the recover() function to replace modified captions with backup files.
        'backup_dir': r'G:\DIY\2021-2023DIY\tana-SD-LoRA\remove-bak',
    }

    remove_tags(CONFIG)
    # recover(CONFIG)
