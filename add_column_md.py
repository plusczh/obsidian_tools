import pandas as pd
import os
from pathlib import Path

def get_files(patterns, path):
    all_files = []
    p = Path(path)
    for item in patterns:
        file_name = p.rglob(f'**/*{item}')
        all_files.extend(file_name)
    return all_files

if __name__ == '__main__':
    update_dir = '/Users/rod/OneDrive/Infrod/0-体验清单'
    patterns = ['.md']
    md_files = get_files(patterns, update_dir)
    for md_path in md_files:
        name = os.path.basename(md_path).split('.')[0]
        with open(md_path, "r") as f:
            md_data = f.readlines()
        print('Adding column to {}...'.format(name))
        md_data.append('douban_link:: \n')
        md_data.append('douban_rating:: \n')
        with open(md_path, "w") as f:
            f.writelines(md_data)
        