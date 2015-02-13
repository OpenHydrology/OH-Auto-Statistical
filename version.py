# -*- coding: utf-8 -*-

from subprocess import check_output, CalledProcessError

TAG_PREFIX = 'v'


def update():
    try:
        git_args = ['git',
                    'describe',
                    '--tags',
                    '--always']
        full_version = check_output(git_args, universal_newlines=True).split('-')

        tag = full_version[0]
        if not tag.startswith(TAG_PREFIX):
            raise ValueError("Tag `{}` must start with `{}`.".format(tag, TAG_PREFIX))
        version = tag[len(TAG_PREFIX):].strip()

        if len(full_version) == 1:
            version_str = version
        else:
            number = full_version[1].strip()
            version_str = '-'.join([version, number])

        with open('VERSION', mode='w', encoding='utf-8') as version_file:
            version_file.write(version_str)

    except CalledProcessError:
        return