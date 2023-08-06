from typing import List
from functools import reduce
from datetime import datetime
from pathlib import Path
import subprocess
import os
import sh

BASE_DIR = Path.home() / ".donno"
REPO = BASE_DIR / 'repo'
NOTE_FILES = REPO.glob('*.md')
EDIT_CMD = 'nvim'
VIEW_CMD = 'nvim -R'
EDITOR_CONF = {'XDG_CONFIG_HOME': '$HOME/Documents/sources/vimrcs/text'}
CURRENT_NB = '/Diary/2020'

TEMP_FILE = 'newnote.md'
REC_FILE = BASE_DIR / 'record'
TRASH = BASE_DIR / 'trash'


def add_note():
    now = datetime.now()
    created = now.strftime("%Y-%m-%d %H:%M:%S")
    current_nb = CURRENT_NB
    header = ('Title: \nTags: \n'
              f'Notebook: {current_nb}\n'
              f'Created: {created}\n'
              f'Updated: {created}\n\n------\n\n')
    with open(TEMP_FILE, 'w') as f:
        f.write(header)
    subprocess.run(f'{EDIT_CMD} {TEMP_FILE}', shell=True,
                   env={**os.environ, **EDITOR_CONF})
    # EDITOR_CONF must be put AFTER `os.environ`, for in above syntax,
    # the latter will update the former
    # meanwhile, sh package is not suitable for TUI, so here I use subprocess
    fn = f'note{now.strftime("%y%m%d%H%M%S")}.md'
    # print(f'Save note to {REPO}/{fn}')
    if not REPO.exists():
        REPO.mkdir(parents=True)
    sh.mv(TEMP_FILE, REPO / fn)


def update_note(no: int):
    with open(REC_FILE) as f:
        paths = [line.strip() for line in f.readlines()]
    fn = paths[no - 1]
    subprocess.run(f'{EDIT_CMD} {fn}', shell=True,
                   env={**os.environ, **EDITOR_CONF})
    updated = datetime.fromtimestamp(
        Path(fn).stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    sh.sed('-i', f'5c Updated: {updated}', fn)
    print(list_notes(5))  # TODO move magic number to config file


def view_note(no: int):
    with open(REC_FILE) as f:
        paths = [line.strip() for line in f.readlines()]
    fn = paths[no - 1]
    subprocess.run(f'{VIEW_CMD} {fn}', shell=True,
                   env={**os.environ, **EDITOR_CONF})


def extract_header(path: Path) -> str:
    header_line_number = 5
    with open(path) as f:
        header = []
        for x in range(header_line_number):
            header_sections = next(f).strip().split(': ')
            header.append(header_sections[1]
                          if len(header_sections) > 1 else '')
    return (f'[{header[4]}] {header[0]} [{header[1]}] {header[2]} '
            f'{header[3]}')


def record_to_details():
    title_line = 'No. Updated, Title, Tags, Notebook, Created'
    with open(REC_FILE) as f:
        paths = [line.strip() for line in f.readlines()]
    headers = [extract_header(path) for path in paths]
    with_index = [f'{idx + 1}. {ele}' for idx, ele in enumerate(headers)]
    return '\n'.join([title_line, *with_index])


def list_notes(number):
    file_list = sorted(NOTE_FILES, key=lambda f: f.stat().st_mtime,
                       reverse=True)
    with open(REC_FILE, 'w') as f:
        f.write('\n'.join([str(path) for path in file_list[:number]]))
    return record_to_details()


def delete_note(no: int):
    with open(REC_FILE) as f:
        paths = [line.strip() for line in f.readlines()]
    if not TRASH.exists():
        TRASH.mkdir()
    sh.mv(paths[no - 1], TRASH)


def filter_word(file_list: List[str], word: str) -> List[str]:
    if len(file_list) == 0:
        return []
    try:
        res = sh.grep('-i', '-l', word, file_list)
    except sh.ErrorReturnCode_1:
        return []
    else:
        return res.stdout.decode('UTF-8').strip().split('\n')


def simple_search(word_list: List[str]) -> List[str]:
    search_res = reduce(filter_word, word_list, list(NOTE_FILES))
    if len(search_res) == 0:
        return ""
    with open(REC_FILE, 'w') as f:
        f.write('\n'.join([str(path) for path in search_res]))
    return record_to_details()
