import os
import sys
import tempfile
import shutil
from datetime import date


HELP_TEXT = \
"""One of the following arguments must be supplied:
- 'major': to increase major version number, e.g. from 1.2.3 to 2.0.0
- 'minor': to increase minor version number, e.g. from 1.2.3 to 1.3.0
- 'patch': to increase patch number, e.g. from 1.2.3 to 1.2.4"""

LEVELS = ['major', 'minor', 'patch']


def main(argv):
    try:
        level_index = LEVELS.index(argv[0].lower())  # 0, 1 or 2
    except (IndexError, ValueError):
        print(HELP_TEXT)
        sys.exit()

    old_version = existing_version()

    new_version = [0, 0, 0]
    for index, value in enumerate(new_version[0:level_index]):
        new_version[index] = old_version[index]
    new_version[level_index] = old_version[level_index] + 1

    print("Previous version: {}.{}.{}".format(*old_version))
    print("Current version:  {}.{}.{}".format(*new_version))

    update_version_file(new_version)
    print("VERSION file updated.")

    update_changelog(new_version)
    print("CHANGELOG.txt updated.")


def existing_version():
    return [int(s) for s in open('VERSION').read().split('.')]


def replace_file_content(file_name, content):
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as temp_file:
        for line in content:
            temp_file.write(line)
    shutil.copy(temp_file.name, file_name)
    os.remove(temp_file.name)


def update_version_file(new_version):
    file_name = 'VERSION'
    new_content = '.'.join([str(i) for i in new_version])
    replace_file_content(file_name, new_content)


def update_changelog(new_version):
    file_name = 'CHANGELOG.txt'

    header = 'version {}.{}.{} ({})'.format(new_version[0], new_version[1], new_version[2], date.today())
    new_content = [header + '\n', '-' * len(header) + '\n']
    with open(file_name, encoding='utf-8') as f:
        for line in f:
            new_content.append(line)

    replace_file_content(file_name, new_content)


if __name__ == "__main__":
    main(sys.argv[1:])