# -*- coding: utf-8 -*-

from subprocess import check_output, CalledProcessError

TAG_PREFIX = 'v'


def update():
    try:
        git_args = ['git',
                    'describe',
                    '--tags',
                    '--always']
        full_version = check_output(git_args, universal_newlines=True)
        tag, number = full_version.split('-')[0:2]
        if not tag.startswith(TAG_PREFIX):
            raise ValueError("Tag `{}` must start with `{}`.".format(tag, TAG_PREFIX))
        version = tag[len(TAG_PREFIX):]

        with open('VERSION', mode='w', encoding='utf-8') as version_file:
            version_file.write('-'.join([version, number]))

    except CalledProcessError:
        return